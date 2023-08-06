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
"""Parent abstract class for Hank AI AWS projects."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

import botocore.session  # type: ignore # found module but no type hints or library stubs

import hankai.lib


class ProfileOutput(hankai.lib.MemberValue):
    """Supported AWS profile output types."""

    JSON = "json"
    YAML = "yaml"
    YAML_STREAM = "yaml-stream"
    TEXT = "text"
    TABLE = "table"


class EnvironmentEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and Environment attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_ENVIRONMENT_PROFILE = "profile"
    HANK_ENVIRONMENT_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_REGION = "region"
    HANK_ENVIRONMENT_OUTPUT = "output"
    HANK_ENVIRONMENT_MFA_SERIAL_ARN = "mfa_serial_arn"
    HANK_ENVIRONMENT_SESSION_DURATION_SECONDS = "session_duration_seconds"


@dataclass
class Environment:  # pylint: disable=too-many-instance-attributes
    """Class to track and manage the system envirionment AWS profile config
    and credentials.

    hankai.lib.Sys is instantiated with this classes sys_env.
    i.e. hankai.lib.Sys()

    If you need to override any attributes for hankai.lib.Sys() examine that
    class and add a member to the EnvEnum that is passed into this
    classes [sys_env].

    https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
    """

    logenv: hankai.lib.LogEnv
    profile: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    mfa_serial_arn: Optional[str] = None
    region: Optional[str] = None
    output: Optional[ProfileOutput] = None
    botocore_session: Optional[botocore.session.Session] = None
    session_duration_seconds: int = 43200
    env: Optional[Type[hankai.lib.EnvEnum]] = None
    sys_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)
        self._sys = hankai.lib.Sys(logenv=self.logenv)
        if self._sys.get_aws_cli_version() != 2:
            raise AssertionError("AWS CLI v2 is required.")

        self.session_duration_seconds = max(self.session_duration_seconds, 60)
        if self.profile:
            if self.profile_exists():
                if not self.access_key_id:
                    self._get_profile_access_key_id()
                if not self.secret_access_key:
                    self._get_profile_secret_access_key()
                if not self.session_token:
                    self._get_profile_session_token()
                if not self.mfa_serial_arn:
                    self._get_profile_mfa_serial()
                if not self.region:
                    self._get_profile_region()
                if not self.output:
                    self._get_profile_output()
            else:
                self.create_profile()

    def sts_session_token(
        self,
        token_code: str,
    ) -> Optional[str]:
        """Return the STS session token for the profile and MFA serial ARN."""
        profile = self.cmd_arg_profile()
        if self.mfa_serial_arn is not None:
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("sts")
            cmd.append("get-session-token")
            cmd.append("--serial-number")
            cmd.append(self.mfa_serial_arn)
            cmd.append("--token-code")
            cmd.append(token_code)
            cmd.append("--duration-seconds")
            cmd.append(str(self.session_duration_seconds))
            try:
                cmd_output, _, _ = self._sys.run(cmd=cmd)
                if isinstance(cmd_output, str):
                    return cmd_output.rstrip()
            except OSError as exc:
                hankai.lib.ErrorExit(
                    env=self.env,
                    max_exceptions=1,
                    logenv=self.logenv,
                ).exception_handler(exception=exc)

        return None

    def cmd_arg_profile(self) -> List[str]:
        """Return the AWS CLI command line argument if attribute profile
        defined. e.g --profile devprofile. For use in AWS CLI commands.
        """
        arg: List[str] = []
        if self.profile:
            arg.append("--profile")
            arg.append(self.profile)

        return arg

    def cmd_arg_region(self) -> List[str]:
        """Return the AWS CLI command line argument if attribute profile
        defined. e.g --region us-east-1. For use in AWS CLI commands.
        """
        arg: List[str] = []
        if self.region:
            arg.append("--region")
            arg.append(self.region)

        return arg

    def create_profile(self) -> None:
        """Create a new AWS profile."""
        if not self.profile or not self.access_key_id or not self.secret_access_key:
            raise ValueError(
                "AWS Environment [profile], [access_key_id] and "
                "[secret_access_key] are required."
            )
        if self.profile_exists():
            raise AssertionError(f"AWS profile [{self.profile}] exists.")
        profile = self.cmd_arg_profile()
        cmd = (
            "aws "
            + " ".join(profile)
            + " configure "
            + (
                "<< EOF\n"
                f"{self.access_key_id}\n"
                f"{self.secret_access_key}\n"
                f"\n"
                f"\n"
                "EOF"
            )
        )
        self._sys.run(cmd=cmd, shell=True)
        self.set_profile_access_key_id()
        self.set_profile_secret_access_key()
        self.set_profile_session_token()
        self.set_profile_mfa_serial()
        self.set_profile_region()
        self.set_profile_output()

    def profile_exists(self) -> bool:
        """Check if the profile exists."""
        cmd: List[str] = [
            "aws",
            "configure",
            "get",
            f"{self.profile}.aws_access_key_id",
        ]
        try:
            _, _, returncode = self._sys.run(cmd=cmd)
            if returncode == 0:
                return True
        except OSError:
            pass

        return False

    def _get_profile_access_key_id(self) -> None:
        """Get credentials profile aws_access_key_id."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("aws_access_key_id")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.access_key_id = cmd_output.rstrip()
        except OSError:
            pass

    def set_profile_access_key_id(self) -> None:
        """Set credentials profile aws_access_key_id."""
        if self.access_key_id:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("aws_access_key_id")
            cmd.append(self.access_key_id)
            self._sys.run(cmd=cmd)

    def _get_profile_secret_access_key(self) -> None:
        """Get credentials profile aws_secret_access_key."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("aws_secret_access_key")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.secret_access_key = cmd_output.rstrip()
        except OSError:
            pass

    def set_profile_secret_access_key(self) -> None:
        """Set credentials profile aws_secret_access_key."""
        if self.secret_access_key:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("aws_secret_access_key")
            cmd.append(self.secret_access_key)
            self._sys.run(cmd=cmd)

    def _get_profile_session_token(self) -> None:
        """Get credentials profile session_token."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("session_token")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.session_token = cmd_output.rstrip()
        except OSError:
            pass

    def set_profile_session_token(self) -> None:
        """Set credentials profile session_token."""
        if self.session_token:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("session_token")
            cmd.append(self.session_token)
            self._sys.run(cmd=cmd)

    def _get_profile_mfa_serial(self) -> None:
        """Get credentials profile mfa_serial."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("mfa_serial")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.mfa_serial_arn = cmd_output.rstrip()
        except OSError:
            pass

    def set_profile_mfa_serial(self) -> None:
        """Set credentials profile MFA serial ARN."""
        if self.mfa_serial_arn:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("mfa_serial")
            cmd.append(self.mfa_serial_arn)
            self._sys.run(cmd=cmd)

    def _get_profile_region(self) -> None:
        """Get credentials profile region."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("region")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.region = cmd_output.rstrip()
        except OSError:
            pass

    def set_profile_region(self) -> None:
        """Set config profile region."""
        if self.region:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("region")
            cmd.append(self.region)
            self._sys.run(cmd=cmd)

    def _get_profile_output(self) -> None:
        """Get credentials profile output."""
        profile = self.cmd_arg_profile()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        cmd.append("configure")
        cmd.append("get")
        cmd.append("output")
        try:
            cmd_output, _, _ = self._sys.run(cmd=cmd)
            if isinstance(cmd_output, str):
                self.output = ProfileOutput.member_by(member=cmd_output.rstrip())
        except OSError:
            pass

    def set_profile_output(self) -> None:
        """Set config profile output type."""
        if self.output:
            profile = self.cmd_arg_profile()
            cmd: List[str] = []
            cmd.append("aws")
            if profile:
                cmd.append(profile[0])
                cmd.append(profile[1])
            cmd.append("configure")
            cmd.append("set")
            cmd.append("output")
            cmd.append(str(self.output))
            self._sys.run(cmd=cmd)

    @staticmethod
    def renew_profile_session(
        token_code: str,
        mfa_env: Environment,
        session_env: Environment,
    ) -> None:
        """Configure the session profile for IAM accounts with MFA enabled and
        enforced by policy.
        """
        if not mfa_env.mfa_serial_arn:
            raise ValueError(f"AWS profile [{mfa_env.profile}] requires an mfa_serial.")

        session_token: Optional[str] = mfa_env.sts_session_token(token_code=token_code)

        if not session_token:
            raise ValueError(
                f"AWS session profile [{session_env.profile}] was unable to "
                "acquire an STS session token."
            )

        credentials: Dict[str, Any] = json.loads(session_token)
        session_env.access_key_id = credentials["Credentials"]["AccessKeyId"]
        session_env.secret_access_key = credentials["Credentials"]["SecretAccessKey"]
        session_env.session_token = credentials["Credentials"]["SessionToken"]

        session_env.set_profile_access_key_id()
        session_env.set_profile_secret_access_key()
        session_env.set_profile_session_token()
        session_env.set_profile_region()
