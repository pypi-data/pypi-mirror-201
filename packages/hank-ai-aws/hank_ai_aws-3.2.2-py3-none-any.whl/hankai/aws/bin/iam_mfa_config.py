#! /usr/bin/env python3
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

"""Utility to update user AWS-CLI credentials and config for AWS MFA enabled IAM
accounts. Excute with --help for details.
https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
"""

from dataclasses import dataclass
from typing import Optional, Type

import hankai.aws
import hankai.lib

from .iam_mfa_argparse import IAMMfaConfigArgparse


@dataclass
class IAMMfaConfig:
    """Utility to set AWS Credentials for MFA protected IAM accounts."""

    token: str
    mfa_env: hankai.aws.Environment
    session_env: hankai.aws.Environment
    logenv: hankai.lib.LogEnv
    argparse: bool = False
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.argparse:
            self._set_from_args()
        elif self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

    def _set_from_args(self) -> None:
        """Set attributes from argparse."""

        args = IAMMfaConfigArgparse.argparse()

        self.token = args.token

        if args.log_level:
            level = hankai.lib.LoguruLevel.member_by(args.log_level)
            if level:
                self.logenv.set_log_level(level=level)
        if args.verbosity:
            self.logenv.set_verbosity(level=args.verbosity)

        self.session_env = hankai.aws.Environment(
            profile=args.session_profile,
            region=args.aws_region,
            logenv=self.logenv,
        )

        self.mfa_env = hankai.aws.Environment(
            profile=args.mfa_profile,
            region=args.aws_region,
            logenv=self.logenv,
        )

        if args.mfa_serial_arn:
            self.mfa_env = hankai.aws.Environment(
                profile=None,
                region=args.aws_region,
                mfa_serial_arn=args.mfa_serial_arn,
                logenv=self.logenv,
            )

        if self.session_env.profile is None:
            raise AssertionError("Unable to locate [session_env] profile.")
        if self.mfa_env.mfa_serial_arn is None:
            raise AssertionError("Unable to locate [mfa_env] profile.")

    def execute(self) -> None:
        """Execute the IAM config."""
        hankai.aws.Environment(logenv=self.logenv).renew_profile_session(
            token_code=self.token,
            mfa_env=self.mfa_env,
            session_env=self.session_env,
        )


def main():
    """Begin AWS IAM MFA Configuration."""
    logenv = hankai.lib.LogEnv()
    IAMMfaConfig(
        token="",
        mfa_env=hankai.aws.Environment(logenv=logenv),
        session_env=hankai.aws.Environment(logenv=logenv),
        logenv=logenv,
        argparse=True,
    ).execute()
