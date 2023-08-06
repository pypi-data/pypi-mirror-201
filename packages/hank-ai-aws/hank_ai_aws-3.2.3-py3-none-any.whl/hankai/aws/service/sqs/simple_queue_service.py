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
"""Manage AWS SimpleQueueService."""
from __future__ import annotations

import copy
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Type

import hankai.lib
from hankai.aws.sdk import ServiceName, Servicer
from hankai.aws.service.s3 import SimpleStorageService


# pylint: disable=too-many-instance-attributes
@dataclass
class SQSMessage:
    """Class to mimic the AWS SQS Resource Message to allow easy swap out
    either of [client_receive_message] or
    [resource_receive_messages]. Also, defining the class as
    the Boto3 SQS Messages are of Any.
    """

    message_id: Optional[str] = None
    receipt_handle: Optional[str] = None
    body: Optional[str] = None
    md5_of_body: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    message_attributes: Optional[Dict[str, Dict[str, Any]]] = None
    md5_of_message_attributes: Optional[str] = None
    queue_url: Optional[str] = None

    def redacted(self) -> SQSMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        message_copy = copy.deepcopy(self)
        if message_copy.body is not None:
            message_copy.body = hankai.lib.RedactString.STRING.value

        return message_copy


class SimpleQueueServiceEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and SimpleQueueServiceEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SQS_QUEUE_NAME = "queue_name"
    HANK_SQS_RECEIVE_ATTRIBUTE_NAMES = "receive_attribute_names"
    HANK_SQS_MESSAGE_ATTRIBUTE_NAMES = "message_attribute_names"
    HANK_SQS_MAX_MESSAGES = "max_messages"
    HANK_SQS_VISIBILITY_TIMEOUT = "visibility_timeout"
    HANK_SQS_WAIT_TIME_SECONDS = "wait_time_seconds"
    HANK_SQS_MESSAGE_ATTRIBUTES = "message_attributes"
    HANK_SQS_MESSAGE_GROUP_ID = "message_group_id"
    HANK_SQS_S3_BUCKET = "s3_bucket"
    HANK_SQS_S3_ALWAYS = "s3_always"
    HANK_SQS_S3_THRESHOLD_BYTES = "s3_threshold_bytes"


