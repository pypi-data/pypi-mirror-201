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
"""Manage AWS Boto3 Session, Client and Resource."""
from dataclasses import dataclass

import boto3  # type: ignore # found module but no type hints or library stubs

from .environment import Environment


@dataclass
class Session:
    """Session to get the boto3 Session.

    ! IMPORTANT: This class should not be instantiated in any class __init__.
    Depending on the credentials the session TTL will *not* be persistent over
    long running durations. Simpler to instantiate boto3 Session for each call.

    Using custom Session rather than the default session Boto3 acts as a proxy
    for low level client instantiation.

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
    """

    environment: Environment

    def session(self) -> boto3.Session:
        """AWS Boto3 Session

        https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/session.html#Session
        """
        return boto3.Session(
            aws_access_key_id=self.environment.access_key_id,
            aws_secret_access_key=self.environment.secret_access_key,
            aws_session_token=self.environment.session_token,
            region_name=self.environment.region,
            botocore_session=self.environment.botocore_session,
            profile_name=self.environment.profile,
        )
