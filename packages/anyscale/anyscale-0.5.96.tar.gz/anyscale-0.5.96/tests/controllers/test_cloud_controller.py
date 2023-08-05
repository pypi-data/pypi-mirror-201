import json
from typing import Any, Dict, Iterator, Optional, Tuple
from unittest.mock import ANY, MagicMock, Mock, patch

import boto3
from click import ClickException
from google.api_core.exceptions import NotFound
from google.auth.credentials import AnonymousCredentials
from moto import mock_cloudformation
import pytest

from anyscale.client.openapi_client.models import (
    AnyscaleAWSAccount,
    AnyscaleawsaccountResponse,
    Cloud,
    CloudConfig,
    CloudRegionAndZones,
    CloudregionandzonesResponse,
    CloudRegionInfo,
    CloudResponse,
    ClusterManagementStackVersions,
    CreateCloudResource,
    CreateCloudResourceGCP,
    UpdateCloudWithCloudResource,
    UpdateCloudWithCloudResourceGCP,
    WriteCloud,
)
from anyscale.client.openapi_client.models.cloud_state import CloudState
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)
from anyscale.client.openapi_client.models.subnet_id_with_availability_zone_aws import (
    SubnetIdWithAvailabilityZoneAWS,
)
from anyscale.controllers.cloud_controller import CloudController


DEFAULT_RAY_IAM_ROLE = "ray-autoscaler-v1"


@pytest.fixture()
def mock_api_client(cloud_test_data: Cloud) -> Mock:
    mock_api_client = Mock()
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock(return_value={})
    mock_api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put = Mock(
        return_value={}
    )
    mock_api_client.get_regions_and_zones_api_v2_clouds_gcp_regions_and_zones_get = Mock(
        return_value=CloudregionandzonesResponse(
            result=CloudRegionAndZones(
                regions={
                    "us-west1": CloudRegionInfo(name="us-west1", availability_zones={}),
                    "us-west2": CloudRegionInfo(name="us-west2", availability_zones={}),
                }
            )
        )
    )

    return mock_api_client


@pytest.fixture(autouse=True)
def mock_auth_api_client(
    mock_api_client: Mock, base_mock_anyscale_api_client: Mock
) -> Iterator[None]:
    mock_auth_api_client = Mock(
        api_client=mock_api_client, anyscale_api_client=base_mock_anyscale_api_client,
    )
    with patch.multiple(
        "anyscale.controllers.base_controller",
        get_auth_api_client=Mock(return_value=mock_auth_api_client),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_get_available_regions() -> Iterator[None]:
    with patch(
        "anyscale.controllers.cloud_controller.get_available_regions",
        return_value=["us-west-2"],
        autospec=True,
    ):
        yield


def mock_role(document: Optional[Dict[str, Any]] = None) -> Mock:
    if document is None:
        document = {}
    mock_role = Mock()

    mock_role.arn = "ARN"
    mock_role.attach_policy = Mock()
    mock_role.assume_role_policy_document = document
    mock_role.instance_profiles.all = Mock(return_value=[])

    return mock_role


def mock_role_with_external_id() -> Mock:
    return mock_role(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "1",
                    "Effect": "Allow",
                    "Principal": {"AWS": ["ARN"]},
                    "Action": "sts:AssumeRole",
                    "Condition": {"StringEquals": {"sts:ExternalId": "extid"}},
                }
            ],
        }
    )


def test_setup_cloud_gcp() -> None:
    mock_launch_gcp_cloud_setup = Mock(return_value=None)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        launch_gcp_cloud_setup=mock_launch_gcp_cloud_setup,
    ):
        cloud_controller = CloudController()
        cloud_controller.setup_cloud(
            provider="gcp", region=None, name="test-gcp", yes=True, gce=True,
        )

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1",
            name="test-gcp",
            is_k8s=False,
            folder_id=None,
            vpc_peering_ip_range=None,
            vpc_peering_target_project_id=None,
            vpc_peering_target_vpc_id=None,
        )

        mock_launch_gcp_cloud_setup.reset_mock()

        cloud_controller.setup_cloud(
            provider="gcp",
            region=None,
            name="test-gcp",
            yes=True,
            folder_id=1234,
            gce=False,
        )

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1",
            name="test-gcp",
            is_k8s=True,
            folder_id=1234,
            vpc_peering_ip_range=None,
            vpc_peering_target_project_id=None,
            vpc_peering_target_vpc_id=None,
        )

        mock_launch_gcp_cloud_setup.reset_mock()

        cloud_controller.setup_cloud(
            provider="gcp",
            region="us-west2",
            name="test-gcp",
            yes=True,
            folder_id=2345,
        )

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west2",
            name="test-gcp",
            is_k8s=True,
            folder_id=2345,
            vpc_peering_ip_range=None,
            vpc_peering_target_project_id=None,
            vpc_peering_target_vpc_id=None,
        )


