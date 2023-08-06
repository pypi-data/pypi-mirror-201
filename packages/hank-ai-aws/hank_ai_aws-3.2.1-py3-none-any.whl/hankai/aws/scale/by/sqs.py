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
"""Manage AWS ASG & ECS Scale by SQS queue properties."""
from dataclasses import dataclass
from typing import Tuple

from hankai.aws.service import SimpleQueueService, SQSScale

from ..base.scale_by import ScaleBy


@dataclass
class ScaleBySQS(ScaleBy):
    """Class to monitor AWS SQS queues and provide predictions."""

    sqs: SimpleQueueService
    scale: SQSScale

    def infer_desired_capacity(
        self,
        min_instances: int = 0,
        max_instances: int = 0,
    ) -> Tuple[int, int]:
        """Get the current state and infer the desired capacity from the
        queue length.
        """
        min_instances = max(min_instances, 0)
        max_instances = max(max_instances, 0)

        (
            available_msgs,
            in_flight_msgs,
            delayed_msgs,
        ) = self.sqs.approximate_number_messages()

        queue_length = available_msgs + in_flight_msgs + delayed_msgs

        inferred_desired_capacity = self.scale.infer_capacity(
            length=queue_length,
            min_instances=min_instances,
            max_instances=max_instances,
        )

        return (queue_length, inferred_desired_capacity)
