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

"""Utility to tag a local Docker image and push to AWS ECR registry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Type

import hankai.aws
import hankai.lib

from .ecr_docker_argparse import ECRPushPullArgparse


class ECRPushPullEnum(hankai.lib.MemberValue):
    """True|False"""

    PUSH = "push"
    PULL = "pull"


@dataclass
class ECRPushPull:  # pylint: disable=too-many-instance-attributes
    """DockerECRPush class to parse args and tag a local Docker image and
    then push or pull from an AWS ECR registry.

    Command line execution ignores any and all EnvEnum.
    Non command line execution ignores and and all command line options.

    [repository] is required for AWS ECR Push.
    [argparse] should only be True for command line execution.
    """

    ecr: hankai.aws.ElasticContainerRegistry
    logenv: hankai.lib.LogEnv
    repository: Optional[str] = None
    ecr_repository: Optional[str] = None
    argparse: bool = False
    tags: Optional[Set[str]] = None
    existing_tag: str = "latest"
    action: hankai.lib.Member = ECRPushPullEnum.PUSH
    ecr_keep_repository: bool = False
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.argparse:
            self._set_from_args()
        elif self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)
            if self.action == ECRPushPullEnum.PUSH and not self.repository:
                raise AssertionError("Push requires [repository].")

            if not self.ecr_repository:
                self.ecr_repository = f"{self.ecr.registry_uri}/{self.repository}"

        self.ecr_remove_repository = True

    def _set_from_args(self) -> None:
        """Set attributes from argparse."""
        args = ECRPushPullArgparse().argparse()

        if args.log_level:
            level = hankai.lib.LoguruLevel.member_by(args.log_level)
            if level:
                self.logenv.set_log_level(level=level)
        if args.verbosity:
            self.logenv.set_verbosity(level=args.verbosity)

        if args.tags:
            self.existing_tag: str = args.tags[0]
            self.tags = set(args.tags)

        self.ecr.environment = hankai.aws.Environment(
            profile=args.aws_profile,
            region=args.aws_region,
            logenv=self.logenv,
        )
        self.ecr.registry_uri = args.aws_ecr_registry_uri

        if args.ecr_repository:
            self.ecr_repository = args.ecr_repository

        if args.push:
            self.action = ECRPushPullEnum.PUSH
            if not args.repository:
                raise AssertionError("Push requires [--repository].")

            if not self.ecr_repository:
                self.ecr_repository = f"{self.ecr.registry_uri}/{args.repository}"

            self.ecr.tag(
                repository=args.repository,
                tag=self.existing_tag,
                new_tags=self.tags,
                ecr_repository=self.ecr_repository,
            )

            if args.ecr_keep_repository:
                self.ecr_remove_repository = False

        if args.pull:
            self.action = ECRPushPullEnum.PULL
            if not args.ecr_repository:
                raise ValueError("Pull requires [--ecr-repository].")
            self.ecr_repository = args.ecr_repository

    def execute(self) -> None:
        """Execute AWS ECR push/pull."""

        if not self.ecr_repository:
            raise ValueError("Argument [ecr_repository] is required.")

        if self.action == ECRPushPullEnum.PUSH:
            if not self.repository:
                raise ValueError("Argument [repository] is required.")

            self.ecr.tag(
                repository=self.repository,
                tag=self.existing_tag,
                new_tags=self.tags,
                ecr_repository=self.ecr_repository,
            )

            if self.ecr_keep_repository:
                self.ecr_remove_repository = False

            self.ecr.push(
                repository=self.ecr_repository,  # __post_init__ sets if not
                tags=self.tags,
                remove_repository=self.ecr_remove_repository,
            )

        if self.action == ECRPushPullEnum.PULL:
            self.ecr.pull(
                repository=self.ecr_repository,  # __post_init__ sets if not
                tags=self.tags,
            )


def main():
    """Begin AWS ECR push/pull. This is *only* intended for command line
    execution.
    """
    logenv = hankai.lib.LogEnv()
    ECRPushPull(
        ecr=hankai.aws.ElasticContainerRegistry(
            environment=hankai.aws.Environment(logenv=logenv),
            registry_uri="",
            logenv=logenv,
        ),
        repository="",
        logenv=logenv,
        argparse=True,
    ).execute()
