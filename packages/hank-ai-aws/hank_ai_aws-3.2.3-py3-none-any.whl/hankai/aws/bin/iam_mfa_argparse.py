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
"""Argparse for IAMMfaConfig."""
import argparse
import os
import textwrap
from argparse import Namespace, RawTextHelpFormatter

import hankai.aws
import hankai.lib


class IAMMfaConfigArgparse:
    """Argparse for IAMMfaConfig."""

    @staticmethod
    def argparse() -> Namespace:
        """Argpase the command line options."""
        this_file = os.path.basename(__file__)
        description = f"""\
                This utility will get session credentials for AWS MFA enabled IAM
                accounts and update the users AWS-CLI configuration to set the
                aws_access_key_id, aws_secret_access_key, session_token and
                aws_default_region for subsequent AWS-CLI invocations.

                This is helpful for AWS IAM accounts which have MFA enforced by
                policy.

                The AWS IAM user must have an active Security Credential AccessKey
                which is already configured in the users AWS-CLI credentials file
                or environment variables.

                Subsequent AWS-CLI commands must be executed with the MFA profile
                containting the session_token.

                NOTE! Only supports AWS IAM username accounts and virtual MFA!

                Gets the MFA ARN for the profile and if the token code is valid
                will set the aws_access_key_id, aws_secret_access_key and
                session_token in the users AWS-CLI credentials file for the
                given session profile name.

                NOTE! The MFA profile may not be the session profile. AWS
                credentials will overwrite the aws_access_key_id and
                aws_secret_access_key with new information.

                It is suggested to use a session profile other than 'default'. By
                using a non default profile you can be authenticated to say both
                PRD and SDLC-DEV at the same time and use the --profile option
                with the aws cli command to target the specific environment.

                --------------------------------------------------------------------
                Example using the 'default' profile:

                {this_file} --mfa-profile hank-ai-sdlc-mfa --session-profile default
                    --token ######

                ~/.aws/config
                [hank-ai-mfa]
                region = us-east-1
                output = json

                [hank-ai-session]
                region = us-east-1
                output = json

                [hank-ai-sdlc-mfa]
                region = us-east-1
                output = json

                [hank-ai-sdlc-session]
                region = us-east-1
                output = json

                [default]
                region = us-east-1
                output = json

                Example ~/.aws/credentials
                [hank-ai-mfa]
                mfa_serial = arn:aws:iam::9###########:mfa/first.lastname
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################

                [hank-ai-session]

                [hank-ai-sdlc-mfa]
                mfa_serial = arn:aws:iam::5###########:mfa/first.lastname
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################

                [hank-ai-sdlc-session]

                [default]
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################
                session_token = #########...

                --------------------------------------------------------------------
                Example using a 'session' profile:

                {this_file} --mfa-profile hank-ai-sdlc-mfa --session-profile
                    hank-ai-sdlc-session --token ######

                ~/.aws/config
                [hank-ai-mfa]
                region = us-east-1
                output = json

                [hank-ai-session]
                region = us-east-1
                output = json

                [hank-ai-sdlc-mfa]
                region = us-east-1
                output = json

                [hank-ai-sdlc-session]
                region = us-east-1
                output = json

                [default]
                region = us-east-1
                output = json

                Example ~/.aws/credentials
                [hank-ai-mfa]
                mfa_serial = arn:aws:iam::9###########:mfa/first.lastname
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################

                [hank-ai-session]

                [hank-ai-sdlc-mfa]
                mfa_serial = arn:aws:iam::5###########:mfa/first.lastname
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################

                [hank-ai-sdlc-session]
                aws_access_key_id = A###################
                aws_secret_access_key = ########################################
                session_token = #########...

                [default]
                """
        parser = argparse.ArgumentParser(
            description=textwrap.dedent(description),
            formatter_class=RawTextHelpFormatter,
        )
        parser.add_argument(
            "--token", type=str, required=False, help="MFA token ######"
        )
        parser.add_argument(
            "--session-profile",
            type=str,
            required=True,
            help="AWS credentials profile to assign the session token. Required.",
        )
        parser.add_argument(
            "--duration-seconds",
            type=int,
            required=False,
            default=hankai.aws.Environment.session_duration_seconds,
            help=(
                "AWS session token duration in seconds. Default "
                f"[{hankai.aws.Environment.session_duration_seconds}]."
            ),
        )

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--mfa-profile",
            type=str,
            help=(
                "AWS credentials profile that has a defined mfa_serial ARN."
                "Mutally exclusive of --mfa-serial-arn. --mfa-profile or "
                "--mfa-serial-arn are required."
            ),
        )
        group.add_argument(
            "--mfa-serial-arn",
            type=str,
            help=(
                "AWS IAM user's MFA Serial ARN if there are no profiles with "
                "'mfa_serial' defined. Mutually exclusive of --mfa-profile. "
                "--mfa-profile or --mfa-serial-arn are required."
            ),
        )

        parser.add_argument(
            "--aws-region",
            type=str,
            required=False,
            help=("AWS default region for the session profile."),
        )
        parser.add_argument(
            "--verbosity",
            type=int,
            required=False,
            default=0,
            help=(
                "Verbosity. Integer greater than equal or to zero. Default "
                f"[{hankai.lib.LogEnv().verbosity}]."
            ),
        )
        parser.add_argument(
            "--log-level",
            type=str,
            required=False,
            default="info",
            help=(
                f"Loguru level. One of {hankai.lib.LoguruLevel.members()} "
                f"Default [{hankai.lib.LogEnv().log_level}]."  # pylint: disable=line-too-long
            ),
        )

        return parser.parse_args()