@pytest.mark.parametrize(
    "vpc_peering_options",
    [
        ("10.0.0.0/12", "project_id", "vpc_id"),
        ("10.0.0.0/12", None, "vpc_id"),
        ("10.0.0.0/12", "project_id", None),
    ],
)
def test_setup_cloud_gcp_vpc_peering(
    vpc_peering_options: Tuple[str, Optional[str], Optional[str]]
) -> None:
    (
        vpc_peering_ip_range,
        vpc_peering_target_project_id,
        vpc_peering_target_vpc_id,
    ) = vpc_peering_options
    mock_launch_gcp_cloud_setup = Mock(return_value=None)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        launch_gcp_cloud_setup=mock_launch_gcp_cloud_setup,
    ):
        cloud_controller = CloudController()
        if vpc_peering_target_project_id is None or vpc_peering_target_vpc_id is None:
            with pytest.raises(ClickException):
                cloud_controller.setup_cloud(
                    provider="gcp",
                    region=None,
                    name="test-gcp",
                    yes=True,
                    gce=False,
                    vpc_peering_ip_range=vpc_peering_ip_range,
                    vpc_peering_target_project_id=vpc_peering_target_project_id,
                    vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
                )
        else:
            cloud_controller.setup_cloud(
                provider="gcp",
                region=None,
                name="test-gcp",
                yes=True,
                gce=False,
                vpc_peering_ip_range=vpc_peering_ip_range,
                vpc_peering_target_project_id=vpc_peering_target_project_id,
                vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
            )

        if vpc_peering_target_project_id is None or vpc_peering_target_vpc_id is None:
            return

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1",
            name="test-gcp",
            is_k8s=True,
            folder_id=None,
            vpc_peering_ip_range=vpc_peering_ip_range,
            vpc_peering_target_project_id=vpc_peering_target_project_id,
            vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
        )

        mock_launch_gcp_cloud_setup.reset_mock()

        cloud_controller.setup_cloud(
            provider="gcp",
            region=None,
            name="test-gcp",
            yes=True,
            gce=True,
            folder_id=1234,
            vpc_peering_ip_range=vpc_peering_ip_range,
            vpc_peering_target_project_id=vpc_peering_target_project_id,
            vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
        )

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1",
            name="test-gcp",
            is_k8s=False,
            folder_id=1234,
            vpc_peering_ip_range=vpc_peering_ip_range,
            vpc_peering_target_project_id=vpc_peering_target_project_id,
            vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
        )


@pytest.mark.parametrize(
    ("vpc_peering_options", "error_output"),
    [
        (
            ("not_an_ip_address", "project_id", "vpc_id"),
            "not_an_ip_address is not a valid IP address.",
        ),
        (
            ("10.0.0.0/20", "project_id", "vpc_id"),
            "10.0.0.0/20 is not a valid IP range. The minimum size is /16",
        ),
        (
            ("42.0.0.0/10", "project_id", "vpc_id"),
            "42.0.0.0/10 is not a allowed private IP address range for GCP",
        ),
    ],
)
def test_setup_cloud_gcp_vpc_peering_validation(
    vpc_peering_options: Tuple[str, str, str], error_output: str
) -> None:
    (
        vpc_peering_ip_range,
        vpc_peering_target_project_id,
        vpc_peering_target_vpc_id,
    ) = vpc_peering_options
    mock_launch_gcp_cloud_setup = Mock(return_value=None)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        launch_gcp_cloud_setup=mock_launch_gcp_cloud_setup,
    ):
        cloud_controller = CloudController()

        with pytest.raises(ClickException) as e:
            cloud_controller.setup_cloud(
                provider="gcp",
                region=None,
                name="test-gcp",
                yes=True,
                vpc_peering_ip_range=vpc_peering_ip_range,
                vpc_peering_target_project_id=vpc_peering_target_project_id,
                vpc_peering_target_vpc_id=vpc_peering_target_vpc_id,
            )

        assert error_output in e.value.message


