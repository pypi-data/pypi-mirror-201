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

"""Utility to setup the environment for AWS CodeArtifact and Pants."""
from dataclasses import dataclass
from typing import Optional, Type

import hankai.aws
import hankai.lib

from .codeartifact_env_setup_argparse import CodeArtifactEnvSetupArgparse


@dataclass
class CodeArtifactEnvSetup:
    """CodeArtifactEnvSetup class to parse args and setup the environment
    for AWS CodeArtifact and Python.

    Command line execution ignores any and all EnvEnum.
    Non command line execution ignores and and all command line options.

    [argparse] should only be True for command line execution.
    """

    codeartifact: hankai.aws.CodeArtifact
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
        args = CodeArtifactEnvSetupArgparse().argparse()

        if args.log_level:
            level = hankai.lib.LoguruLevel.member_by(args.log_level)
            if level:
                self.logenv.set_log_level(level=level)
        if args.verbosity:
            self.logenv.set_verbosity(level=args.verbosity)

        self.codeartifact.environment = hankai.aws.Environment(
            profile=args.aws_profile,
            region=args.aws_region,
            logenv=self.logenv,
        )
        self.codeartifact.repository = args.repository
        self.codeartifact.domain = args.domain
        self.codeartifact.domain_owner = args.domain_owner

    def execute(self) -> None:
        """Execute AWS CodeArtifact ENV setup."""
        self.codeartifact.get_authorization_token()
        self.codeartifact.get_pants_python_repos_indexes()
        self.codeartifact.python_login_pip()
        self.codeartifact.python_login_twine()


def main():
    """Begin AWS CodeArtifact environment configuration. This is *only*
    intended for command line execution.
    """
    CodeArtifactEnvSetup(
        codeartifact=hankai.aws.CodeArtifact(
            environment=hankai.aws.Environment(logenv=hankai.lib.LogEnv()),
            repository="",
            domain="",
            logenv=hankai.lib.LogEnv(),
        ),
        logenv=hankai.lib.LogEnv(),
        argparse=True,
    ).execute()
