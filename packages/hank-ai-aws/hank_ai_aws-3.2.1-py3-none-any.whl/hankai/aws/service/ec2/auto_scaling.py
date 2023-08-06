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
"""Manage AWS EC2 Auto Scaling."""
from dataclasses import dataclass, field
from typing import Any, List, Optional, Type

import jsonpickle  # type: ignore[import]
from pendulum.datetime import DateTime

import hankai.lib
from hankai.aws.sdk import ServiceName, Servicer


@dataclass
class EC2AutoScalingGroupState:  # pylint: disable=too-many-instance-attributes
    """Class to contain the AWS EC2 Auto Scaling Group service state."""

    desired_capacity: int = -1
    min_capacity: int = -1
    max_capacity: int = -1
    pending: List[str] = field(default_factory=list)
    pending_wait: List[str] = field(default_factory=list)
    pending_proceed: List[str] = field(default_factory=list)
    in_service: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.eventual_in_service = (
            self.in_service + self.pending + self.pending_wait + self.pending_proceed
        )


class EC2AutoScalingGroupEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and EC2AutoScalingGroupEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_EC2ASG_GROUP_NAME = "group_name"
    HANK_EC2ASG_HONOR_COOLDOWN = "honor_cooldown"


@dataclass
class EC2AutoScalingGroup:  # pylint: disable=too-many-instance-attributes
    """Class to manage the AWS EC2 Auto Scaling Group.

    hankai.aws.Servicer.service_name *must* be defined
    as "autoscaling".

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups
    """

    servicer: Servicer
    group_name: str
    logenv: hankai.lib.LogEnv
    honor_cooldown: bool = True
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        if self.servicer.service_name != ServiceName.EC2_AUTOSCALING:
            raise ValueError(
                f"Servicer.service_name must be [{ServiceName.EC2_AUTOSCALING}]."
            )
        self.__scaling_start_datetime: Optional[DateTime] = None

    def elapsed_scaling_seconds(self) -> Optional[float]:
        """Calculate the scaling action elapsed time."""
        if self.__scaling_start_datetime:
            return hankai.lib.Util.elapsed_seconds(start=self.__scaling_start_datetime)

        return None

    def resource(self) -> Any:
        """Return the resource."""
        return self.servicer.resource()

    def client(self) -> Any:
        """Return the client."""
        return self.servicer.client()

    def describe(self) -> Any:
        """Return AWS EC2 Auto Scaling Group description."""
        response = self.client().describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                self.group_name,
            ]
        )
        self.logenv.logger.debug(
            "AWS EC2 Auto Scaling Group description response:\n{}",
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        return response

    def scaling_activities(self) -> Any:
        """Return AWS EC2 Auto Scaling Group scaling activities."""
        response = self.client().describe_scaling_activities(
            AutoScalingGroupName=self.group_name,
            IncludeDeletedGroups=False,
        )
        self.logenv.logger.debug(
            "AWS EC2 Auto Scaling Group activities response:\n{}",
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        return response

    def scaling_active(self) -> bool:
        """Resolve if AWS EC2 Auto Scaling Group most recent scaling event is
        active.
        """
        is_active = False
        activities = self.scaling_activities()
        if (
            activities.get("Activities")
            and activities["Activities"][0].get("EndTime") is None
        ):
            is_active = True

        return is_active

    def scaling_successful(self) -> Optional[bool]:
        """Resolve if AWS EC2 Auto Scaling Group most recent scaling event
        was successful. None is returned if there is active scaling.
        """
        is_successful = None
        if not self.scaling_active():
            is_successful = False
            activities = self.scaling_activities()
            if activities.get("Activities"):
                if activities["Activities"][0].get("EndTime"):
                    status_code = activities["Activities"][0].get("StatusCode")
                    if status_code == "Successful":
                        is_successful = True

        return is_successful

    def capacity_states(
        self,
    ) -> EC2AutoScalingGroupState:
        """Return scaling group capacities states"""
        state = EC2AutoScalingGroupState()
        response = self.describe()

        if response is None:
            return state

        self.logenv.logger.debug(
            "AWS Auto Scaling Group [{}] describe auto scaling groups response:\n{}",
            self.group_name,
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        state.desired_capacity = response["AutoScalingGroups"][0]["DesiredCapacity"]
        state.min_capacity = response["AutoScalingGroups"][0]["MinSize"]
        state.max_capacity = response["AutoScalingGroups"][0]["MaxSize"]

        for inst in response["AutoScalingGroups"][0]["Instances"]:
            lc_state = inst["LifecycleState"]
            if lc_state == "Pending":
                state.pending.append(inst)
            elif lc_state == "Pending:Wait":
                state.pending_wait.append(inst)
            elif lc_state == "Pending:Proceed":
                state.pending_proceed.append(inst)
            elif lc_state == "InService":
                state.in_service.append(inst)

        return state

    def set_desired_capacity(
        self,
        desired_capacity: int = 0,
    ) -> Any:
        """Set the desired capacity. If HonorCooldown is True then the request
        will be ignored.

        Boto3 set_desired_capacity *should* raise exception if desired
        capacity < min or > max, but that has not been tested.
        """
        response = self.client().set_desired_capacity(
            AutoScalingGroupName=self.group_name,
            DesiredCapacity=desired_capacity,
            HonorCooldown=self.honor_cooldown,
        )
        self.logenv.logger.debug(
            "Setting desired capacity [{}] for AWS Auto Scaling Group "
            "[{}] honor cooldown [{}]; response:\n{}",
            desired_capacity,
            self.group_name,
            self.honor_cooldown,
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        return response
