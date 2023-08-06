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
"""Manage AWS ECS Scale by SQS queue properties."""
import time
from dataclasses import dataclass
from typing import Optional, Type

import backoff
from pendulum.datetime import DateTime

import hankai.lib
from hankai.aws.service import ElasticContainerService, ElasticContainerServiceState

from ..base.scale import Scale
from ..by.sqs import ScaleBySQS


@dataclass
# pylint: disable=too-many-ancestors disable=too-many-instance-attributes
class ScaleECSBySQS(Scale):
    """Class to monitor AWS SQS and adjust AWS ECS cluster service desired tasks
    based on the monitored SQS queue. As the queue message depth increases the
    inferred tasks/capacity will increase by a proportional amount based on the
    scaling block size.

    The scaling block size is a rough approximation of the aggregate group of
    messages that can be processed an amount of time that makes it worthwhile
    to scale out or in the cluster services.

    This runs indefinitely. If there are too many exceptions it will abort.
    There are functions with backoff limiters for cases where the SQS queue
    returns zero messages repeatedly as well as when the inferred capacity
    remains the same between calls.

    [expected_scaling_seconds=0] will disable warning for
    exceeding expected scaling action time.

    [max_desired_tasks]
    https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-quotas.html

    Setting [disable_adjustment=True] will
    disable any capacity adjustment that would have resulted in an actual
    adjustment and will instead report the predicted capacity. Monitoring
    of the AWS SQS queue will occur once every
    [disable_adjustment_delay_seconds].
    """

    ecs: ElasticContainerService
    sqs_scale: ScaleBySQS
    logenv: hankai.lib.LogEnv
    backoff: hankai.lib.Backoff
    min_desired_tasks: int = 0
    max_desired_tasks: int = 5000
    expected_scaling_seconds: int = 600
    disable_adjustment: bool = False
    disable_adjustment_delay_seconds: int = 60
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.min_desired_tasks = max(self.min_desired_tasks, 0)
        self.max_desired_tasks = max(self.max_desired_tasks, 5000)
        self.expected_scaling_seconds = max(self.expected_scaling_seconds, 0)
        if self.min_desired_tasks > self.max_desired_tasks:
            raise ValueError(
                "Argument [min_desired_tasks] must be "
                "less than or equal to [max_desired_tasks]."
            )
        self.disable_adjustment_delay_seconds = max(
            self.disable_adjustment_delay_seconds, 0
        )

        self.__scaling_start_datetime: Optional[DateTime] = None

    def ready_to_scale(self, state: ElasticContainerServiceState) -> bool:
        """Report if the AWS ECS is ready to receive an adjustment."""
        is_ready = True

        if state.status not in ("PRIMARY", "ACTIVE"):
            self.logenv.logger.critical(
                "AWS ECS cluster [{}] service [{}] status is [{}]; "
                "AWS ECS cluster status must be PRIMARY or ACTIVE.",
                self.ecs.cluster_name,
                self.ecs.service_name,
                state.status,
            )
            is_ready = False

        if is_ready and state.running_tasks != state.desired_tasks:
            if self.logenv.verbosity > 0:
                self.logenv.logger.info(
                    "AWS ECS cluster [{}] service [{}] running tasks count "
                    "[{}] has not reached the desired tasks count [{}].",
                    self.ecs.cluster_name,
                    self.ecs.service_name,
                    state.running_tasks,
                    state.desired_tasks,
                )
            is_ready = False

        return is_ready

    def predict_capacity(self) -> Optional[int]:
        """Get the current state and infer the desired tasks count from the
        queue length.

        Wrapper for _predict_capacity to be able to set @backoff
        decorator. See hankai.lib.Backoff.
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

            state = self.ecs.service_states()

            if self.__scaling_start_datetime:
                elapsed_seconds = self.elapsed_scaling_seconds(
                    start=self.__scaling_start_datetime
                )
                if state.running_tasks == state.desired_tasks:
                    if elapsed_seconds:
                        self.logenv.logger.success(
                            "AWS ECS cluster [{}] service [{}] scaling action "
                            "completed in [{}] seconds. Running tasks [{}] "
                            "equals desired tasks [{}].",
                            self.ecs.cluster_name,
                            self.ecs.service_name,
                            elapsed_seconds,
                            state.running_tasks,
                            state.desired_tasks,
                        )
                    self.__scaling_start_datetime = None
                    return None

                if self.expected_scaling_seconds > 0:
                    if (
                        elapsed_seconds
                        and elapsed_seconds > self.expected_scaling_seconds
                    ):
                        self.logenv.logger.warning(
                            "AWS ECS cluster [{}] service [{}] scaling action "
                            "elapsed time [{}] has exceeded the expected "
                            "scaling action seconds [{}].",
                            self.ecs.cluster_name,
                            self.ecs.service_name,
                            elapsed_seconds,
                            self.expected_scaling_seconds,
                        )

            if not self.disable_adjustment and not self.ready_to_scale(state=state):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS ECS cluster [{}] service [{}] scaling is not ready; "
                        "triggering backoff for adjusting capacity.",
                        self.ecs.cluster_name,
                        self.ecs.service_name,
                    )
                return None

            if (
                not self.disable_adjustment
                and state.desired_tasks != state.running_tasks
            ):
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS ECS cluster [{}] service [{}] running tasks count "
                        "[{}] does not equal desired tasks count [{}]. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.ecs.cluster_name,
                        self.ecs.service_name,
                        state.running_tasks,
                        state.running_tasks,
                    )
                return None

            _, desired_capacity = self.sqs_scale.infer_desired_capacity(
                min_instances=self.min_desired_tasks,
                max_instances=self.max_desired_tasks,
            )

            if self.disable_adjustment:
                return desired_capacity

            if desired_capacity == state.desired_tasks:
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "AWS ECS cluster [{}] service [{}] desired tasks count "
                        "[{}] equals inferred desired tasks count [{}]. Scaling "
                        "action is not required; triggering backoff for "
                        "adjusting capacity.",
                        self.ecs.cluster_name,
                        self.ecs.service_name,
                        state.desired_tasks,
                        desired_capacity,
                    )
                return None

            return desired_capacity

        return _predict_capacity()

    def adjust_capacity(self) -> None:
        """Gets the predicted AWS ECS desired tasks capacity based on the AWS
        SQS queue length and scale in or out the ECS service desired tasks.
        """
        while True:
            desired_tasks: Optional[int] = self.predict_capacity()

            if desired_tasks is None:
                # This thread is blocked by predict_capacity backoff.
                # desired_tasks=None should never occur.
                raise AssertionError("AWS ECS [desired_tasks=None].")

            if self.disable_adjustment:
                self.logenv.logger.warning(
                    "Scaling action disabled. AWS ECS cluster [{}] service "
                    "[{}] inferred tasks count is [{}]. Delaying next "
                    "inference for [{}] seconds.",
                    self.ecs.cluster_name,
                    self.ecs.service_name,
                    desired_tasks,
                    self.disable_adjustment_delay_seconds,
                )
                time.sleep(self.disable_adjustment_delay_seconds)
                return

            self.logenv.logger.info(
                "Scaling action initiated. Setting AWS ECS cluster [{}] service "
                "[{}] desired tasks count to [{}].",
                self.ecs.cluster_name,
                self.ecs.service_name,
                desired_tasks,
            )

            self.__scaling_start_datetime = hankai.lib.Util.date_now()
            self.ecs.update_service(desired_count=desired_tasks)
