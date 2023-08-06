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
"""Hank AI AWS Service initialization."""
from hankai.aws.service.codeartifact.codeartifact import *
from hankai.aws.service.ec2.auto_scaling import *
from hankai.aws.service.ecr.elastic_container_registry import *
from hankai.aws.service.ecs.elastic_container_service import *
from hankai.aws.service.s3.simple_storage_service import *
from hankai.aws.service.sqs.scale import *
from hankai.aws.service.sqs.simple_queue_service import *

__all__ = [
    "CodeArtifact",
    "CodeArtifactEnv",
    #
    "SimpleQueueService",
    "SimpleQueueServiceEnv",
    #
    "SimpleStorageService",
    "SimpleStorageServiceEnv",
    #
    "ElasticContainerRegistry",
    "ElasticContainerRegistryEnv",
    #
    "ElasticContainerService",
    "ElasticContainerServiceEnv",
    "ElasticContainerServiceState",
    #
    "EC2AutoScalingGroup",
    "EC2AutoScalingGroupEnv",
    #
    "SQSScale",
    "SQSScaleEnv",
]