def test_setup_cloud_gcp_bad_region() -> None:
    mock_confirm = Mock(side_effect=ClickException("aborted"))
    with patch.multiple(
        "anyscale.controllers.cloud_controller", confirm=mock_confirm,
    ):
        cloud_controller = CloudController()
        # NOTE: GCP regions are [cont]-[local][number], not [cont]-[local]-[number]
        with pytest.raises(ClickException):
            cloud_controller.setup_cloud(
                provider="gcp", region="us-west-2", name="test-gcp",
            )

        mock_confirm.assert_called()


def test_setup_cloud_invalid_provider() -> None:
    cloud_controller = CloudController()
    with pytest.raises(ClickException):
        cloud_controller.setup_cloud(
            provider="azure",
            region="azure-west-1",
            name="invalid cloud provider",
            yes=False,
        )


def test_delete_cloud_by_name(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    success = cloud_controller.delete_cloud(
        cloud_id=None, cloud_name=cloud_test_data.name, skip_confirmation=True
    )
    assert success

    cloud_controller.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_delete_cloud_by_id(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    success = cloud_controller.delete_cloud(
        cloud_id=cloud_test_data.id, cloud_name=None, skip_confirmation=True
    )
    assert success

    cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_with(
        cloud_id=cloud_test_data.id
    )
    cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_missing_name_and_id() -> None:
    cloud_controller = CloudController()

    with pytest.raises(ClickException):
        cloud_controller.delete_cloud(None, None, True)

    with pytest.raises(ClickException):
        cloud_controller.update_cloud_config(None, None, 0)

    with pytest.raises(ClickException):
        cloud_controller.get_cloud_config(None, None)


@pytest.mark.parametrize("role_name_exists", [True, False])
def test_setup_cross_region(cloud_test_data: Cloud, role_name_exists: bool) -> None:
    mock_get_aws_account = Mock(
        return_value=AnyscaleawsaccountResponse(
            result=AnyscaleAWSAccount(anyscale_aws_account="aws_account_type")
        )
    )
    mock_create_cloud = Mock(return_value=CloudResponse(result=cloud_test_data))

    mock_role = mock_role_with_external_id()
    mock_role_policy = Mock()
    mock_role.Policy.return_value = mock_role_policy
    if role_name_exists:
        roles = [mock_role, None, mock_role]
    else:
        roles = [None, mock_role]

    mock_iam = Mock()
    with patch.multiple(
        "anyscale.controllers.cloud_controller", _get_role=Mock(side_effect=roles),
    ), patch.multiple("boto3", resource=Mock(return_value=mock_iam),), patch.multiple(
        "secrets", token_hex=lambda x: "f" * x * 2
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = (
            mock_get_aws_account
        )
        cloud_controller.api_client.create_cloud_api_v2_clouds_post = mock_create_cloud
        cloud_controller.setup_aws_cross_account_role("us-west-2", "name")

    cloud_controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get.assert_called_once()

    assert (
        mock_role_policy.put.call_count == 2
    ), "Expected 2 calls, only got {}:\n{}".format(
        mock_role_policy.put.call_count, mock_role_policy.put.mock_calls
    )
    mock_role.AssumeRolePolicy.assert_called()

    mock_iam.create_role.assert_called_once_with(
        AssumeRolePolicyDocument=ANY, RoleName="anyscale-iam-role-ffffffff"
    )
    mock_iam.meta.client.update_role.assert_called_once()


def test_prepare_for_managed_cloud_setup() -> None:
    mock_get_available_regions = Mock(return_value=["us-west-1", "us-west-2"])
    mock_get_role = Mock(return_value=None)
    mock_get_user_env_aws_account = Mock(return_value="mock_user_aws_account_id")
    mock_create_cloud_api_v2_clouds_post = Mock(
        return_value=Mock(result=Mock(id="mock_cloud_id"))
    )
    cluster_management_stack_version = ClusterManagementStackVersions.V2

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_available_regions=mock_get_available_regions,
        _get_role=mock_get_role,
        get_user_env_aws_account=mock_get_user_env_aws_account,
    ), patch.multiple("secrets", token_hex=Mock(return_value="02e38860")):
        cloud_controller = CloudController()
        cloud_controller.api_client.create_cloud_api_v2_clouds_post = (
            mock_create_cloud_api_v2_clouds_post
        )

        (
            anyscale_iam_role_name,
            created_cloud_id,
        ) = cloud_controller.prepare_for_managed_cloud_setup(
            "us-west-2", "cloud_name", cluster_management_stack_version
        )

    assert anyscale_iam_role_name == "anyscale-iam-role-02e38860"
    assert created_cloud_id == "mock_cloud_id"

    mock_get_available_regions.assert_called_once_with()
    mock_get_role.assert_called_once_with(anyscale_iam_role_name, "us-west-2")
    mock_get_user_env_aws_account.assert_called_once_with("us-west-2")
    mock_create_cloud_api_v2_clouds_post.assert_called_once_with(
        write_cloud=WriteCloud(
            provider="AWS",
            region="us-west-2",
            credentials=f"arn:aws:iam::mock_user_aws_account_id:role/{anyscale_iam_role_name}",
            name="cloud_name",
            is_bring_your_own_resource=False,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )


def test_update_cloud_config_by_name(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    cloud_controller.update_cloud_config(
        cloud_id=None, cloud_name=cloud_test_data.name, max_stopped_instances=100,
    )

    cloud_controller.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    cloud_controller.api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put.assert_called_once_with(
        cloud_id=cloud_test_data.id,
        cloud_config=CloudConfig(max_stopped_instances=100),
    )


def test_update_cloud_config_by_id(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    cloud_controller.update_cloud_config(
        cloud_id=cloud_test_data.id, cloud_name=None, max_stopped_instances=100,
    )

    cloud_controller.api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put.assert_called_once_with(
        cloud_id=cloud_test_data.id,
        cloud_config=CloudConfig(max_stopped_instances=100),
    )


@pytest.mark.parametrize("cloud_id", [None, "cloud_id_1"])
@pytest.mark.parametrize("cloud_name", [None, "cloud_name_1"])
def test_set_default_cloud(cloud_id: Optional[str], cloud_name: Optional[str]) -> None:
    cloud_controller = CloudController()
    if not (cloud_id or cloud_name) or (cloud_id and cloud_name):
        # Error if neither or both of cloud_id and cloud_name provided
        with pytest.raises(ClickException):
            cloud_controller.set_default_cloud(
                cloud_id=cloud_id, cloud_name=cloud_name,
            )
    else:
        cloud_controller.set_default_cloud(
            cloud_id=cloud_id, cloud_name=cloud_name,
        )
        cloud_controller.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post.assert_called_once_with(
            cloud_id="cloud_id_1"
        )


@pytest.mark.parametrize("cloud_id", [None, "cloud_id_1"])
@pytest.mark.parametrize("cloud_name", [None, "cloud_name_1"])
def test_list_cloud(cloud_id: Optional[str], cloud_name: Optional[str]) -> None:
    cloud_controller = CloudController()
    cloud_controller.api_client.list_clouds_api_v2_clouds_get = Mock(
        return_value=Mock(results=[Mock()])
    )
    cloud_controller.list_clouds(cloud_name, cloud_id)

    if cloud_id is not None:
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
            cloud_id
        )
    elif cloud_name is not None:
        cloud_controller.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
            {"name": cloud_name}
        )
    else:
        cloud_controller.api_client.list_clouds_api_v2_clouds_get.assert_called_once_with()


@pytest.mark.parametrize(
    "anyscale_iam_role",
    [
        "arn:aws:iam::123:role/mock_anyscale_role",
        "arn:aws:iam::123:role/path/mock_anyscale_role",
    ],
)
@pytest.mark.parametrize(
    "anyscale_instance_role",
    [
        "arn:aws:iam::123:role/instance_role",
        "arn:aws:iam::123:role/path/instance_role",
    ],
)
@pytest.mark.parametrize("verify_success", [True, False])
@pytest.mark.parametrize("private_network", [True, False])
def test_register_cloud(
    anyscale_iam_role: str,
    anyscale_instance_role: str,
    verify_success: bool,
    private_network: bool,
) -> None:

    mock_cloud = Mock(result=Mock(id="mock_cloud_id"))
    mock_api_client = Mock(
        create_cloud_api_v2_clouds_post=Mock(return_value=mock_cloud)
    )
    mock_region = "mock_region"
    mock_cloud_name = "mock_cloud"
    mock_vpc_id = "mock_vpc_id"
    mock_subnet_ids = ["mock_subnet"]
    mock_efs_id = "mock_efs_id"
    mock_security_group_ids = ["security_group_id"]
    mock_s3_bucket_id = "mock_s3_bucket_id"
    mock_get_role = Mock()
    mock_get_aws_efs_mount_target_ip = Mock(return_value="mock_efs_ip")

    def mock_associate_subnet_ids_with_policy(resource, region):
        return [SubnetIdWithAvailabilityZoneAWS("mock_subnet", "mock_az")]

    cluster_management_stack_version = ClusterManagementStackVersions.V2
    with patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_aws_cloud_resources",
        new=Mock(return_value=verify_success),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        associate_aws_subnets_with_azs=mock_associate_subnet_ids_with_policy,
        _update_external_ids_for_policy=Mock(return_value={"mock_policy": "test"}),
        _get_role=mock_get_role,
        _get_aws_efs_mount_target_ip=mock_get_aws_efs_mount_target_ip,
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client

        if verify_success:
            cloud_controller.register_aws_cloud(
                region=mock_region,
                name=mock_cloud_name,
                vpc_id=mock_vpc_id,
                subnet_ids=mock_subnet_ids,
                efs_id=mock_efs_id,
                anyscale_iam_role_id=anyscale_iam_role,
                instance_iam_role_id=anyscale_instance_role,
                security_group_ids=mock_security_group_ids,
                s3_bucket_id=mock_s3_bucket_id,
                private_network=private_network,
                cluster_management_stack_version=cluster_management_stack_version,
                yes=True,
            )
        else:
            with pytest.raises(ClickException) as e:
                cloud_controller.register_aws_cloud(
                    region=mock_region,
                    name=mock_cloud_name,
                    vpc_id=mock_vpc_id,
                    subnet_ids=mock_subnet_ids,
                    efs_id=mock_efs_id,
                    anyscale_iam_role_id=anyscale_iam_role,
                    instance_iam_role_id=anyscale_instance_role,
                    security_group_ids=mock_security_group_ids,
                    s3_bucket_id=mock_s3_bucket_id,
                    private_network=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    yes=True,
                )
            e.match("Please make sure all the resources provided")
    mock_get_role.assert_called_once_with("mock_anyscale_role", mock_region)

    mock_api_client.create_cloud_api_v2_clouds_post.assert_called_with(
        write_cloud=WriteCloud(
            provider="AWS",
            region=mock_region,
            credentials=anyscale_iam_role,
            name=mock_cloud_name,
            is_bring_your_own_resource=True,
            is_private_cloud=private_network,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )

    mock_subnet_ids_with_azs = mock_associate_subnet_ids_with_policy(
        mock_subnet_ids, mock_region
    )

    if verify_success:
        mock_api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put.assert_called_with(
            cloud_id=mock_cloud.result.id,
            update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                cloud_resource_to_update=CreateCloudResource(
                    aws_vpc_id=mock_vpc_id,
                    aws_subnet_ids_with_availability_zones=mock_subnet_ids_with_azs,
                    aws_iam_role_arns=[anyscale_iam_role, anyscale_instance_role],
                    aws_security_groups=mock_security_group_ids,
                    aws_s3_id=mock_s3_bucket_id,
                    aws_efs_id=mock_efs_id,
                    aws_efs_mount_target_ip="mock_efs_ip",
                ),
            ),
        )
    else:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_once_with(
            cloud_id=mock_cloud.result.id
        )


@pytest.mark.parametrize(
    ("valid_filestore_config", "verify_success"),
    [
        pytest.param(True, True, id="success",),
        pytest.param(True, False, id="verification-fails",),
        pytest.param(False, False, id="invalid-filestore",),
    ],
)
@pytest.mark.parametrize("private_network", [True, False])
def test_register_cloud_gcp(
    valid_filestore_config: bool, verify_success: bool, private_network: bool,
) -> None:
    mock_cloud = Mock(result=Mock(id="mock_cloud_id"))
    mock_api_client = Mock(
        create_cloud_api_v2_clouds_post=Mock(return_value=mock_cloud)
    )
    mock_region = "mock_region"
    mock_project_id = "mock_project_id"
    mock_cloud_name = "mock_cloud"
    mock_vpc_name = "mock_vpc_name"
    mock_subnet_names = ["mock_subnet"]
    mock_filestore_instance_id = "mock_filestore_instance"
    mock_filestore_location = "mock_filestore_location"
    mock_anyscale_service_account_email = "123@123.com"
    mock_instance_service_account_email = "456@456.com"
    mock_firewall_policy_names = ["mock_firewall_policy"]
    mock_cloud_storage_bucket_name = "mock_cloud_storage_bucket_name"
    mock_provider_id = "projects/123/locations/global/workloadIdentityPools/mock-pool/providers/mock-provider"
    cluster_management_stack_version = ClusterManagementStackVersions.V2

    mock_get_application_default_credentials = Mock(
        return_value=(AnonymousCredentials(), mock_project_id)
    )

    def mock_get_gcp_filestore_config(
        factory, project_id, vpc_name, filestore_location, filestore_instance_id, logger
    ):
        if valid_filestore_config:
            return GCPFileStoreConfig(
                instance_name="mock_instance",
                mount_target_ip="mock_ip",
                root_dir="mock_root_dir",
            )
        else:
            raise NotFound

    with patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_gcp_cloud_resources",
        new=Mock(return_value=verify_success),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_import_gcp_utils=Mock(
            return_value=(
                mock_get_application_default_credentials,
                mock_get_gcp_filestore_config,
            )
        ),
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client

        if verify_success:
            cloud_controller.register_gcp_cloud(
                region=mock_region,
                name=mock_cloud_name,
                project_id=mock_project_id,
                vpc_name=mock_vpc_name,
                subnet_names=mock_subnet_names,
                filestore_instance_id=mock_filestore_instance_id,
                filestore_location=mock_filestore_location,
                anyscale_service_account_email=mock_anyscale_service_account_email,
                instance_service_account_email=mock_instance_service_account_email,
                provider_id=mock_provider_id,
                firewall_policy_names=mock_firewall_policy_names,
                cloud_storage_bucket_name=mock_cloud_storage_bucket_name,
                private_network=private_network,
                cluster_management_stack_version=cluster_management_stack_version,
                yes=True,
            )
        else:
            with pytest.raises(ClickException) as e:
                cloud_controller.register_gcp_cloud(
                    region=mock_region,
                    name=mock_cloud_name,
                    project_id=mock_project_id,
                    vpc_name=mock_vpc_name,
                    subnet_names=mock_subnet_names,
                    filestore_instance_id=mock_filestore_instance_id,
                    filestore_location=mock_filestore_location,
                    anyscale_service_account_email=mock_anyscale_service_account_email,
                    instance_service_account_email=mock_instance_service_account_email,
                    provider_id=mock_provider_id,
                    firewall_policy_names=mock_firewall_policy_names,
                    cloud_storage_bucket_name=mock_cloud_storage_bucket_name,
                    private_network=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    yes=True,
                )
            if valid_filestore_config:
                e.match("Please make sure all the resources provided")

    mock_api_client.create_cloud_api_v2_clouds_post.assert_called_with(
        write_cloud=WriteCloud(
            provider="GCP",
            region=mock_region,
            credentials=json.dumps(
                {
                    "project_id": mock_project_id,
                    "provider_id": mock_provider_id,
                    "service_account_email": mock_anyscale_service_account_email,
                }
            ),
            name=mock_cloud_name,
            is_bring_your_own_resource=True,
            is_private_cloud=private_network,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )

    if verify_success:
        mock_api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put.assert_called_with(
            cloud_id=mock_cloud.result.id,
            update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                cloud_resource_to_update=CreateCloudResourceGCP(
                    gcp_vpc_id=mock_vpc_name,
                    gcp_subnet_ids=mock_subnet_names,
                    gcp_cluster_node_service_account_email=mock_instance_service_account_email,
                    gcp_anyscale_iam_service_account_email=mock_anyscale_service_account_email,
                    gcp_filestore_config=GCPFileStoreConfig(
                        instance_name="mock_instance",
                        mount_target_ip="mock_ip",
                        root_dir="mock_root_dir",
                    ),
                    gcp_firewall_policy_ids=mock_firewall_policy_names,
                    gcp_cloud_storage_bucket_id=mock_cloud_storage_bucket_name,
                ),
            ),
        )
    else:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_once_with(
            cloud_id=mock_cloud.result.id
        )


@pytest.mark.parametrize("state", [CloudState.ACTIVE, CloudState.DELETED])
@pytest.mark.parametrize("has_cloud_resource", [True, False])
@pytest.mark.parametrize("cloud_provider", ["AWS", "GCP"])
@pytest.mark.parametrize("is_bring_your_own_resource", [True, False])
def test_verify_cloud(
    state: CloudState,
    has_cloud_resource: bool,
    cloud_provider: str,
    is_bring_your_own_resource: bool,
):
    cloud_resource_mock = Mock() if has_cloud_resource else None
    verify_mock = Mock(return_value=True)
    verify_aws_subnets_mock = Mock(return_value=True)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_cloud_id_and_name=Mock(return_value=("", "")),
        verify_aws_vpc=verify_mock,
        verify_aws_subnets=verify_aws_subnets_mock,
        verify_aws_iam_roles=verify_mock,
        verify_aws_security_groups=verify_mock,
        verify_aws_s3=verify_mock,
        verify_aws_efs=verify_mock,
        verify_aws_cloudformation_stack=verify_mock,
        CreateCloudResource=Mock(return_value=cloud_resource_mock),
    ):
        cloud_controller = CloudController()
        cloud_controller.log = Mock()
        cloud = Mock(
            result=Mock(
                state=state,
                region="mock_region",
                cloud_resource=cloud_resource_mock,
                provider=cloud_provider,
                is_bring_your_own_resource=is_bring_your_own_resource,
                is_private_cloud=False,
            )
        )
        cloud_controller.api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get = Mock(
            return_value=cloud
        )
        verify_result = cloud_controller.verify_cloud(
            cloud_name="mock_cloud_name", cloud_id="mock_cloud_id"
        )

        if state in (CloudState.DELETING, CloudState.DELETED):
            assert verify_result is False
        elif not has_cloud_resource:
            assert verify_result is False
        elif cloud_provider == "AWS":
            if is_bring_your_own_resource:
                assert verify_mock.call_count == 5
            else:
                assert verify_mock.call_count == 6
            verify_mock.assert_called_with(
                cloud_resource=cloud.result.cloud_resource,
                boto3_session=ANY,
                logger=cloud_controller.log,
            )
            verify_aws_subnets_mock.assert_called_once_with(
                cloud_resource=cloud.result.cloud_resource,
                region=cloud.result.region,
                is_private_network=False,
                logger=cloud_controller.log,
                ignore_capacity_errors=False,
            )
            assert verify_result
        else:
            assert verify_result is False


@pytest.mark.parametrize("cloud_setup_failure", [True, False])
def test_setup_managed_cloud(cloud_setup_failure) -> None:
    mock_region = "us-east-2"
    mock_cloud_name = "mock_cloud_name"
    mock_cloud_id = "mock_cloud_id"
    mock_anyscale_iam_role_name = "mock_anyscale_iam_role_name"
    mock_ray_iam_role_name = f"{mock_cloud_id}-cluster_node_role"
    mock_cfn_stack = "mock_cfn_stack"
    mock_api_client = Mock()
    mock_prepare_for_managed_cloud_setup = Mock(
        return_value=(mock_anyscale_iam_role_name, mock_cloud_id)
    )
    mock_run_cloudformation = Mock(return_value=mock_cfn_stack)
    mock_update_cloud_with_resources = Mock()

    cluster_management_stack_version = ClusterManagementStackVersions.V2

    if cloud_setup_failure:
        mock_update_cloud_with_resources.side_effect = Exception("ERROR")

    with patch.multiple(
        "anyscale.controllers.cloud_controller.CloudController",
        prepare_for_managed_cloud_setup=mock_prepare_for_managed_cloud_setup,
        run_cloudformation=mock_run_cloudformation,
        update_cloud_with_resources=mock_update_cloud_with_resources,
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client
        if cloud_setup_failure:
            with pytest.raises(ClickException):
                cloud_controller.setup_managed_cloud(
                    provider="aws",
                    region=mock_region,
                    name=mock_cloud_name,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
        else:
            cloud_controller.setup_managed_cloud(
                provider="aws",
                region=mock_region,
                name=mock_cloud_name,
                cluster_management_stack_version=cluster_management_stack_version,
            )

    mock_prepare_for_managed_cloud_setup.assert_called_with(
        mock_region, mock_cloud_name, cluster_management_stack_version
    )
    mock_run_cloudformation.assert_called_with(
        mock_region, mock_cloud_id, mock_anyscale_iam_role_name, mock_ray_iam_role_name
    )
    mock_update_cloud_with_resources.assert_called_with(mock_cfn_stack, mock_cloud_id)

    if cloud_setup_failure:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_with(
            cloud_id=mock_cloud_id
        )


def test_delete_cloud():
    mock_cloud_id = "mock_cloud_id"
    mock_cloud_name = "mock_cloud_name"
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_cloud_id_and_name=Mock(return_value=(mock_cloud_id, mock_cloud_name)),
        confirm=Mock(return_value=True),
    ):
        cloud_controller = CloudController()
        cloud_controller.log = Mock()
        mock_cloud = Mock(
            result=Mock(provider="AWS", is_bring_your_own_resource=False,)
        )
        cloud_controller.api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get = Mock(
            return_value=mock_cloud
        )
        cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put = Mock(
            return_value=mock_cloud
        )
        cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock()
        cloud_controller.delete_aws_managed_cloud = Mock()

        mock_confirm = Mock(return_value=True)

        with patch(cloud_controller.__module__ + ".confirm", new=mock_confirm):
            cloud_controller.delete_cloud(
                cloud_name=mock_cloud_name,
                cloud_id=mock_cloud_id,
                skip_confirmation=False,
            )

        mock_confirm.assert_called_once()

        cloud_controller.delete_aws_managed_cloud.assert_called_with(
            cloud=mock_cloud.result
        )
        cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_with(
            cloud_id=mock_cloud_id
        )
        cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put.assert_called_with(
            cloud_id=mock_cloud_id,
            update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                state=CloudState.DELETING
            ),
        )


@pytest.mark.parametrize("pre_deleted", [True, False])
@mock_cloudformation
def test_delete_aws_managed_cloud(pre_deleted: bool):
    cfn = boto3.client("cloudformation", region_name="us-west-2")
    stack_response = cfn.create_stack(
        StackName="stack_name", TemplateBody="{Resources: {}}"
    )
    stack_id = stack_response["StackId"]
    if pre_deleted:
        cfn.delete_stack(StackName=stack_id)

    cloud_mock = Mock(
        id="mock_cloud_id",
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id=stack_id,),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    assert cloud_controller.delete_aws_managed_cloud(cloud=cloud_mock)


@mock_cloudformation
def test_delete_aws_managed_cloud_invalid_cloudformation_stack():
    cloud_mock = Mock(
        id="mock_cloud_id",
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id="invalid_id"),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    with pytest.raises(ClickException) as e:
        cloud_controller.delete_aws_managed_cloud(cloud=cloud_mock,)

    assert "Failed to fetch the cloudformation stack" in e.value.message
