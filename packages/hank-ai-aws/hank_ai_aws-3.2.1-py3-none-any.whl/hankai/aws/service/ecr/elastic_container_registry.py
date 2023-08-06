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
"""Manage AWS Elastic Container Registry."""
from dataclasses import dataclass
from typing import List, Optional, Set, Type

import hankai.lib
from hankai.aws.sdk import Environment


class ElasticContainerRegistryEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and ElasticContainerRegistry attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_ECR_REGISTRY_URI = "registry_uri"
    HANK_ECR_PUSH_ALL_TAGS = "push_all_tags"


@dataclass
class ElasticContainerRegistry:  # pylint: disable=too-many-instance-attributes
    """Class to manage Elastic Container Registry (ECR).
    ECR repository_arn: <aws_account_id>.dkr.ecr.<region>.amazonaws.com

    hankai.lib.Sys is instantiated with this classes sys_env.
    i.e. hankai.lib.Sys()

    If you need to override any attributes for hankai.lib.Sys() examine that
    class and add a member to the EnvEnum that is passed into this
    classes [sys_env].

    https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html
    """

    environment: Environment
    registry_uri: str
    logenv: hankai.lib.LogEnv
    push_all_tags: bool = True
    env: Optional[Type[hankai.lib.EnvEnum]] = None
    sys_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            hankai.lib.LogEnv().env_supersede(clz=self, env_type=self.env)
        self._sys = hankai.lib.Sys(logenv=self.logenv)
        if self._sys.get_aws_cli_version() != 2:
            raise AssertionError("AWS CLI v2 is required.")
        self._docker_logged_in = False

    def docker_login(self) -> None:
        """Login Docker with AWS ECR."""
        profile_list = self.environment.cmd_arg_profile()
        region_list = self.environment.cmd_arg_region()
        profile = ""
        region = ""
        if profile_list:
            profile = " " + " ".join(self.environment.cmd_arg_profile()) + " "
        if region_list:
            region = " " + " ".join(self.environment.cmd_arg_region()) + " "

        cmd = (
            f"aws{profile}{region} ecr get-login-password | "
            f"docker login --username AWS --password-stdin {self.registry_uri}"
        )
        _, stderr, responsecode = self._sys.run(cmd=cmd, shell=True)
        if responsecode == 0:
            self._docker_logged_in = True
        else:
            raise AssertionError(
                "Unable to perform docker login with ECR login password. "
                f"Command failed with response code [{responsecode}] and "
                f"error message [{str(stderr)}]."
            )

    def tags(self, repository: str) -> Set[str]:
        """Get all tags for the given repository."""
        all_tags: Set[str] = set()
        cmd: List[str] = []
        cmd.append("docker")
        cmd.append("images")
        cmd.append("--filter")
        cmd.append("dangling=false")
        cmd.append("--format")
        cmd.append("'{{.Tag}}'")
        cmd.append(repository)
        cmd_output, _, _ = self._sys.run(cmd)
        if cmd_output and isinstance(cmd_output, str):
            all_tags = set(cmd_output.strip().splitlines())

        return all_tags

    def tag(
        self,
        repository: str,
        tag: str = "latest",
        new_tags: Optional[Set[str]] = None,
        ecr_repository: Optional[str] = None,
    ) -> None:
        """Tag the local Docker image with tags that don't exist. If ecr_repository
        is None the default ecr_repository is registry_uri/image.
        """
        if not ecr_repository:
            ecr_repository = f"{self.registry_uri}/{repository}"

        all_existing_tags = self.tags(repository=repository)

        if tag not in all_existing_tags:
            raise ValueError(
                f"Docker image repository [{repository}] tag [{tag}] does not exist."
            )

        cmd: List[str] = []
        if new_tags:
            for new_tag in new_tags:
                if new_tag not in all_existing_tags:
                    cmd = []
                    cmd.append("docker")
                    cmd.append("tag")
                    cmd.append(f"{repository}:{tag}")
                    cmd.append(f"{repository}:{new_tag}")
                    self._sys.run(cmd)

            if self.push_all_tags:
                all_existing_tags.update(new_tags)
            else:
                all_existing_tags = new_tags

        for existing_tag in all_existing_tags:
            cmd = []
            cmd.append("docker")
            cmd.append("tag")
            cmd.append(f"{repository}:{existing_tag}")
            cmd.append(f"{ecr_repository}:{existing_tag}")
            self._sys.run(cmd)

    def push(
        self,
        repository: str,
        tags: Optional[Set[str]] = None,
        remove_repository: bool = True,
    ) -> None:
        """Push Docker image to AWS ECR logged in registry URI. If
        push_all_tags is True, [tags] is optional. If it is False
        [tags] are required.
        """
        if not self.push_all_tags and not tags:
            raise ValueError("Argument [tags] is required when not pushing all tags.")

        if not self._docker_logged_in:
            self.docker_login()

        rm_tags: Set[str] = set()
        cmd: List[str] = []
        if self.push_all_tags:
            cmd.append("docker")
            cmd.append("push")
            cmd.append("--all-tags")
            cmd.append(repository)
            self._sys.run(cmd)
            rm_tags = self.tags(repository=repository)
        elif tags is not None:
            rm_tags = tags
            for tag in tags:
                cmd = []
                cmd.append("docker")
                cmd.append("push")
                cmd.append(f"{repository}:{tag}")
                self._sys.run(cmd)

        if remove_repository:
            for tag in rm_tags:
                cmd = []
                cmd.append("docker")
                cmd.append("image")
                cmd.append("rm")
                cmd.append("-f")
                cmd.append(f"{repository}:{tag}")
                self._sys.run(cmd)

    def pull(self, repository: str, tags: Optional[Set[str]] = None) -> None:
        """Pull Docker image from AWS ECR logged in registry URI. The default
        for [tags] is "latest".
        """
        if not tags:
            tags = {"latest"}

        if not self._docker_logged_in:
            self.docker_login()

        for tag in tags:
            cmd = f"docker pull '{repository}:{tag}'"
            self._sys.run(cmd)
