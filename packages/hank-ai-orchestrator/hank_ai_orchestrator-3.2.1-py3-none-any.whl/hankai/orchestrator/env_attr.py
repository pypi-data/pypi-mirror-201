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
"""Orchestrator EnvEnum to differentiate between mixed services."""

import hankai.lib


class EnvironmentEC2ASGEnv(hankai.lib.EnvEnum):
    """ENV variables and Environment attributes for AWS Environment."""

    HANK_ENVIRONMENT_EC2ASG_PROFILE = "profile"
    HANK_ENVIRONMENT_EC2ASG_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_EC2ASG_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_EC2ASG_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_EC2ASG_REGION = "region"
    HANK_ENVIRONMENT_EC2ASG_OUTPUT = "output"


class EnvironmentECSEnv(hankai.lib.EnvEnum):
    """ENV variables and Environment attributes for AWS ECS."""

    HANK_ENVIRONMENT_ECS_PROFILE = "profile"
    HANK_ENVIRONMENT_ECS_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_ECS_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_ECS_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_ECS_REGION = "region"
    HANK_ENVIRONMENT_ECS_OUTPUT = "output"


class EnvironmentSQSEnv(hankai.lib.EnvEnum):
    """ENV variables and Environment attributes for AWS SQS."""

    HANK_ENVIRONMENT_SQS_PROFILE = "profile"
    HANK_ENVIRONMENT_SQS_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_SQS_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_SQS_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_SQS_REGION = "region"
    HANK_ENVIRONMENT_SQS_OUTPUT = "output"


class ServicerEC2ASGEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS EC2 ASG."""

    HANK_SERVICER_EC2ASG_API_VERSION = "api_version"
    HANK_SERVICER_EC2ASG_USE_SSL = "use_ssl"
    HANK_SERVICER_EC2ASG_VERIFY = "verify"
    HANK_SERVICER_EC2ASG_ENDPOINT_URL = "endpoint_url"


class ServicerECSEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS ECS."""

    HANK_SERVICER_ECS_API_VERSION = "api_version"
    HANK_SERVICER_ECS_USE_SSL = "use_ssl"
    HANK_SERVICER_ECS_VERIFY = "verify"
    HANK_SERVICER_ECS_ENDPOINT_URL = "endpoint_url"


class ServicerSQSEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS SQS."""

    HANK_SERVICER_SQS_API_VERSION = "api_version"
    HANK_SERVICER_SQS_USE_SSL = "use_ssl"
    HANK_SERVICER_SQS_VERIFY = "verify"
    HANK_SERVICER_SQS_ENDPOINT_URL = "endpoint_url"


class EnvironmentSQSRequestsEnv(hankai.lib.EnvEnum):
    """ENV variables and Environment attributes for AWS Environment."""

    HANK_ENVIRONMENT_SQS_REQUESTS_PROFILE = "profile"
    HANK_ENVIRONMENT_SQS_REQUESTS_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_SQS_REQUESTS_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_SQS_REQUESTS_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_SQS_REQUESTS_REGION = "region"
    HANK_ENVIRONMENT_SQS_REQUESTS_OUTPUT = "output"


class EnvironmentSQSResponsesEnv(hankai.lib.EnvEnum):
    """ENV variables and Environment attributes for AWS Environment."""

    HANK_ENVIRONMENT_SQS_RESPONSES_PROFILE = "profile"
    HANK_ENVIRONMENT_SQS_RESPONSES_ACCESS_KEY_ID = "access_key_id"
    HANK_ENVIRONMENT_SQS_RESPONSES_SECRET_ACCESS_KEY = "secret_access_key"
    HANK_ENVIRONMENT_SQS_RESPONSES_SESSION_TOKEN = "session_token"
    HANK_ENVIRONMENT_SQS_RESPONSES_REGION = "region"
    HANK_ENVIRONMENT_SQS_RESPONSES_OUTPUT = "output"


class ServicerSQSRequestsEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS SQS."""

    HANK_SERVICER_SQS_REQUESTS_API_VERSION = "api_version"
    HANK_SERVICER_SQS_REQUESTS_USE_SSL = "use_ssl"
    HANK_SERVICER_SQS_REQUESTS_VERIFY = "verify"
    HANK_SERVICER_SQS_REQUESTS_ENDPOINT_URL = "endpoint_url"


class ServicerSQSResponsesEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS SQS."""

    HANK_SERVICER_SQS_RESPONSES_API_VERSION = "api_version"
    HANK_SERVICER_SQS_RESPONSES_USE_SSL = "use_ssl"
    HANK_SERVICER_SQS_RESPONSES_VERIFY = "verify"
    HANK_SERVICER_SQS_RESPONSES_ENDPOINT_URL = "endpoint_url"


class SQSResponsesQueueEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS SQS."""

    HANK_SQS_RESPONSES_QUEUE_NAME = "queue_name"
    HANK_SQS_RESPONSES_RECEIVE_ATTRIBUTE_NAMES = "receive_attribute_names"
    HANK_SQS_RESPONSES_MESSAGE_ATTRIBUTE_NAMES = "message_attribute_names"
    HANK_SQS_RESPONSES_MAX_MESSAGES = "max_messages"
    HANK_SQS_RESPONSES_VISIBILITY_TIMEOUT = "visibility_timeout"
    HANK_SQS_RESPONSES_WAIT_TIME_SECONDS = "wait_time_seconds"
    HANK_SQS_RESPONSES_MESSAGE_ATTRIBUTES = "message_attributes"
    HANK_SQS_RESPONSES_MESSAGE_GROUP_ID = "message_group_id"
    HANK_SQS_RESPONSES_S3_BUCKET = "s3_bucket"
    HANK_SQS_RESPONSES_S3_ALWAYS = "s3_always"
    HANK_SQS_RESPONSES_S3_THRESHOLD_BYTES = "s3_threshold_bytes"


class SQSRequestsQueueEnv(hankai.lib.EnvEnum):
    """ENV variables and Servicer attributes for AWS SQS."""

    HANK_SQS_REQUESTS_QUEUE_NAME = "queue_name"
    HANK_SQS_REQUESTS_RECEIVE_ATTRIBUTE_NAMES = "receive_attribute_names"
    HANK_SQS_REQUESTS_MESSAGE_ATTRIBUTE_NAMES = "message_attribute_names"
    HANK_SQS_REQUESTS_MAX_MESSAGES = "max_messages"
    HANK_SQS_REQUESTS_VISIBILITY_TIMEOUT = "visibility_timeout"
    HANK_SQS_REQUESTS_WAIT_TIME_SECONDS = "wait_time_seconds"
    HANK_SQS_REQUESTS_MESSAGE_ATTRIBUTES = "message_attributes"
    HANK_SQS_REQUESTS_MESSAGE_GROUP_ID = "message_group_id"
    HANK_SQS_REQUESTS_S3_BUCKET = "s3_bucket"
    HANK_SQS_REQUESTS_S3_ALWAYS = "s3_always"
    HANK_SQS_REQUESTS_S3_THRESHOLD_BYTES = "s3_threshold_bytes"
