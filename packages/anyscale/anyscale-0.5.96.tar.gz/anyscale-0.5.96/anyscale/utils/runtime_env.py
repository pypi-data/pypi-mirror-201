# pylint:disable=private-import
import copy
import hashlib
import logging
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING
from urllib.parse import urlparse
import uuid

import click

from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.client.openapi_client.models.cloud_with_cloud_resource import (
    CloudWithCloudResource,
)
from anyscale.client.openapi_client.models.decorated_session import DecoratedSession
from anyscale.client.openapi_client.models.user_info import UserInfo
from anyscale.shared_anyscale_utils.aws import AwsArn, S3_BUCKET_ARN_PREFIX
from anyscale.util import is_anyscale_workspace
from anyscale.utils.ray_utils import zip_directory  # type: ignore


if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _upload_file_to_google_cloud_storage(file: str, bucket: str, object_name: str):
    try:
        from google.cloud import storage

    except Exception:  # noqa: BLE001
        raise click.ClickException(
            "Could not upload file to Google Storage. Could not import the Google Storage Python API via `from google.cloud import storage`.  Please check your installation or try running `pip install --upgrade google-cloud-storage`."
        )
    try:
        storage_client = storage.Client()
        bucket_obj = storage_client.bucket(bucket)
        blob = bucket_obj.blob(object_name)
        blob.upload_from_filename(file)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Could not upload file to Google Cloud Storage. Please check your credentials and ensure that the bucket exists. {e}"
        )


def _upload_file_to_s3(file: str, bucket: str, object_key: str):
    try:
        import boto3
    except Exception:  # noqa: BLE001
        raise click.ClickException(
            "Could not upload file to S3: Could not import the Amazon S3 Python API via `import boto3`.  Please check your installation or try running `pip install boto3`."
        )
    try:
        s3_client = boto3.client("s3")
        s3_client.upload_file(file, bucket, object_key)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Could not upload file to S3. Check your credentials and that the bucket exists. Original error: {e}"
        )


def _get_remote_storage_object_name(upload_path, upload_filename):
    # Strip leading slash, otherwise bucket will create a new directory called "/".
    object_name = os.path.join(urlparse(upload_path).path, upload_filename).lstrip("/")
    return object_name


def _upload_file_to_remote_storage(
    source_file: str, upload_path: str, upload_filename: str
):
    parsed_upload_path = urlparse(upload_path)
    service = parsed_upload_path.scheme
    bucket = parsed_upload_path.netloc
    object_name = _get_remote_storage_object_name(upload_path, upload_filename)
    if service == "s3":
        _upload_file_to_s3(source_file, bucket, object_key=object_name)
    if service == "gs":
        _upload_file_to_google_cloud_storage(
            source_file, bucket, object_name=object_name
        )

    final_uploaded_filepath = os.path.join(upload_path, upload_filename)
    try:
        from smart_open import open

        open(final_uploaded_filepath)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Could not open uploaded file, maybe something went wrong while uploading: {e}."
        )

    return final_uploaded_filepath


def is_dir_remote_uri(working_dir: str) -> bool:
    parsed = urlparse(working_dir)
    if parsed.scheme:
        return True
    return False


def upload_and_rewrite_working_dir(
    runtime_env_json: Dict[str, Any],
    upload_file_to_remote_storage_fn: Callable[
        [str, str, str], str
    ] = _upload_file_to_remote_storage,
) -> Dict[str, Any]:
    """Upload a local working_dir and rewrite the working_dir field with the destination remote URI.

    After uploading, deletes the "upload_path" field because it is no longer used and is not a valid
    OSS runtime env field.
    """
    if runtime_env_json.get("working_dir", None) is None:
        return runtime_env_json

    working_dir = runtime_env_json["working_dir"]
    if is_dir_remote_uri(working_dir):
        # The working dir is a remote URI already
        return runtime_env_json

    upload_path = runtime_env_json["upload_path"]
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_file_path = os.path.join(
            temp_dir, "anyscale_generated_working_dir.zip"
        )
        zip_directory(
            working_dir,
            excludes=runtime_env_json.get("excludes", []),
            output_path=temp_zip_file_path,
            # Ray requires remote Zip URIs to consist of a single top-level directory when unzipped.
            include_parent_dir=True,
        )

        hash_val = hashlib.md5(Path(temp_zip_file_path).read_bytes()).hexdigest()
        uploaded_zip_file_name = f"_anyscale_pkg_{hash_val}.zip"
        final_uploaded_filepath = upload_file_to_remote_storage_fn(
            temp_zip_file_path, upload_path, uploaded_zip_file_name,
        )

    final_runtime_env = runtime_env_json.copy()
    final_runtime_env["working_dir"] = final_uploaded_filepath
    del final_runtime_env["upload_path"]
    return final_runtime_env


