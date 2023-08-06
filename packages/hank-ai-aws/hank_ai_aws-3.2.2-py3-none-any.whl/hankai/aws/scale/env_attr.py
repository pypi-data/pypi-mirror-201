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
"""Convenience EnvEnum for common/shared AWS scaling."""

import hankai.lib


class ScaleEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and Scale attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SCALE_EXPECTED_SCALING_SECONDS = "expected_scaling_seconds"
    HANK_SCALE_DISABLE_ADJUSTMENT = "disable_adjustment"
    HANK_SCALE_DISABLE_ADJUSTMENT_DELAY_SECONDS = "disable_adjustment_delay_seconds"


class ScaleECSEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and ScaleECS attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SCALE_ECS_MIN_DESIRED_TASKS = "min_desired_tasks"
    HANK_SCALE_ECS_MAX_DESIRED_TASKS = "max_desired_tasks"


class ScaleEC2ASGAndECSEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and ScaleEC2ASGAndECS attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SCALE_EC2ASG_AND_ECS_TASKS_PER_INSTANCE = "ecs_tasks_per_ec2asg_instance"
    HANK_SCALE_EC2ASG_AND_ECS_ACTION_TIMEOUT_SECONDS = "action_timeout_seconds"
