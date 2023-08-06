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
"""Manage AWS Elastic Container Service."""
from dataclasses import dataclass
from typing import Any, Optional, Type

import jsonpickle  # type: ignore[import]
from pendulum.datetime import DateTime

import hankai.lib
from hankai.aws.sdk import ServiceName, Servicer


@dataclass
class ElasticContainerServiceState:
    """Class to contain the AWS ECS service state."""

    status: str = ""
    desired_tasks: int = -1
    running_tasks: int = -1
    pending_tasks: int = -1

    def __post_init__(self) -> None:
        self.eventual_tasks = self.running_tasks + self.pending_tasks


class ElasticContainerServiceEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and ElasticContainerService attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_ECS_CLUSTER_NAME = "cluster_name"
    HANK_ECS_SERVICE_NAME = "service_name"
    HANK_ECS_REQUIRE_ACTIVE_STATUS = "require_active_status"


@dataclass
class ElasticContainerService:  # pylint: disable=too-many-instance-attributes
    """Class to manage the AWS Elastic Container Service (ECS).

    hankai.aws..Servicer.service_name *must* be defined
    as "ecs".

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html
    """

    servicer: Servicer
    cluster_name: str
    service_name: str
    logenv: hankai.lib.LogEnv
    require_active_status: bool = True
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        if self.servicer.service_name != ServiceName.ELASTIC_CONTAINER_SERVICE:
            raise ValueError(
                f"Servicer.service_name must be [{ServiceName.ELASTIC_CONTAINER_SERVICE}]."
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
        """Return the ECS Service description."""
        response = self.client().describe_services(
            cluster=self.cluster_name,
            services=[
                self.service_name,
            ],
            include=[
                "TAGS",
            ],
        )
        self.logenv.logger.debug(
            "AWS ECS describe services response:\n{}",
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        return response

    def service_states(
        self,
    ) -> ElasticContainerServiceState:
        """Return the ECS Service status and task state counts."""
        state = ElasticContainerServiceState()
        response = self.describe()

        if response is None:
            return state

        self.logenv.logger.debug(
            "AWS ECS cluster [{}] service [{}] describe services; response:\n{}",
            self.cluster_name,
            self.service_name,
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        # Allow raise exception for KeyError, TypeError etc.
        state.status = response["services"][0]["status"]
        state.desired_tasks = int(response["services"][0]["desiredCount"])
        state.running_tasks = int(response["services"][0]["runningCount"])
        state.pending_tasks = int(response["services"][0]["pendingCount"])

        return state

    def scaling_active(self) -> bool:
        """Resolve if AWS ECS most recent scaling event is active."""
        is_active = False
        activities = self.service_states()
        if activities.desired_tasks != activities.running_tasks:
            is_active = True

        return is_active

    def scaling_successful(self) -> Optional[bool]:
        """Resolve if AWS ECS most recent scaling event
        was successful. None is returned if there is active scaling.
        """
        is_successful = None
        if self.__scaling_start_datetime and not self.scaling_active():
            is_successful = False
            activities = self.service_states()
            if activities.desired_tasks == activities.running_tasks:
                is_successful = True

        return is_successful

    def update_service(self, desired_count: int) -> Any:
        """Set the ECS Service task count."""
        response = self.client().update_service(
            cluster=self.cluster_name,
            service=self.service_name,
            desiredCount=desired_count,
        )
        self.logenv.logger.debug(
            "Setting desired task count [{}] for AWS ECS cluster name "
            "[{}] service [{}]; response:\n{}",
            desired_count,
            self.cluster_name,
            self.service_name,
            jsonpickle.encode(response, unpicklable=False, indent=2)
            if self.logenv.verbosity > 1
            else "(redacted; verbosity < 2)",
        )

        return response
