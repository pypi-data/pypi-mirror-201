#
# MIT License
#
# Copyright © 2022 Hank AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Manage AWS ASG & ECS Scale by SQS queue properties."""
import time
from dataclasses import dataclass
from typing import Optional, Tuple, Type

import backoff
from pendulum.datetime import DateTime

import hankai.lib
from hankai.aws.service import EC2AutoScalingGroupState, ElasticContainerServiceState

from ..base.scale import Scale
from ..ec2.asg_by_sqs import ScaleEC2ASGBySQS
from ..ecs.by_sqs import ScaleECSBySQS


@dataclass
class ScaleEC2ASGAndECSBySQS(Scale):  # pylint: disable=too-many-instance-attributes

    """Class to monitor AWS SQS and adjust AWS ECS cluster service inferred tasks
    and AWS EC2 Auto Scaling Group inferred capacity based on the monitored SQS
    queue. As the queue message depth increases the inferred tasks/capacity will
    increase by a proportional amount based on the scaling block size.

    AWS EC2 Auto Scaling Group desired capacity will dominate the scaling action
    decisions. AWS ECS cluster service will be adjusted from the metrics of the
    EC2 Auto Scaling Group.

    The scaling block size is a rough approximation of the aggregate group of
    messages that can be processed an amount of time that makes it worthwhile
    to scale out or in the cluster services.

    This runs indefinitely. If there are too many exceptions it will abort.
    There are functions with backoff limiters for cases where the SQS queue
    returns zero messages repeatedly as well as when the inferred capacity
    remains the same between calls.

    [aws_sqs_scale_action_timeout_seconds=0] will disable the timeout check.

    Setting [disable_adjustment=True] will
    disable any capacity adjustment that would have resulted in an actual
    adjustment and will instead report the predicted capacity. Monitoring
    of the AWS SQS queue will occur once every
    [disable_adjustment_delay_seconds].
    """

    asg_sqs: ScaleEC2ASGBySQS
    ecs_sqs: ScaleECSBySQS
    logenv: hankai.lib.LogEnv
    backoff: hankai.lib.Backoff
    ecs_tasks_per_ec2asg_instance: int = 1
    action_timeout_seconds: int = 1200
    disable_adjustment: bool = False
    disable_adjustment_delay_seconds: int = 60
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.ecs_tasks_per_ec2asg_instance = max(self.ecs_tasks_per_ec2asg_instance, 1)
        self.action_timeout_seconds = max(self.action_timeout_seconds, 0)
        self.disable_adjustment_delay_seconds = max(
            self.disable_adjustment_delay_seconds, 0
        )

        self.__scaling_start_datetime: Optional[DateTime] = None

    def ready_to_scale(
        self, state: Tuple[EC2AutoScalingGroupState, ElasticContainerServiceState]
    ) -> bool:
        """Report if the AWS ECS and AWS EC2 Auto Scaling Group are ready to
        receive a new adjustment.
        """
        ec2asg_state, ecs_state = state
        is_ready = False

        ec2asg_ready = self.asg_sqs.ready_to_scale(state=ec2asg_state)
        ecs_ready = self.ecs_sqs.ready_to_scale(state=ecs_state)

        if ec2asg_ready and ecs_ready:
            is_ready = True

        return is_ready

    def predict_capacity(
        self,
    ) -> Optional[int]:
        """Get the current state and infer the desired capacity from the
        queue length.

        Scaling is done when AWS ECS desired tasks count has been achieved. AWS
        ECS services are sometimes dependent on the AWS Auto Scaling Group first
        achieved and offered as an AWS ECS Capacity Provider.

        Wrapper for _predict_capacity to be able to set @backoff decorator.
        See hankai.lib.Backoff.
        """

        @backoff.on_predicate(
            backoff.expo,
            lambda x: x is None,
            max_value=self.backoff.max_value_seconds,
            max_time=self.backoff.max_time_seconds,
            jitter=backoff.full_jitter,
            logger=None,
        )
        def _predict_capacity() -> Optional[  # pylint: disable=too-many-return-statements,too-many-branches
            int
        ]:
            """Get the current AWS EC2 Auto Scaling Group and ECS states.

            https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Deployment.html
            """
            ec2asg_state = self.asg_sqs.ec2asg.capacity_states()
            ecs_state = self.ecs_sqs.ecs.service_states()

            if self.__scaling_start_datetime:
                elapsed_seconds = self.elapsed_scaling_seconds(
                    start=self.__scaling_start_datetime
                )
                if (
                    ecs_state.running_tasks == ecs_state.desired_tasks
                    and len(ec2asg_state.in_service) == ec2asg_state.desired_capacity
                ):
                    if elapsed_seconds:
                        self.logenv.logger.success(
                            "AWS EC2 Auto Scaling Group [{}] and AWS ECS cluster "
                            "[{}] service [{}] scaling action completed in [{}] "
                            "seconds. AWS EC2 in-service instances [{}] and AWS "
                            "ECS running tasks [{}] equals desired "
                            "capacity/tasks [{}].",
                            self.asg_sqs.ec2asg.group_name,
                            self.ecs_sqs.ecs.cluster_name,
                            self.ecs_sqs.ecs.service_name,
                            elapsed_seconds,
                            ec2asg_state.desired_capacity,
                            ecs_state.desired_tasks,
                            ecs_state.desired_tasks,
                            self.action_timeout_seconds,
                        )
                    self.__scaling_start_datetime = None
                    return None

                if self.action_timeout_seconds > 0:
                    if (
                        elapsed_seconds
                        and elapsed_seconds > self.action_timeout_seconds
                    ):
                        self.logenv.logger.warning(
                            "AWS EC2 Auto Scaling Group [{}] and AWS ECS cluster "
                            "[{}] service [{}] scaling action elapsed time [{}] "
                            "has exceeded the expected scaling action seconds [{}].",
                            self.asg_sqs.ec2asg.group_name,
                            self.ecs_sqs.ecs.cluster_name,
                            self.ecs_sqs.ecs.service_name,
                            elapsed_seconds,
                            self.action_timeout_seconds,
                        )

            if not self.disable_adjustment and not self.ready_to_scale(
                state=(ec2asg_state, ecs_state)
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] and/or AWS ECS cluster "
                        "[{}] service [{}] scaling are not ready; triggering "
                        "backoff for adjusting capacity.",
                        self.asg_sqs.ec2asg.group_name,
                        self.ecs_sqs.ecs.cluster_name,
                        self.ecs_sqs.ecs.service_name,
                    )
                return None

            if not self.disable_adjustment and (
                ec2asg_state.desired_capacity != len(ec2asg_state.in_service)
                or ecs_state.desired_tasks != ecs_state.running_tasks
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] in-service count [{}] "
                        "does not equal desired capacity count [{}] and/or AWS "
                        "ECS cluster [{}] service [{}] running tasks count [{}] "
                        "does not equal desired tasks count [{}]. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.asg_sqs.ec2asg.group_name,
                        ec2asg_state.in_service,
                        ec2asg_state.desired_capacity,
                        self.ecs_sqs.ecs.cluster_name,
                        self.ecs_sqs.ecs.service_name,
                        ecs_state.running_tasks,
                        ecs_state.desired_tasks,
                    )
                return None

            # AWS EC2 Auto Scaling Group min/max values are the lower/upper
            # bounds for the ECS desired tasks presuming that the EC2 Auto
            # Scaling Group is a ECS Capacity Provider.
            _, desired_capacity = self.asg_sqs.sqs_scale.infer_desired_capacity(
                min_instances=ec2asg_state.min_capacity,
                max_instances=ec2asg_state.max_capacity,
            )

            if self.disable_adjustment:
                return desired_capacity

            desired_tasks = desired_capacity * self.ecs_tasks_per_ec2asg_instance

            if (
                desired_tasks < self.ecs_sqs.min_desired_tasks
                or desired_tasks > self.ecs_sqs.max_desired_tasks
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS ECS cluster [{}] service [{}] inferred desired "
                        "tasks count [{}] is less than minimum tasks count "
                        "[{}] or greater than maximum tasks count. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.asg_sqs.ec2asg.group_name,
                        ec2asg_state.desired_capacity,
                        desired_capacity,
                        self.ecs_sqs.ecs.cluster_name,
                        self.ecs_sqs.ecs.service_name,
                        ecs_state.desired_tasks,
                        desired_tasks,
                    )
                return None

            if (
                ec2asg_state.desired_capacity == desired_capacity
                and ecs_state.desired_tasks == desired_tasks
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] desired capacity [{}] "
                        "equals inferred desired capacity count [{}] and AWS "
                        "ECS cluster [{}] service [{}] desired tasks count [{}] "
                        "equals inferred desired tasks count [{}]. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.asg_sqs.ec2asg.group_name,
                        ec2asg_state.desired_capacity,
                        desired_capacity,
                        self.ecs_sqs.ecs.cluster_name,
                        self.ecs_sqs.ecs.service_name,
                        ecs_state.desired_tasks,
                        desired_tasks,
                    )
                return None

            return desired_capacity

        return _predict_capacity()

    def adjust_capacity(self) -> None:
        """Some applications run on custom EC2 GPU instances where
        one ECS Service task executes per instance. Therefore, the ECS
        min/max variable is a one-to-one relationship with the EC2 auto
        scaling group min/max and inferred capacity. EC2 Auto Scaling Groups
        min/max will be the precedence for the ECR desired task count. EC2 ASG
        is the limiting factor as the min/max instances. If EC2 ASG is min 1
        then ECS desired will be 1 even if there are 0 messages.
        """
        while True:
            desired_capacity: Optional[int] = self.predict_capacity()

            if desired_capacity is None:
                # This thread is blocked by predict_capacity backoff.
                # state_prediction=None should never occur.
                raise AssertionError(
                    "AWS Auto Scaling Group and AWS ECS [desired_capacity=None]."
                )

            desired_tasks = desired_capacity * self.ecs_tasks_per_ec2asg_instance

            if self.disable_adjustment:
                self.logenv.logger.warning(
                    "Scaling action disabled. AWS EC2 Auto Scaling Group [{}] "
                    "inferred capacity count is [{}] and AWS ECS cluster [{}] "
                    "service [{}] inferred tasks count is [{}]. Delaying next "
                    "inference for [{}] seconds.",
                    self.asg_sqs.ec2asg.group_name,
                    desired_capacity,
                    self.ecs_sqs.ecs.cluster_name,
                    self.ecs_sqs.ecs.service_name,
                    desired_tasks,
                    self.disable_adjustment_delay_seconds,
                )
                time.sleep(self.disable_adjustment_delay_seconds)
                return

            self.logenv.logger.info(
                "Scaling action initiated. Setting AWS EC2 Auto Scaling Group "
                "[{}] desired capacity count [{}] and AWS ECS cluster [{}] "
                "service [{}] desired tasks count [{}].",
                self.asg_sqs.ec2asg.group_name,
                desired_capacity,
                self.ecs_sqs.ecs.cluster_name,
                self.ecs_sqs.ecs.service_name,
                desired_tasks,
            )

            self.__scaling_start_datetime = hankai.lib.Util.date_now()
            self.ecs_sqs.ecs.update_service(desired_count=desired_tasks)
            self.asg_sqs.ec2asg.set_desired_capacity(desired_capacity=desired_capacity)
