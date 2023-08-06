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
"""Argparse for CodeArtifactEnvSetup."""
import argparse
import textwrap
from argparse import Namespace, RawTextHelpFormatter

import hankai.lib


class CodeArtifactEnvSetupArgparse:
    """Argparse for ECRPushPull."""

    @staticmethod
    def argparse() -> Namespace:
        """Argpase the command line options."""
        description = """\
            Setup the Python environment to access AWS CodeArtifact.

            This utility will get AWS CodeArtifact authorization token and set
            ENV variable CODEARTIFACT_AUTH_TOKEN. It will also set the ENV
            variable PANTS_PYTHON_REPOS_INDEXES with the AWS CodeArtifact domain
            PyPi URL. You must be authenticated with AWS.
            """
        parser = argparse.ArgumentParser(
            description=textwrap.dedent(description),
            formatter_class=RawTextHelpFormatter,
        )
        parser.add_argument(
            "--domain",
            type=str,
            required=True,
            help="AWS CodeArtifact domain. Required.",
        )
        parser.add_argument(
            "--repository",
            type=str,
            required=True,
            help="AWS CodeArtifact repository name. Required.",
        )
        parser.add_argument(
            "--domain-owner",
            type=str,
            required=False,
            help="AWS CodeArtifact domain owner.",
        )
        parser.add_argument(
            "--aws-profile",
            type=str,
            required=False,
            help="AWS credentials profile to get the CodeArtifact authorization token.",
        )
        parser.add_argument(
            "--aws-region",
            type=str,
            required=False,
            help="AWS default region for the session profile.",
        )
        parser.add_argument(
            "--log-level",
            type=str,
            required=False,
            default="info",
            help=(
                f"Loguru level. One of {hankai.lib.LoguruLevel.members()} "
                f"Default [{hankai.lib.LogEnv().log_level}]."
            ),
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

        return parser.parse_args()
