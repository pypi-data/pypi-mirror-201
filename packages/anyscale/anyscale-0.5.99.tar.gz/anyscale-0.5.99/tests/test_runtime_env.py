# type: ignore

import os
from typing import Optional
from unittest.mock import Mock, mock_open, patch

import boto3
import pytest
import smart_open

import anyscale
from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.client.openapi_client.models.decoratedsession_response import (
    DecoratedsessionResponse,
)
from anyscale.utils.runtime_env import (
    _get_cloud_gs_bucket_from_cloud,
    _get_cloud_s3_bucket_from_cloud,
    override_runtime_env_for_local_working_dir,
    upload_and_rewrite_workspace_working_dir,
)


def test_override_no_workspace():
    local_test_zip_path = "file://test.zip"
    runtime_env = {"working_dir": local_test_zip_path}
    modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
    assert modified_runtime_env["working_dir"] == local_test_zip_path


def test_override_upload_no_workspace():
    runtime_env = {
        "working_dir": "job-services-cuj-examples",
        "upload_path": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job",
    }
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.multiple(
        os, makedirs=Mock()
    ), patch("builtins.open", mock_open()), patch.multiple(
        boto3, client=boto_mock
    ), patch.multiple(
        smart_open, open=Mock()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith(
            "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job"
        )
        assert modified_runtime_env["working_dir"].endswith(".zip")


def test_override_upload_with_workspace():
    runtime_env = {
        "working_dir": "job-services-cuj-examples",
        "upload_path": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job",
    }
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ,
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "Test_workspace_id"},
        clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        boto3, client=boto_mock
    ), patch.multiple(
        smart_open, open=Mock()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith("file:///efs/jobs")
        assert modified_runtime_env["working_dir"].endswith(".zip")


def test_runtime_env_override_to_efs_workspace():
    runtime_env = {"working_dir": "file://test.zip"}
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ,
        {"ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "Test_workspace_id"},
        clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "urllib.request", urlretrieve=Mock()
    ), patch(
        "builtins.open", mock_open()
    ):
        modified_runtime_env = override_runtime_env_for_local_working_dir(runtime_env)
        assert modified_runtime_env["working_dir"].startswith("file:///efs")


def test_local_runtime_env_override_to_efs_job():
    runtime_env = {"working_dir": "file://test.zip"}
    test_job_id = "Test_job_id"
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "urllib.request", urlretrieve=Mock()
    ), patch(
        "builtins.open", mock_open()
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )


def test_s3_runtime_env_override_to_efs_job():
    runtime_env = {
        "working_dir": "s3://bk-premerge-first-jawfish-artifacts/e2e_tests/job/_anyscale_pkg_00216a215e75dff900a133c9ac9c764a.zip"
    }
    test_job_id = "Test_job_id"
    boto_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        boto3, client=boto_mock
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        boto_mock.assert_called_once_with("s3")
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )


def test_https_runtime_env_override_to_efs_job():
    runtime_env = {
        "working_dir": "https://github.com/anyscale/docs_examples/archive/refs/heads/main.zip"
    }
    test_job_id = "Test_job_id"
    urlretrieve_mock = Mock()
    with patch.multiple(os.path, ismount=Mock(return_value=True)), patch.dict(
        os.environ, {"ANYSCALE_EXPERIMENTAL_INITIAL_JOB_ID": test_job_id}, clear=True,
    ), patch.multiple(os, makedirs=Mock()), patch(
        "builtins.open", mock_open()
    ), patch.multiple(
        "urllib.request", urlretrieve=urlretrieve_mock
    ):
        modified_runtime_env = anyscale.snapshot_util.env_hook(runtime_env)
        urlretrieve_mock.assert_called_once()
        assert (
            modified_runtime_env["working_dir"]
            == f"/efs/jobs/{test_job_id}/working_dir.zip"
        )


