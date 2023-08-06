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
"""Argparse for ECRPushPull."""
import argparse
import textwrap
from argparse import Namespace, RawTextHelpFormatter

import hankai.aws
import hankai.lib


class ECRPushPullArgparse:
    """Argparse for ECRPushPull."""

    @staticmethod
    def argparse() -> Namespace:
        """Argpase the command line options."""
        description = """\
            Push a local Docker image with a list of optional tags, tag the
            local Docker image and push to the AWS ECR registry.

            Pull a remote AWS ECR Docker image.

            Command line option --aws-ecr-registry-uri,--aws-ecr-tags and
            --aws-profile supersede all their ENV declarations.
            """
        parser = argparse.ArgumentParser(
            description=textwrap.dedent(description),
            formatter_class=RawTextHelpFormatter,
        )

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--push",
            action="store_true",
            help=(
                "Request push of local Docker image to AWS ECR registry. "
                "Mutually exclusive of --pull. --push or --pull is required."
            ),
        )
        group.add_argument(
            "--pull",
            action="store_true",
            help=(
                "Request pull of remote Docker image from AWS ECR registry. "
                "Mutually exclusive of --push. --push or --pull is required."
            ),
        )

        parser.add_argument(
            "--aws-ecr-registry-uri",
            type=str,
            required=True,
            help="AWS ECR registry URI. Required.",
        )
        parser.add_argument(
            "--repository",
            type=str,
            required=False,
            help="Local Docker repository image to push. Required for --push.",
        )
        parser.add_argument(
            "--ecr-repository",
            type=str,
            required=False,
            help=(
                "AWS ECR repository to push to or pull from. "
                "Default [aws-ecr-registry-uri/repository]. Required for --pull."
            ),
        )
        parser.add_argument(
            "--tags",
            nargs="+",
            required=False,
            default=["latest"],
            help=(
                "Docker repository image tag list to push or pull. "
                "! IMPORTANT: The first tag must currently exist. "
                "e.g. --tags latest A B C D. Default [latest]."
            ),
        )
        parser.add_argument(
            "--ecr-keep-repository",
            action="store_true",
            default=False,
            help=("Keep local repository by tags. Default[False]."),
        )
        parser.add_argument(
            "--aws-profile",
            type=str,
            required=False,
            help=(
                "AWS credentials profile to get the ECR authorization for "
                "docker login."
            ),
        )
        parser.add_argument(
            "--aws-region",
            type=str,
            required=False,
            help=("AWS region to get the ECR authorization for docker login."),
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
