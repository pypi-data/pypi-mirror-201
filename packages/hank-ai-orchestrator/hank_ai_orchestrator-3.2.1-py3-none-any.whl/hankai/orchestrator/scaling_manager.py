#!/usr/bin/env python3
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


# pylint: disable=invalid-name
"""Orchestrator auto scaling managers for auto scaling in/out various AWS
compute resources.
"""
from abc import ABC, abstractmethod

import hankai.aws
import hankai.lib

from .env_attr import (
    EnvironmentEC2ASGEnv,
    EnvironmentECSEnv,
    EnvironmentSQSEnv,
    ServicerEC2ASGEnv,
    ServicerECSEnv,
    ServicerSQSEnv,
)


class ScalingManager(ABC):
    """ScalingManager base class."""

    def __init__(self, logenv: hankai.lib.LogEnv, backoff: hankai.lib.Backoff) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        """Start the scaling manager."""
        raise NotImplementedError()


class ScalingManagerEC2ASGAndECSBySQS(ScalingManager):
    """Orchestrator scaling manager to scale in/out the AWS EC2 Auto Scaling Group
    and the AWS ECS autocoding service based on the AWS SQS queue length.

    Monitor AWS SQS and adjust both the AWS EC2 ASG desired capacity and
    the AWS ECS cluster service desired tasks based on the monitored SQS queue.
    As the queue message depth increases the desired tasks/capacity will
    increase by a proportional amount based on the scaling block size.

    NOTE! The AWS EC2 ASG minimum and maximum capacity drive the scaling value
    minimum and maximum tasks for AWS ECS. At no time will the number of ECS
    tasks be lower than the EC2 ASG minimum capacity. The minimum and maximum
    values will not necessarily be one-to-one. That is ScaleEC2ASGAndECSBySQS
    [ecs_tasks_per_ec2asg_instance=1000] means EC2 ASG maximum capacity should
    equal the forecast ECS tasks. If forecast is to run 5000 ECS tasks then the
    EC2 ASG maximum capacity should be at least 5.

    The scaling block size is a rough approximation of the aggregate group of
    messages that can be processed an amount of time that makes it worthwhile
    to scale out or in the ECS cluster service.

    This runs indefinitely. If there are too many exceptions it will abort.
    There are functions with backoff limiters for cases where the SQS queue
    returns the same value repeatedly as well as when the desired capacity
    remains the same between calls.
    """

    # pylint: disable=too-many-locals
    def __init__(self, logenv: hankai.lib.LogEnv, backoff: hankai.lib.Backoff) -> None:
        super().__init__(logenv=logenv, backoff=backoff)
        asg_env = hankai.aws.Environment(
            env=EnvironmentEC2ASGEnv,
            logenv=logenv,
        )
        ecs_env = hankai.aws.Environment(
            env=EnvironmentECSEnv,
            logenv=logenv,
        )
        sqs_env = hankai.aws.Environment(
            env=EnvironmentSQSEnv,
            logenv=logenv,
        )
        asg_session = hankai.aws.Session(environment=asg_env)
        ecs_session = hankai.aws.Session(environment=ecs_env)
        sqs_session = hankai.aws.Session(environment=sqs_env)
        asg_ser = hankai.aws.Servicer(
            session=asg_session,
            service_name=hankai.aws.ServiceName.EC2_AUTOSCALING,
            env=ServicerEC2ASGEnv,
            logenv=logenv,
        )
        ecs_ser = hankai.aws.Servicer(
            session=ecs_session,
            service_name=hankai.aws.ServiceName.ELASTIC_CONTAINER_SERVICE,
            env=ServicerECSEnv,
            logenv=logenv,
        )
        sqs_ser = hankai.aws.Servicer(
            session=sqs_session,
            service_name=hankai.aws.ServiceName.SIMPLE_QUEUE_SERVICE,
            env=ServicerSQSEnv,
            logenv=logenv,
        )
        sqs_scale = hankai.aws.ScaleBySQS(
            sqs=hankai.aws.SimpleQueueService(
                servicer=sqs_ser,
                queue_name="must-env-supersede",
                env=hankai.aws.SimpleQueueServiceEnv,
                logenv=logenv,
            ),
            scale=hankai.aws.SQSScale(
                env=hankai.aws.SQSScaleEnv,
                logenv=logenv,
            ),
        )
        asg = hankai.aws.EC2AutoScalingGroup(
            servicer=asg_ser,
            group_name="must-env-supersede",
            env=hankai.aws.EC2AutoScalingGroupEnv,
            logenv=logenv,
        )
        asg_sqs = hankai.aws.ScaleEC2ASGBySQS(
            ec2asg=asg,
            sqs_scale=sqs_scale,
            env=hankai.aws.ScaleEnv,
            logenv=logenv,
            backoff=backoff,
        )
        ecs = hankai.aws.ElasticContainerService(
            servicer=ecs_ser,
            cluster_name="must-env-supersede",
            service_name="must-env-supersede",
            env=hankai.aws.ElasticContainerServiceEnv,
            logenv=logenv,
        )
        ecs_sqs = hankai.aws.ScaleECSBySQS(
            ecs=ecs,
            sqs_scale=sqs_scale,
            env=hankai.aws.ScaleECSEnv,
            logenv=logenv,
            backoff=backoff,
        )
        self.logenv = hankai.lib.LogEnv(hankai.lib.LogEnvEnv)

        self.scaler = hankai.aws.ScaleEC2ASGAndECSBySQS(
            asg_sqs=asg_sqs,
            ecs_sqs=ecs_sqs,
            env=hankai.aws.ScaleEC2ASGAndECSEnv,
            logenv=logenv,
            backoff=backoff,
        )

    def start(self) -> None:
        """Start the scaling manager."""
        self.logenv.logger.info(
            "Orchestrator scaling manager for AWS EC2 Auto Scaling Group and "
            "AWS ECS by AWS SQS started [{}].",
            hankai.lib.Util.date_now(),
        )

        while True:
            self.scaler.adjust_capacity()