@pytest.mark.parametrize(
    "working_dir", [".", "./subdir/subdir2", "/root_dir/subdir1"],
)
@pytest.mark.parametrize(
    "protocol", ["s3", "gs"],
)
def test_upload_and_rewrite_workspace_working_dir(working_dir: str, protocol: str):
    """
    This test checks that the upload remote path follows the expected pattern.
    """
    mock_logger = Mock()
    workspace_id = "test_workspace_id"
    cluster_id = "test_cluster_id"

    cloud_id = "test_cloud_id"
    org_id = "test_org_id"
    remote_bucket_name = "test_remote_bucket_name"

    # mock api calls utilized for collecting information required to construct the remote path
    mock_api_client = Mock()
    mock_get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get = Mock(
        return_value=DecoratedsessionResponse(result=Mock(cloud=Mock(id=cloud_id)))
    )
    if protocol == "s3":
        mock_api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get = Mock(
            return_value=Mock(
                result=Mock(
                    provider=CloudProviders.AWS,
                    cloud_resource=Mock(aws_s3_id=remote_bucket_name),
                )
            )
        )
    elif protocol == "gs":
        mock_api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get = Mock(
            return_value=Mock(result=Mock(provider=CloudProviders.GCP, id=cloud_id,))
        )
        mock_api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_get = Mock(
            return_value=Mock(
                result=Mock(
                    cloud_resource=Mock(gcp_cloud_storage_bucket_id=remote_bucket_name),
                )
            )
        )
    mock_get_user_info_api_v2_userinfo_get = Mock(
        return_value=Mock(result=Mock(organizations=[Mock(id=org_id)]))
    )
    mock_api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get = (
        mock_get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get
    )
    mock_api_client.get_user_info_api_v2_userinfo_get = (
        mock_get_user_info_api_v2_userinfo_get
    )

    rewritten_runtime_env = {
        "pip": ["requests"],
        "working_dir": f"{protocol}://bucket",
    }
    upload_and_rewrite_working_dir_mock = Mock(return_value=rewritten_runtime_env)
    with patch.multiple(
        "anyscale.utils.runtime_env",
        upload_and_rewrite_working_dir=upload_and_rewrite_working_dir_mock,
    ):
        upload_and_rewrite_workspace_working_dir(
            api_client=mock_api_client,
            existing_runtime_env={"working_dir": working_dir},
            workspace_id=workspace_id,
            cluster_id=cluster_id,
            log=mock_logger,
        )
    expected_bucket_prefix = f"{protocol}://{remote_bucket_name}/{org_id}/{cloud_id}/workspace_snapshots/{workspace_id}"

    call_args = upload_and_rewrite_working_dir_mock.call_args
    runtime_env_arg = call_args[0][0]
    assert runtime_env_arg["working_dir"] == working_dir
    assert runtime_env_arg["upload_path"].startswith(expected_bucket_prefix)


@pytest.mark.parametrize(
    ("aws_s3_id", "expected_bucket_name"),
    [
        (None, None),
        (
            "anyscale-production-data-cld-9xr5r1b2g6egh9bwgdi66whsjv",
            "anyscale-production-data-cld-9xr5r1b2g6egh9bwgdi66whsjv",
        ),
        (
            "arn:aws:s3:::anyscale-test-data-cld-n5rtny1bj8pv6gsmb7m5a4l2",
            "anyscale-test-data-cld-n5rtny1bj8pv6gsmb7m5a4l2",
        ),
    ],
)
def test_get_s3_bucket_aws(
    aws_s3_id: Optional[str], expected_bucket_name: Optional[str]
):
    cloud = Mock(provider=CloudProviders.AWS, cloud_resource=Mock(aws_s3_id=aws_s3_id))

    assert _get_cloud_s3_bucket_from_cloud(cloud) == expected_bucket_name


@pytest.mark.parametrize(
    ("gcp_cloud_storage_bucket_id", "expected_bucket_name"),
    [
        (None, None),
        (
            "anyscale-production-data-cld-9xr5r1b2g6egh9bwgdi66whsjv",
            "anyscale-production-data-cld-9xr5r1b2g6egh9bwgdi66whsjv",
        ),
    ],
)
def test_get_gs_bucket_gcp(
    gcp_cloud_storage_bucket_id: Optional[str], expected_bucket_name: Optional[str]
):
    mock_api_client = Mock()
    mock_api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_get = Mock(
        return_value=Mock(
            result=Mock(
                cloud_resource=Mock(
                    gcp_cloud_storage_bucket_id=gcp_cloud_storage_bucket_id
                ),
            )
        )
    )

    cloud = Mock(id="test_cloud_id", provider=CloudProviders.GCP,)

    assert (
        _get_cloud_gs_bucket_from_cloud(mock_api_client, cloud) == expected_bucket_name
    )