def override_runtime_env_for_local_working_dir(
    runtime_env: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    If runtime_env contains a "upload_path" field, we need to upload it first
    before backing it up inside EFS (if in workspaces).
    """
    if runtime_env:
        runtime_env = upload_and_rewrite_working_dir(runtime_env)

    if is_anyscale_workspace():
        import anyscale

        runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        # Snapshot the working directory to EFS so the job we submit can read it from there
        parsed_working_dir = urlparse(runtime_env["working_dir"])
        # We add prefix "file://" only if the working dir is local dir
        if not parsed_working_dir.scheme:
            runtime_env["working_dir"] = "file://" + runtime_env["working_dir"]
        fake_job_id = uuid.uuid4().hex
        runtime_env = anyscale.snapshot_util.checkpoint_job(fake_job_id, runtime_env)
        runtime_env["working_dir"] = "file://" + runtime_env["working_dir"]

    return runtime_env


def upload_and_rewrite_workspace_working_dir(
    *,
    api_client: DefaultApi,
    existing_runtime_env: Dict[str, Any],
    workspace_id: str,
    cluster_id: str,
) -> Dict[str, Any]:
    """
    Push Workspace working dir to S3 bucket and rewrite the working_dir field with the destination uri

    If the upload_path is not specified by the user, we will get the s3 bucket
    name based on the cloud. We then rewrite the working_dir to the S3 path
    so that the launched service will read from S3 directly.

    The S3 path: s3://{s3_bucket_name}/{org_id}/{cloud_id}/workspace_snapshots/{workspace_id}/{backup_zip}
    """
    decorated_cluster = api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get(
        cluster_id
    ).result
    cloud_id = decorated_cluster.cloud.id

    s3_bucket_name = _get_cloud_s3_bucket_from_cluster(api_client, decorated_cluster)
    org_id = _get_organization_id(api_client)
    new_runtime_env = copy.deepcopy(existing_runtime_env)
    pre_upload_working_dir = new_runtime_env["working_dir"]

    new_runtime_env[
        "upload_path"
    ] = f"s3://{s3_bucket_name}/{org_id}/{cloud_id}/workspace_snapshots/{workspace_id}"
    new_runtime_env = upload_and_rewrite_working_dir(new_runtime_env)

    logger.info(
        f"Uploaded working directory content from {Path(pre_upload_working_dir).absolute()} to {new_runtime_env['working_dir']}"
    )
    return new_runtime_env


def _get_organization_id(api_client: DefaultApi):
    user_info: UserInfo = (api_client.get_user_info_api_v2_userinfo_get().result)
    orgs = user_info.organizations
    return orgs[0].id


def _get_cloud_s3_bucket_from_cluster(
    api_client: DefaultApi, decorated_cluster: DecoratedSession
) -> Optional[str]:
    """
    If the cloud has an associated aws s3 bucket, we return its name.

    Please note that this is only for v2 clouds where customers have their
    own S3 buckets.
    """
    cloud_id = decorated_cluster.cloud.id
    cloud: CloudWithCloudResource = api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get(
        cloud_id
    ).result
    if cloud.provider == CloudProviders.GCP:
        raise click.ClickException(
            "Currently launching a service from workspaces in a GCP cloud is not supported. "
            "Please contact Anyscale support for more info."
        )
    if cloud and cloud.cloud_resource and cloud.cloud_resource.aws_s3_id:
        s3_bucket_name = cloud.cloud_resource.aws_s3_id
        # Buckets can also be in format of "arn:aws:s3:::bucket/path" instead of "bucket/path"
        if s3_bucket_name.startswith(S3_BUCKET_ARN_PREFIX):
            s3_bucket_name = AwsArn.from_string(s3_bucket_name).resource_id
        return s3_bucket_name
    else:
        return None
