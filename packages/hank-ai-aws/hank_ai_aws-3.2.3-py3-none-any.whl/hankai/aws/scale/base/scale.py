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
"""Classes for Scales."""
from abc import ABC, abstractmethod
from typing import Any, Optional

from pendulum.datetime import DateTime

import hankai.lib


class Scale(ABC):
    """Scale base class."""

    @staticmethod
    def elapsed_scaling_seconds(start: DateTime) -> float:
        """Calculate the scaling action elapsed time."""
        return hankai.lib.Util.elapsed_seconds(start=start)

    @abstractmethod
    def ready_to_scale(self, state: Any) -> bool:
        """Ready to scale based on state."""
        raise NotImplementedError()

    @abstractmethod
    def predict_capacity(self) -> Optional[int]:
        """Predict the capacity scale."""
        raise NotImplementedError()

    @abstractmethod
    def adjust_capacity(self) -> None:
        """Adjust the capacity based on the predicted capacity scale."""
        raise NotImplementedError()
