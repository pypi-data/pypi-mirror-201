from json import dumps
from typing import Dict, Set

from constructs import Construct
from hmd_cli_tools.cdktf_tools import HmdCdkTfStack, get_neptune_endpoint, LibrarianHmdCdkTfStack
from hmd_cli_tools.hmd_cli_tools import (
    get_cloud_region,
    get_deployer_target_session,
    get_secret,
    get_session,
)
from hmd_lib_cdktf_factories import Lambda, ApiGateway, Iam, Sqs


class CdkTfStack(LibrarianHmdCdkTfStack):
    def __init__(
        self,
        scope: Construct,
        ns: str,
        instance_name,
        repo_name,
        deployment_id,
        environment,
        hmd_region,
        customer_code,
        repo_version,
        account_number,
        profile,
        config,
    ):
        super().__init__(
            scope,
            ns,
            instance_name,
            repo_name,
            deployment_id,
            environment,
            hmd_region,
            customer_code,
            repo_version,
            account_number,
            profile,
            config,
        )