# pylint: disable=too-many-ancestors
@dataclass
class SimpleQueueService:  # pylint: disable=too-many-instance-attributes
    """Class to manage the AWS Simple Service Queue (SQS). It supports
    messages exceeding 256Kb with the sqs_extended_client and AWS S3 for
    message storage.

    To enable SQS-S3 set [s3_bucket]. Set [s3_always=True] to
    send all messages through S3 regardless of size.
    Set [s3_threshold_bytes=X] to define thresholds < 262144.

    NOTE! When using S3 for large messages and the S3 AWS boto3 client/resource
    requires parmeters different from SQS AWS Boto3 client/resource - those
    S3 AWS Boto3 client/resource parameters must be overridden via ENV
    variables.

    hankai.aws..Servicer.service_name *must* be defined
    as "sqs".

    https://pypi.org/project/sqs-extended-client/
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.message
    https://docs.aws.amazon.com/SimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling
    """

    servicer: Servicer
    queue_name: str
    logenv: hankai.lib.LogEnv
    receive_attribute_names: List[str] = field(default_factory=lambda: ["All"])
    message_attribute_names: List[str] = field(default_factory=list)
    max_messages: int = 10
    visibility_timeout: int = 600
    wait_time_seconds: int = 5
    message_attributes: Dict[str, Any] = field(default_factory=dict)
    message_group_id: Optional[str] = None
    s3_bucket: Optional[str] = None
    s3_always: bool = False
    s3_threshold_bytes: Optional[int] = None
    env: Optional[Type[hankai.lib.EnvEnum]] = None
    s3_env: Optional[Type[hankai.lib.EnvEnum]] = None
    s3_servicer_env: Optional[Type[hankai.lib.EnvEnum]] = None

    # pylint: disable=too-many-branches
    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        if self.servicer.service_name != ServiceName.SIMPLE_QUEUE_SERVICE:
            raise ValueError(
                f"Servicer.service_name must be [{ServiceName.SIMPLE_QUEUE_SERVICE}]."
            )
        self.max_messages = max(self.max_messages, 1)
        self.visibility_timeout = max(self.visibility_timeout, 0)
        self.wait_time_seconds = max(self.wait_time_seconds, 0)
        if self.queue_is_fifo() and not self.message_group_id:
            raise ValueError("Argument [message_group_id] is required for FIFO queues.")
        if self.s3_bucket:
            if self.s3_threshold_bytes is not None:
                self.s3_threshold_bytes = max(self.s3_threshold_bytes, 0)
                self.s3_threshold_bytes = min(self.s3_threshold_bytes, 262144)

        self.__queue_url: Optional[str] = None

    def _manage_large_messages(self, servicer: Any) -> None:
        """Manage large payloads via S3. The third party Python S3 library for
        large message supports AWS Boto3 S3 client or resource.

        https://pypi.org/project/sqs-extended-client/
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.message
        """
        if self.s3_bucket:
            servicer.large_payload_support = self.s3_bucket
            servicer.always_through_s3 = self.s3_always
            if self.s3_threshold_bytes is not None:
                servicer.message_size_threshold = self.s3_threshold_bytes
            # ! IMPORTANT: The sqs_extended_client attempts creates an S3 client
            # ! session if none passed in. While it works as expected with
            # ! AWS credential ENV variables, it does not work if an AWS profile
            # ! is being used. So, create and S3 resource to pass into the
            # ! extended client. It must also the an S3.Resource to match
            # ! sqs_extended_client AWS S3 calls.
            is_providing_s3 = False
            if self.servicer.session.environment.profile:
                is_providing_s3 = True
                servicer.s3 = SimpleStorageService(
                    env=self.s3_env,
                    servicer=Servicer(
                        env=self.s3_servicer_env,
                        session=self.servicer.session,
                        service_name=ServiceName.SIMPLE_STORAGE_SERVICE,
                        logenv=self.logenv,
                    ),
                    bucket=self.s3_bucket,
                ).resource()

            if self.logenv.verbosity > 0:
                self.logenv.logger.debug(
                    "AWS SQS large message via S3 support bucket [{}], always [{}], "
                    "threshold bytes [{}], providing S3 resource [{}]",
                    servicer.large_payload_support,
                    servicer.always_through_s3,
                    servicer.message_size_threshold,
                    is_providing_s3,
                )

    def resource(self) -> Any:
        """Return the resource."""
        return self.servicer.resource()

    def client(self) -> Any:
        """Return the client."""
        client = self.servicer.client()
        self._manage_large_messages(client)

        return client

    def resource_queue(self) -> Any:
        """Return the resource queue by name."""
        queue = self.resource().get_queue_by_name(QueueName=self.queue_name)
        self._manage_large_messages(queue)

        return queue

    @property
    def queue_url(self) -> str:
        """Return the queue URL."""
        if self.__queue_url:
            return self.__queue_url
        self.__queue_url = str(self.resource_queue().url)

        return self.__queue_url

    def attributes(self, attribute_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Return the all the queue attributes or a subset of them."""
        all_attributes: Dict[str, Any] = self.resource_queue().attributes
        if attribute_names is None:
            return all_attributes

        sub_attr = {key: all_attributes[key] for key in attribute_names}

        return sub_attr

    def approximate_number_messages(self) -> Tuple[int, int, int]:
        """Return the queue approximate number of messages. It returns a tuple
        of three integers ApproximateNumberOfMessages, ApproximateNumberOfMessagesNotVisible
        and ApproximateNumberOfMessagesDelayed.

        ! Warning: The ApproximateNumberOfMessagesDelayed,
        ApproximateNumberOfMessagesNotVisible and ApproximateNumberOfMessagesVisible
        metrics may not achieve consistency until at least 1 minute after the
        producers stop sending messages. This period is required for the queue
        metadata to reach eventual consistency.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html
        """
        available_key = "ApproximateNumberOfMessages"
        in_flight_key = "ApproximateNumberOfMessagesNotVisible"
        delayed_key = "ApproximateNumberOfMessagesDelayed"
        attrs = [
            available_key,
            in_flight_key,
            delayed_key,
        ]

        return (
            int(self.attributes(attribute_names=attrs)[available_key]),
            int(self.attributes(attribute_names=attrs)[in_flight_key]),
            int(self.attributes(attribute_names=attrs)[delayed_key]),
        )

    def client_receive_message(self) -> List[SQSMessage]:
        """Receive dict messages from the client."""
        hankai.lib.Sys.write_file(
            file="/tmp/test",
            data=f"in client_receive_message queue[{self.queue_url}]\n",
            append=True,
        )
        kwargs: Dict[str, Any] = {"QueueUrl": self.queue_url}
        if self.receive_attribute_names:
            kwargs["AttributeNames"] = self.receive_attribute_names
        if self.max_messages:
            kwargs["MaxNumberOfMessages"] = self.max_messages
        if self.visibility_timeout:
            kwargs["VisibilityTimeout"] = self.visibility_timeout
        if self.wait_time_seconds:
            kwargs["WaitTimeSeconds"] = self.wait_time_seconds
        if self.message_attribute_names:
            kwargs["MessageAttributeNames"] = self.message_attribute_names

        messages = self.client().receive_message(**kwargs).get("Messages", [])
        hankai.lib.Sys.write_file(
            file="/tmp/test",
            data=f"after receive_message {str(messages)}\n",
            append=True,
        )
        return_messages: List[SQSMessage] = []
        for message in messages:
            return_messages.append(
                SQSMessage(
                    message_id=message["MessageId"],
                    receipt_handle=message["ReceiptHandle"],
                    body=message["Body"],
                    # If Body is empty there will be no
                    # MD5OfBody; don't allow KeyError
                    md5_of_body=message.get("MD5OfBody", None),
                    attributes=message["Attributes"],
                    message_attributes=message["MessageAttributes"],
                    # If MessageAttributes is empty there will be no
                    # MD5OfMessageAttributes; don't allow KeyError
                    md5_of_message_attributes=message.get(
                        "MD5OfMessageAttributes", None
                    ),
                    queue_url=self.queue_url,
                )
            )

        return return_messages

    def resource_receive_messages(self) -> List[SQSMessage]:
        """Receive list of messages from the resource queue."""
        kwargs: Dict[str, Any] = {}
        if self.receive_attribute_names:
            kwargs["AttributeNames"] = self.receive_attribute_names
        if self.max_messages:
            kwargs["MaxNumberOfMessages"] = self.max_messages
        if self.visibility_timeout:
            kwargs["VisibilityTimeout"] = self.visibility_timeout
        if self.wait_time_seconds:
            kwargs["WaitTimeSeconds"] = self.wait_time_seconds
        if self.message_attribute_names:
            kwargs["MessageAttributeNames"] = self.message_attribute_names

        messages = self.resource_queue().receive_messages(**kwargs)
        return_messages: List[SQSMessage] = []
        for message in messages:
            return_messages.append(
                SQSMessage(
                    message_id=message.message_id,
                    receipt_handle=message.receipt_handle,
                    body=message.body,
                    md5_of_body=message.md5_of_body,
                    attributes=message.attributes,
                    message_attributes=message.message_attributes,
                    md5_of_message_attributes=message.md5_of_message_attributes,
                    queue_url=self.queue_url,
                )
            )

        return return_messages

    def send_message(
        self,
        message: str,
    ) -> Any:
        """Send a message to the queue.

        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html
        """
        msg_size_bytes = sys.getsizeof(message)
        if msg_size_bytes < 1 or (msg_size_bytes > 262144 and self.s3_bucket is None):
            raise AssertionError(
                f"Message bytes [{msg_size_bytes}] is less than 1 byte or "
                "greater than 262,144 bytes and AWS S3 bucket was not provided. "
                "Messages greater than 262,144 bytes must use AWS S3."
            )

        kwargs: Dict[str, Any] = {
            "QueueUrl": self.queue_url,
            "MessageBody": message,
        }

        if self.message_attributes:
            kwargs["MessageAttributes"] = self.message_attributes

        # Including MessageGroupId for non-FIFO queues will raise AWS exception.
        if self.queue_is_fifo():
            kwargs["MessageGroupId"] = self.message_group_id

        return self.client().send_message(**kwargs)

    def delete_message(self, receipt_handle: str) -> None:
        """Delete a message from the queue."""
        kwargs = {"QueueUrl": self.queue_url, "ReceiptHandle": receipt_handle}
        self.client().delete_message(**kwargs)

    def queue_is_fifo(self) -> bool:
        """AWS SQS FIFO queues *must* be named with the .fifo suffix.

        https://docs.aws.amazon.com/SimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html
        """
        if re.search(r"\.fifo$", self.queue_name):
            return True

        return False
