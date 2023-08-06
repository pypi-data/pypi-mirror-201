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

import hankai.lib
from hankai.aws.sdk import ServiceName, Servicer


class SimpleStorageServiceEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and SimpleStorageService attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_S3_BUCKET = "bucket"


@dataclass
class SimpleStorageService:  # pylint: disable=too-many-instance-attributes
    """Class to manage AWS S3..

    hankai.aws..Servicer.service_name *must* be defined
    as "s3".

    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html
    """

    servicer: Servicer
    bucket: str
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            hankai.lib.LogEnv().env_supersede(clz=self, env_type=self.env)
        if self.servicer.service_name != ServiceName.SIMPLE_STORAGE_SERVICE:
            raise ValueError(
                f"Servicer.service_name must be [{ServiceName.SIMPLE_STORAGE_SERVICE}]."
            )

    def resource(self) -> Any:
        """Return the resource."""
        return self.servicer.resource()

    def client(self) -> Any:
        """Return the client."""
        return self.servicer.client()

    def resource_bucket(self) -> Any:
        """Return the resource Bucket."""
        return self.resource().Bucket(self.bucket)

    def put(self, key: str, body: bytes) -> Any:
        """Put an object into the bucket and return the object resource."""
        kwargs = {"Bucket": self.bucket, "Key": key, "Body": body}

        return self.resource_bucket().put(**kwargs)

    def put_multipart(self, file_path: str, key: str) -> Any:
        """Put an object into the bucket with multipart upload and return the
        object resource.
        """
        if self.servicer.config is not None:
            return self.client().upload_file(
                file_path, self.bucket, key, Config=self.servicer.config
            )

        return self.client().upload_file(file_path, self.bucket, key)

    def get(self, key: str) -> bytes:
        """Get an object from the bucket and return the file like object."""

        data = b""
        bucket = self.resource_bucket()
        bucket.download_fileobj(key, data)

        return data
