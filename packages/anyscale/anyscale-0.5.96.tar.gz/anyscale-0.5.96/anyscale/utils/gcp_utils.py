import subprocess
from typing import Dict, List, Optional, Set, Tuple, Union

from click import ClickException
from google.api_core.exceptions import NotFound
import google.auth
from google.auth.credentials import Credentials
from google.iam.v1.policy_pb2 import Binding

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)


def get_application_default_credentials(
    logger: BlockLogger,
) -> Tuple[Credentials, Optional[str]]:
    """Get application default credentials, or run `gcloud` to try to log in."""
    try:
        return google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as e:
        logger.warning(
            "Could not automatically determine Google Application Default Credentials, trying to authenticate via GCloud"
        )
        auth_login = subprocess.run(["gcloud", "auth", "application-default", "login"])
        if auth_login.returncode != 0:
            raise RuntimeError("Failed to authenticate via gcloud") from e

        return google.auth.default()


def binding_from_dictionary(
    inp: List[Dict[str, Union[List[str], str]]]
) -> List[Binding]:
    return [Binding(role=b["role"], members=b["members"]) for b in inp]


def check_policy_bindings(
    iam_policy: List[Binding], member: str, possible_roles: Set[str]
) -> bool:
    """Checks if `member` has any role in `possible_roles` given the specified iam_policy."""
    return any(
        policy.role in possible_roles and member in policy.members
        for policy in iam_policy
    )


def check_required_policy_bindings(
    iam_policy: List[Binding], member: str, required_roles: Set[str]
) -> bool:
    """Checks if `member` has all roles in `required_roles` given the specified iam_policy."""
    granted_roles = {policy.role for policy in iam_policy if member in policy.members}
    return required_roles.issubset(granted_roles)


def get_gcp_filestore_config(
    factory, project_id, vpc_name, filestore_location, filestore_instance_id, logger
):
    client = factory.filestore_v1.CloudFilestoreManagerClient()
    instance_name = "projects/{}/locations/{}/instances/{}".format(
        project_id, filestore_location, filestore_instance_id
    )
    try:
        file_store = client.get_instance(name=instance_name)
    except NotFound as e:
        logger.error(
            f"Could not find Filestore with id {filestore_instance_id} in project {project_id}. Please validate that you're using the correct GCP project and that the resource values are correct."
        )
        raise e
    root_dir = file_store.file_shares[0].name
    for v in file_store.networks:
        if v.network == vpc_name:
            mount_target_ip = v.ip_addresses[0]
            break
    else:
        logger.error(
            f"Filestore {filestore_instance_id} is not connected to {vpc_name}, but to {file_store.networks}. "
            f"This cannot be edited on an existing Filestore instance. Please recreate the filestore and connect it to {vpc_name}."
        )
        raise ClickException(
            f"Filestore {filestore_instance_id} is not connected to {vpc_name}."
        )
    return GCPFileStoreConfig(
        instance_name=instance_name, root_dir=root_dir, mount_target_ip=mount_target_ip,
    )
