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
"""Calculating scaling capacity based on SQS."""
from dataclasses import dataclass
from typing import Optional, Type

import hankai.lib


class SQSScaleEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and SQSScale attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SQS_SCALE_BLOCK_SIZE = "block_size"


@dataclass
class SQSScale:
    """SQS scale calculations."""

    logenv: hankai.lib.LogEnv
    block_size: int = 1
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.block_size = max(self.block_size, 1)

    def infer_capacity(  # pylint: disable=too-many-branches
        self, length: int, min_instances: int = 0, max_instances: int = 0
    ) -> int:
        """Infer desired capacity based on the scaling block size an the SQS
        queue length.
        """
        length = max(length, 0)
        min_instances = max(min_instances, 0)
        max_instances = max(max_instances, 0)
        if min_instances > max_instances:
            raise ValueError(
                "Argument [min_instances] must be less than or equal to "
                "[max_instances]."
            )

        if min_instances == max_instances:
            self.logenv.logger.warning("Minimum instances equals maximum instances.")

        if min_instances == 0 and max_instances == 0:
            self.logenv.logger.warning(
                "Minimum instances and maximum instances are both zero. There "
                "is nothing to infer; capacity [0]."
            )
            return 0

        # Calculate the queue desired capacity
        capacity = -1
        if length > self.block_size:
            capacity = int(length / self.block_size)
        elif length > 0:
            capacity = 1
        elif length <= 0:
            capacity = 0

        if capacity > 0 or self.logenv.verbosity > 0:
            self.logenv.logger.info(
                "Queue load length [{}] and block size [{}] infers a capacity "
                "of [{}] instance(s) from the allowed minimum [{}] instances "
                "and maximum [{}] instances.",
                length,
                self.block_size,
                capacity,
                min_instances,
                max_instances,
            )

        if capacity > max_instances:
            if self.logenv.verbosity > 0:
                self.logenv.logger.warning(
                    "Inferred desired capacity limited to AWS EC2 Auto Scaling "
                    "Group maximum instances [{}]; requested [{}] instances.",
                    max_instances,
                    capacity,
                )

            return max_instances

        if capacity < min_instances:
            if self.logenv.verbosity > 0:
                self.logenv.logger.warning(
                    "Inferred desired capacity limited to AWS EC2 Auto Scaling "
                    "Group minimum instances [{}]; requested [{}] instances.",
                    min_instances,
                    capacity,
                )

            return min_instances

        return capacity
