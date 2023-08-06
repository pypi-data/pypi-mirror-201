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
"""Hank AI AWS initialization."""
from hankai.aws.scale.by.sqs import *
from hankai.aws.scale.composite.ec2asg_ecs_by_sqs import *
from hankai.aws.scale.ec2.asg_by_sqs import *
from hankai.aws.scale.ecs.by_sqs import *
from hankai.aws.scale.env_attr import *
from hankai.aws.sdk.environment import *
from hankai.aws.sdk.servicer import *
from hankai.aws.sdk.session import *
from hankai.aws.service.codeartifact.codeartifact import *
from hankai.aws.service.ec2.auto_scaling import *
from hankai.aws.service.ecr.elastic_container_registry import *
from hankai.aws.service.ecs.elastic_container_service import *
from hankai.aws.service.s3.simple_storage_service import *
from hankai.aws.service.sqs.scale import *
from hankai.aws.service.sqs.simple_queue_service import *

__all__ = [
    "Environment",
    "EnvironmentEnv",
    "ProfileOutput",
    "Servicer",
    "ServiceName",
    "Session",
    #
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
    "ScaleBySQS",
    "ScaleEC2ASGBySQS",
    "ScaleEC2ASGAndECSBySQS",
    "ScaleECSBySQS",
    #
    "ScaleEnv",
    "ScaleECSEnv",
    "ScaleEC2ASGAndECSEnv",
]

__version__ = "3.2.2"
