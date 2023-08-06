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
"""Manage AWS CodeArtifact."""
import os
from dataclasses import dataclass
from typing import List, Optional, Type

import hankai.lib
from hankai.aws.sdk import Environment


class CodeArtifactEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and CodeArtifactEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_CODEARTIFACT_REPOSITORY = "repository"
    HANK_CODEARTIFACT_DOMAIN = "domain"
    HANK_CODEARTIFACT_DOMAIN_OWNER = "domain_owner"
    HANK_CODEARTIFACT_FORMAT = "format"


@dataclass
class CodeArtifact:  # pylint: disable=too-many-instance-attributes
    """Class for AWS CodeArtifact.

    https://docs.aws.amazon.com/cli/latest/reference/codeartifact/login.html
    """

    environment: Environment
    repository: str
    domain: str
    logenv: hankai.lib.LogEnv
    domain_owner: Optional[str] = None
    format: str = "pypi"
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            hankai.lib.LogEnv().env_supersede(clz=self, env_type=self.env)
        self._sys = hankai.lib.Sys(logenv=self.logenv)
        if self._sys.get_aws_cli_version() != 2:
            raise AssertionError("AWS CLI v2 is required.")
        self.__auth_token = ""
        self.__repository_url = ""

    def cmd_arg_domain_owner(self) -> List[str]:
        """Return the command line argument for AWS CLI --profile."""
        arg: List[str] = []
        if self.domain_owner:
            arg.append("--domain-owner")
            arg.append(self.domain_owner)

        return arg

    def get_authorization_token(self) -> str:  # pylint: disable=too-many-statements
        """Get AWS CodeArtifact authorization token and set ENV variable
        CODEARTIFACT_AUTH_TOKEN for pip and TWINE_USERNAME, TWINE_PASSWORD and
        TWINE_REPOSITORY_URL for twine. Returns the authorization token.
        """

        pip = "CODEARTIFACT_AUTH_TOKEN"
        twine_username = "TWINE_USERNAME"
        twine_password = "TWINE_PASSWORD"
        twine_repo_url = "TWINE_REPOSITORY_URL"

        profile = self.environment.cmd_arg_profile()
        region = self.environment.cmd_arg_region()
        domain_owner = self.cmd_arg_domain_owner()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        if region:
            cmd.append(region[0])
            cmd.append(region[1])
        cmd.append("codeartifact")
        cmd.append("get-authorization-token")
        cmd.append("--domain")
        cmd.append(self.domain)
        if domain_owner:
            cmd.append(domain_owner[0])
            cmd.append(domain_owner[1])
        cmd.append("--query")
        cmd.append("authorizationToken")
        cmd.append("--output")
        cmd.append("text")

        token, *_ = self._sys.run(cmd=cmd)
        if token and isinstance(token, str):
            self.__auth_token = token.strip()
            os.environ[pip] = self.__auth_token
            os.environ[twine_username] = "aws"
            os.environ[twine_password] = self.__auth_token
            print(f'export {pip}=("{os.environ[pip]}")')
            print(f'export {twine_username}=("{os.environ[twine_username]}")')
            print(f'export {twine_repo_url}=("{os.environ[twine_repo_url]}")')

        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        if region:
            cmd.append(region[0])
            cmd.append(region[1])
        cmd.append("codeartifact")
        cmd.append("get-repository-endpoint")
        cmd.append("--domain")
        cmd.append(self.domain)
        if domain_owner:
            cmd.append(domain_owner[0])
            cmd.append(domain_owner[1])
        cmd.append("--repository")
        cmd.append(self.repository)
        cmd.append("--query")
        cmd.append("repositoryEndpoint")
        cmd.append("--output")
        cmd.append("text")

        url, *_ = self._sys.run(cmd=cmd)
        if url and isinstance(url, str):
            self.__repository_url = url.strip()
            os.environ[twine_repo_url] = self.__repository_url
            print(f'export {twine_repo_url}=("{os.environ[twine_repo_url]}")')

        return self.__auth_token

    def get_pants_python_repos_indexes(
        self, aws_region: str = "us-east-1"
    ) -> List[str]:
        """Get the Pants Python repos indexes for AWS CodeArtifact and
        set ENV variable PANTS_PYTHON_REPOS_INDEXES.
        """
        env_var = "PANTS_PYTHON_REPOS_INDEXES"
        if not self.__auth_token:
            self.get_authorization_token()
        indexes: List[str] = []
        if self.__auth_token:
            index = (
                f"https://aws:{self.__auth_token}@"
                f"{self.domain}-"
                f"{self.domain_owner}.d.codeartifact."
                f"{aws_region}.amazonaws.com/pypi/"
                f"{self.repository}/simple/"
            )
            indexes.append(index)

        if indexes:
            os.environ[env_var] = f"+{indexes}"
            print(f'export {env_var}=("{os.environ[env_var]}")')

        return indexes

    def python_login_pip(self) -> None:
        """Login to the AWS CodeArtifact repository for pip."""
        profile = self.environment.cmd_arg_profile()
        region = self.environment.cmd_arg_region()
        domain_owner = self.cmd_arg_domain_owner()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        if region:
            cmd.append(region[0])
            cmd.append(region[1])
        cmd.append("codeartifact")
        cmd.append("login")
        cmd.append("--tool")
        cmd.append("pip")
        cmd.append("--repository")
        cmd.append(self.repository)
        cmd.append("--domain")
        cmd.append(self.domain)
        if domain_owner:
            cmd.append(domain_owner[0])
            cmd.append(domain_owner[1])
        self._sys.run(cmd=cmd)

    def python_login_twine(self) -> None:
        """Login to the AWS CodeArtifact repository for twine."""
        profile = self.environment.cmd_arg_profile()
        region = self.environment.cmd_arg_region()
        domain_owner = self.cmd_arg_domain_owner()
        cmd: List[str] = []
        cmd.append("aws")
        if profile:
            cmd.append(profile[0])
            cmd.append(profile[1])
        if region:
            cmd.append(region[0])
            cmd.append(region[1])
        cmd.append("codeartifact")
        cmd.append("login")
        cmd.append("--tool")
        cmd.append("twine")
        cmd.append("--repository")
        cmd.append(self.repository)
        cmd.append("--domain")
        cmd.append(self.domain)
        if domain_owner:
            cmd.append(domain_owner[0])
            cmd.append(domain_owner[1])
        self._sys.run(cmd=cmd)
