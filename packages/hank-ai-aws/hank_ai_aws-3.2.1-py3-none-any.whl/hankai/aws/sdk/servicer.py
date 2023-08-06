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
"""Manage AWS Boto3 Client and Resource."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Type, Union

import botocore  # type: ignore # found module but no type hints or library stubs

# AWS SQS - S3 Large Message support
# https://pypi.org/project/sqs-extended-client/
import sqs_extended_client  # type: ignore # pylint: disable=unused-import

import hankai.lib

from .session import Session


class ServiceName(hankai.lib.MemberValue):
    """Supported AWS Boto3 service names."""

    EC2_AUTOSCALING = "autoscaling"
    ELASTIC_CONTAINER_SERVICE = "ecs"
    SIMPLE_STORAGE_SERVICE = "s3"
    SIMPLE_QUEUE_SERVICE = "sqs"

    def __str__(self) -> str:
        return str(self.value)


class ServicerEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and Servicer attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SERVICER_SERVICE_NAME = "service_name"
    HANK_SERVICER_API_VERSION = "api_version"
    HANK_SERVICER_USE_SSL = "use_ssl"
    HANK_SERVICER_VERIFY = "verify"
    HANK_SERVICER_ENDPOINT_URL = "endpoint_url"


@dataclass
class Servicer:  # pylint: disable=too-many-instance-attributes
    """Servicer to get the AWS Boto3 Session Client or Resource by
    service name.

    [region_name], [aws_access_key_id], [aws_secret_access_key],
    [session_token] and [config], if needed, should be provided in
    via [aws: Session].

    ! IMPORTANT: This class should not be instantiated in any class __init__.
    Depending on the credentials the session TTL will *not* be persistent over
    long running durations. Simpler to instantiate boto3 Session for each call.

    Using custom Session rather than the default session Boto3 acts as a proxy
    for low level client instantiation.

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
    """

    # pylint: disable=too-many-arguments
    # session: hankai.aws..session.Session
    session: Session
    service_name: ServiceName
    logenv: hankai.lib.LogEnv
    api_version: Optional[str] = None
    use_ssl: bool = True
    verify: Optional[Union[bool, str]] = None  # AWS Boto3 default is True
    endpoint_url: Optional[str] = None
    config: Optional[botocore.client.Config] = None
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

    def client(self) -> Any:
        """AWS Boto3 Client
        Return type hint is Any as a factory is used and the return
        class can be nearly anything.
        e.g. 'sqs' -> boto3.resources.factory.sqs.ServiceResource

        https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/session.html#Session
        """
        return self.session.session().client(
            service_name=str(self.service_name),
            api_version=self.api_version,
            use_ssl=self.use_ssl,
            verify=self.verify,
            endpoint_url=self.endpoint_url,
            config=self.config,
        )

    def resource(self) -> Any:
        """AWS Boto3 Resource
        Return type hint is Any as a factory is used and the return
        class can be nearly anything.
        e.g. 'sqs' -> boto3.resources.factory.sqs.ServiceResource

        https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/session.html#Session
        """
        return self.session.session().resource(
            service_name=str(self.service_name),
            api_version=self.api_version,
            use_ssl=self.use_ssl,
            verify=self.verify,
            endpoint_url=self.endpoint_url,
            config=self.config,
        )
