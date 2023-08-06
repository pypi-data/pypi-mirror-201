from phiterm.utils.enums import ExtendedEnum


class WorkspaceVisibilityEnum(ExtendedEnum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class WorkspaceStarterTemplate(ExtendedEnum):
    aws_ai_app = "aws-ai-app"
    aws_ml_api = "aws-ml-api"
    aws_dp = "aws-data-platform"
    aws_spark_dp = "aws-spark-data-platform"
    aws_snowflake_dp = "aws-snowflake-data-platform"


class WorkspaceEnv(ExtendedEnum):
    dev = "dev"
    stg = "stg"
    prd = "prd"
    test = "test"
    all = "all"


class WorkspaceConfigType(ExtendedEnum):
    docker = "docker"
    k8s = "k8s"
    gcp = "gcp"
    aws = "aws"


class WorkspaceSetupActions(ExtendedEnum):
    WS_CONFIG_IS_AVL = "WS_CONFIG_IS_AVL"
    WS_IS_AUTHENTICATED = "WS_IS_AUTHENTICATED"
    GCP_SVC_ACCOUNT_IS_AVL = "GCP_SVC_ACCOUNT_IS_AVL"
    GIT_REMOTE_ORIGIN_IS_AVL = "GIT_REMOTE_ORIGIN_IS_AVL"