class ScalingManagerECSBySQS(ScalingManager):
    """Orchestrator scaling manager to scale in/out the the AWS ECS service
    based on the AWS SQS queue length.

    Monitor AWS SQS and adjust AWS ECS cluster service desired tasks
    based on the monitored SQS queue. As the queue message depth increases the
    desired tasks/capacity will increase by a proportional amount based on the
    scaling block size.

    The scaling block size is a rough approximation of the aggregate group of
    messages that can be processed an amount of time that makes it worthwhile
    to scale out or in the ECS cluster service.

    This runs indefinitely. If there are too many exceptions it will abort.
    There are functions with backoff limiters for cases where the SQS queue
    returns the same value repeatedly as well as when the desired capacity
    remains the same between calls.
    """

    def __init__(self, logenv: hankai.lib.LogEnv, backoff: hankai.lib.Backoff) -> None:
        super().__init__(logenv, backoff)
        environment = hankai.aws.Environment(
            env=hankai.aws.EnvironmentEnv,
            logenv=logenv,
        )
        session = hankai.aws.Session(environment=environment)
        ecs_ser = hankai.aws.Servicer(
            session=session,
            service_name=hankai.aws.ServiceName.ELASTIC_CONTAINER_SERVICE,
            env=ServicerECSEnv,
            logenv=logenv,
        )
        sqs_ser = hankai.aws.Servicer(
            session=session,
            service_name=hankai.aws.ServiceName.SIMPLE_QUEUE_SERVICE,
            env=ServicerSQSEnv,
            logenv=logenv,
        )
        sqs_scale = hankai.aws.ScaleBySQS(
            sqs=hankai.aws.SimpleQueueService(
                servicer=sqs_ser,
                queue_name="must-env-supersede",
                env=hankai.aws.SimpleQueueServiceEnv,
                logenv=logenv,
            ),
            scale=hankai.aws.SQSScale(
                env=hankai.aws.SQSScaleEnv,
                logenv=logenv,
            ),
        )
        ecs = hankai.aws.ElasticContainerService(
            servicer=ecs_ser,
            cluster_name="must-env-supersede",
            service_name="must-env-supersede",
            env=hankai.aws.ElasticContainerServiceEnv,
            logenv=logenv,
        )
        self.logenv = hankai.lib.LogEnv()

        self.scaler = hankai.aws.ScaleECSBySQS(
            ecs=ecs,
            sqs_scale=sqs_scale,
            env=hankai.aws.ScaleECSEnv,
            logenv=logenv,
            backoff=backoff,
        )

    def start(self) -> None:
        """Start the scaling manager."""
        self.logenv.logger.info(
            "Orchestrator scaling manager for AWS ECS by AWS SQS started [{}].",
            hankai.lib.Util.date_now(),
        )

        while True:
            self.scaler.adjust_capacity()
