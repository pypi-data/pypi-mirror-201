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
from typing import Optional, Type

import backoff
from pendulum.datetime import DateTime

import hankai.lib
from hankai.aws.service import EC2AutoScalingGroup, EC2AutoScalingGroupState

from ..base.scale import Scale
from ..by.sqs import ScaleBySQS


@dataclass
class ScaleEC2ASGBySQS(Scale):  # pylint: disable=too-many-instance-attributes
    """Class to monitor AWS SQS and adjust AWS EC2 Auto Scaling Group desired
    capacity based on the monitored SQS queue. As the queue message depth
    increases the inferred tasks/capacity will increase by a proportional amount
    based on the scaling block size.

    The scaling block size is a rough approximation of the aggregate group of
    messages that can be processed an amount of time that makes it worthwhile
    to scale out or in the cluster services.

    This runs indefinitely. If there are too many exceptions it will abort.
    There are functions with backoff limiters for cases where the SQS queue
    returns zero messages repeatedly as well as when the inferred capacity
    remains the same between calls.

    [aws_scale_ecs_by_sqs_expected_scaling_seconds=0] will disable warning for
    exceeding expected scaling action time.

    Setting [disable_adjustment=True] will
    disable any capacity adjustment that would have resulted in an actual
    adjustment and will instead report the predicted capacity. Monitoring
    of the AWS SQS queue will occur once every
    [disable_adjustment_delay_seconds].
    """

    ec2asg: EC2AutoScalingGroup
    sqs_scale: ScaleBySQS
    logenv: hankai.lib.LogEnv
    backoff: hankai.lib.Backoff
    expected_scaling_seconds: int = 600
    disable_adjustment: bool = False
    disable_adjustment_delay_seconds: int = 60
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.expected_scaling_seconds = max(self.expected_scaling_seconds, 0)
        self.disable_adjustment_delay_seconds = max(
            self.disable_adjustment_delay_seconds, 0
        )

        self.__scaling_start_datetime: Optional[DateTime] = None

    def ready_to_scale(self, state: EC2AutoScalingGroupState) -> bool:
        """Report if the AWS EC2 Auto Scaling Group is ready to receive a
        new adjustment.
        """
        is_ready = True

        if state.max_capacity == 0:
            self.logenv.logger.critical(
                "AWS EC2 Auto Scaling Group [{}] maximum capacity is zero. "
                "Scaling is not possible.",
                self.ec2asg.group_name,
            )
            is_ready = False

        # Unless there is a manual AWS Console change to the ASG
        # _pending_inferred_desired_capacity is only set after a call to adjust
        # the ASG and ECS desired counts. Subsequent scaling actions are
        # ignored if the current scaling action is active. Must wait for the
        # current scaling action to complete.
        if is_ready and self.ec2asg.scaling_active() is True:
            if self.logenv.verbosity > 0:
                self.logenv.logger.info(
                    "AWS EC2 Auto Scaling Group [{}] most recent scaling event "
                    "is in progress.",
                    self.ec2asg.group_name,
                )
            is_ready = False

        if is_ready and self.ec2asg.scaling_successful() is False:
            self.logenv.logger.critical(
                "AWS EC2 Auto Scaling Group [{}] most recent scaling event "
                "was not successful.",
                self.ec2asg.group_name,
            )

        if is_ready and len(state.in_service) != state.desired_capacity:
            if self.logenv.verbosity > 0:
                self.logenv.logger.warning(
                    "AWS EC2 Auto Scaling Group [{}] in-service instances "
                    "[{}] does not equal the pending desired capacity [{}].",
                    self.ec2asg.group_name,
                    len(state.in_service),
                    state.desired_capacity,
                )
            is_ready = False

        return is_ready

    def predict_capacity(
        self,
    ) -> Optional[int]:
        """Get the current state and infer the desired tasks count from the
        queue length.

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
        def _predict_capacity() -> Optional[int]:
            """Get the current AWS EC2 Auto Scaling Group and ECS states.

            https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Deployment.html
            """
            state = self.ec2asg.capacity_states()

            if self.__scaling_start_datetime:
                elapsed_seconds = self.elapsed_scaling_seconds(
                    start=self.__scaling_start_datetime
                )
                if len(state.in_service) == state.desired_capacity:
                    if elapsed_seconds:
                        self.logenv.logger.success(
                            "AWS EC2 Auto Scaling Group [{}] scaling action "
                            "completed in [{}] seconds. In-service instances "
                            "[{}] equals desired capacity [{}].",
                            self.ec2asg.group_name,
                            elapsed_seconds,
                            state.in_service,
                            state.desired_capacity,
                        )
                    self.__scaling_start_datetime = None
                    return None

                if self.expected_scaling_seconds > 0:
                    if (
                        elapsed_seconds
                        and elapsed_seconds > self.expected_scaling_seconds
                    ):
                        self.logenv.logger.warning(
                            "AWS EC2 Auto Scaling Group [{}] scaling action "
                            "elapsed time [{}] has exceeded the expected "
                            "scaling action seconds [{}].",
                            self.ec2asg.group_name,
                            elapsed_seconds,
                            self.expected_scaling_seconds,
                        )

            if not self.disable_adjustment and not self.ready_to_scale(state=state):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] scaling is not ready; "
                        "triggering backoff for adjusting capacity.",
                        self.ec2asg.group_name,
                    )
                return None

            if not self.disable_adjustment and state.desired_capacity != len(
                state.in_service
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] in-service count [{}] "
                        "does not equal desired capacity count [{}]. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.ec2asg.group_name,
                        len(state.in_service),
                        state.desired_capacity,
                    )
                return None

            _, desired_capacity = self.sqs_scale.infer_desired_capacity(
                min_instances=state.min_capacity, max_instances=state.max_capacity
            )

            if self.disable_adjustment:
                return desired_capacity

            if state.desired_capacity == desired_capacity:
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS EC2 Auto Scaling Group [{}] desired capacity count "
                        "[{}] equals the inferred desired capacity count [{}]. "
                        "Scaling action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.ec2asg.group_name,
                        state.desired_capacity,
                        desired_capacity,
                    )
                return None

            return desired_capacity

        return _predict_capacity()

    def adjust_capacity(self) -> None:
        """Gets the predicted AWS EC2 Auto Scaling Group desired capacity based
        on the AWS SQS queue length and scale in or out the EC2 Auto Scaling
        Group desired capacity.
        """
        while True:
            desired_capacity: Optional[int] = self.predict_capacity()

            if desired_capacity is None:
                # This thread is blocked by predict_capacity backoff.
                # desired_tasks=None should never occur.
                raise AssertionError(
                    "AWS EC2 Auto Scaling Group [desired_capacity=None]."
                )

            if self.disable_adjustment:
                self.logenv.logger.warning(
                    "Scaling action disabled. AWS EC2 Auto Scaling Group [{}] "
                    "inferred capacity count is [{}]. Delaying next inference "
                    "for [{}] seconds.",
                    self.ec2asg.group_name,
                    desired_capacity,
                    self.disable_adjustment_delay_seconds,
                )
                time.sleep(self.disable_adjustment_delay_seconds)
                return

            self.logenv.logger.info(
                "Scaling action initiated. Setting AWS EC2 Auto Scaling Group "
                "[{}] desired capacity count [{}].",
                self.ec2asg.group_name,
                desired_capacity,
            )

            self.__scaling_start_datetime = hankai.lib.Util.date_now()
            self.ec2asg.set_desired_capacity(desired_capacity=desired_capacity)
