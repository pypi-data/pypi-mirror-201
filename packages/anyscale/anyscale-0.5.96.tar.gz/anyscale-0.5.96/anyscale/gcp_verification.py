from functools import partial
import importlib
import ipaddress
from typing import Any, Dict, Iterable, List, Tuple

from google.api_core.exceptions import NotFound, PermissionDenied
from google.auth.credentials import Credentials
import google.cloud
from google.cloud import compute_v1
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.constants import (
    PUBLIC_ACCESS_PREVENTION_ENFORCED,
    PUBLIC_ACCESS_PREVENTION_INHERITED,
)
from google.iam.v1.policy_pb2 import Binding
from googleapiclient.discovery import build as api_client_build
from googleapiclient.errors import HttpError

from anyscale.cli_logger import BlockLogger
from anyscale.shared_anyscale_utils.conf import ANYSCALE_HOST
from anyscale.util import confirm
from anyscale.utils.gcp_utils import (
    binding_from_dictionary,
    check_policy_bindings,
    check_required_policy_bindings,
    get_application_default_credentials,
)
from anyscale.utils.network_verification import (
    check_inbound_firewall_permissions,
    FirewallRule,
    GCP_SUBNET_CAPACITY,
    Protocol,
)


class GCPLogger:
    def __init__(self, logger: BlockLogger, project_id: str, yes: bool = False):
        self.internal = logger
        self.project_id = project_id
        self.yes = yes

    def log_resource_not_found_error(self, resource_name: str, resource_id: str):
        self.internal.error(
            f"Could not find {resource_name} with id {resource_id} in project {self.project_id}. Please validate that you're using the correct GCP project and that the resource values are correct."
        )

    def confirm_missing_permission(self, error_str: str):
        self.internal.error(error_str)
        confirm(
            "If the serivce account has these required permissions granted via other roles\n"
            "or via a group, press 'y' to continue with verification or 'N' to abort.",
            yes=self.yes,
        )


class GoogleCloudClientFactory:
    """Factory to generate both Google Cloud Client libraries & Google API Client libraries.

    Google Cloud Client libraries are instantiated by:
    ```
        factory = GoogleCloudClientFactory(credentials=AnonymousCredentials())
        client = factory.compute_v1.ExampleClient()
    ```

    Google API Client libraries are instantiated by:
    ```
        factory = GoogleCloudClientFactory(credentials=AnonymousCredentials())
        client = factory.build("iam", "v1")
    ```
    """

    def __init__(self, credentials: Credentials, force_rest=False, **kwargs):
        kwargs["credentials"] = credentials
        self.kwargs = kwargs
        self.force_rest = force_rest

    def __getattr__(self, client_library: str):
        """Get a wrapped Google Cloud Client library that injects default values from the factory."""
        if not hasattr(google.cloud, client_library):
            importlib.import_module(f"google.cloud.{client_library}")
        module = getattr(google.cloud, client_library)
        kwargs = self.kwargs

        # NOTE the `storage` library only supports HTTP, but doesn't
        # have the `transport` argument in its signature.
        if self.force_rest and client_library != "storage":
            kwargs["transport"] = "rest"

        class WrappedClient:
            def __getattr__(self, client_type: str):
                return partial(getattr(module, client_type), **kwargs)

        return WrappedClient()

    def build(self, service_name: str, version: str):
        """Return a Google API Client with default values from the factor"""
        return api_client_build(
            service_name, version, cache_discovery=False, **self.kwargs
        )


def verify_gcp(resources: Dict[str, Any], logger: BlockLogger) -> bool:
    credentials, credentials_project = get_application_default_credentials(logger)
    specified_project = resources["project_id"]
    if credentials_project != specified_project:
        logger.warning(
            f"Default credentials are for {credentials_project}, but this cloud is being configured for {specified_project}"
        )

    factory = GoogleCloudClientFactory(credentials=credentials)
    gcp_logger = GCPLogger(logger, specified_project)

    return all(
        [
            _verify_gcp_project(factory, resources, gcp_logger),
            _verify_gcp_access_service_account(factory, resources, gcp_logger),
            _verify_gcp_dataplane_service_account(factory, resources, gcp_logger),
            _verify_gcp_networking(factory, resources, gcp_logger),
            _verify_firewall_policy(factory, resources, gcp_logger),
            _verify_filestore(factory, resources, gcp_logger),
            _verify_cloud_storage(factory, resources, gcp_logger),
        ]
    )


def _verify_gcp_networking(
    factory: GoogleCloudClientFactory, resources: Dict, logger: GCPLogger,
) -> bool:
    """Verify the existence and connectedness of the VPC & Subnet."""

    project = resources["project_id"]
    vpc_name = resources["vpc_name"]
    # TODO Verify Internet Gateway
    try:
        vpc = factory.compute_v1.NetworksClient().get(project=project, network=vpc_name)
    except NotFound:
        logger.log_resource_not_found_error("VPC", vpc_name)
        return False

    subnet_name = resources["subnet_name"]
    try:
        subnet = factory.compute_v1.SubnetworksClient().get(
            project=project, subnetwork=subnet_name, region=resources["region"]
        )
    except NotFound:
        logger.log_resource_not_found_error("Subnet", subnet_name)
        return False

    if subnet.network != vpc.self_link:
        logger.internal.error(f"Subnet {subnet_name} is not part of {vpc_name}!")
        return False

    return _gcp_subnet_has_enough_capacity(subnet, logger.internal)


def _gcp_subnet_has_enough_capacity(
    subnet: compute_v1.types.compute.Subnetwork, logger: BlockLogger
) -> bool:
    """Verify if the subnet provided has a large enough IP address block."""
    if GCP_SUBNET_CAPACITY.verify_network_capacity(
        cidr_block_str=subnet.ip_cidr_range, resource_name=subnet.name, logger=logger,
    ):
        logger.info(f"Subnet {subnet.name} verification succeeded.")
        return True
    return False


def _verify_gcp_project(
    factory: GoogleCloudClientFactory, resources, logger: GCPLogger
) -> bool:
    """Verify if the project exists and is active.

    NOTE: This also checks that Compute Engine Service Agent is configured in the default way.
    """
    project_client = factory.resourcemanager_v3.ProjectsClient()
    project_id = resources["project_id"]
    try:
        project = project_client.get_project(name=f"projects/{project_id}")
    except (NotFound, PermissionDenied):
        logger.log_resource_not_found_error("Project", project_id)
        return False
    if project.state != project.State.ACTIVE:
        logger.internal.error(
            f"Project {project_id} is in state: {project.state}, not active"
        )
        return False

    iam_policies = project_client.get_iam_policy(resource=f"projects/{project_id}")
    project_number = project.name.split("/")[1]

    if not check_policy_bindings(
        iam_policies.bindings,
        f"serviceAccount:service-{project_number}@compute-system.iam.gserviceaccount.com",
        {"roles/compute.serviceAgent"},
    ):
        logger.internal.warning(
            "The Compute Engine Service Agent does not have the standard IAM Role of 'roles/compute.serviceAgent' in your project.\n"
            "This is not recommended by Google and may result in an inability for Compute Engine to function properly:\n"
            "https://cloud.google.com/compute/docs/access/service-accounts#compute_engine_service_account"
        )

    # TODO: Verify that APIs are Enabled. This will implicitly be verified during other verification steps.
    return True


def _verify_gcp_access_service_account(
    factory: GoogleCloudClientFactory, resources, logger: GCPLogger
) -> bool:
    """Verify if the Service Account meant to grant Anyscale access to this cloud has access to the specified project.

    NOTE: We verify that this service account can call signBlob on itself because this is necessary for downloading logs.
    """
    project_id = resources["project_id"]
    anyscale_access_service_account = resources["anyscale_access_service_account"]

    service_account_client = factory.build("iam", "v1").projects().serviceAccounts()
    try:
        service_account_iam_policy = service_account_client.getIamPolicy(
            resource=f"projects/-/serviceAccounts/{anyscale_access_service_account}"
        ).execute()
    except HttpError as e:
        if e.status_code == 404:
            logger.log_resource_not_found_error(
                "Anyscale Access Service Account", anyscale_access_service_account
            )
            return False

    if not check_policy_bindings(
        binding_from_dictionary(service_account_iam_policy["bindings"]),
        f"serviceAccount:{anyscale_access_service_account}",
        {"roles/iam.serviceAccountTokenCreator"},
    ):
        logger.confirm_missing_permission(
            f"Service Account {anyscale_access_service_account} must have the `iam.serviceAccounts.signBlob` permission to perform log download from the Anyscale platform.\n"
            "Please grant the `roles/iam.serviceAccountTokenCreator` role to this Service Account to pass this check."
        )
        return False

    project_client = factory.resourcemanager_v3.ProjectsClient()
    iam_policies = project_client.get_iam_policy(resource=f"projects/{project_id}")
    if not check_policy_bindings(
        iam_policies.bindings,
        f"serviceAccount:{anyscale_access_service_account}",
        {"roles/editor", "roles/owner"},
    ):
        logger.confirm_missing_permission(
            f"Service Account {anyscale_access_service_account} must have either `roles/editor` or `roles/owner` roles on the Project {project_id}.\n"
            "A more fine-grained set of permissions may be possible, but may break Anyscale's functionality."
        )
        return False

    return True


def _verify_gcp_dataplane_service_account(
    factory: GoogleCloudClientFactory, resources, logger: GCPLogger
) -> bool:
    """Verify that the Service Account for compute instances exists *in* the specified project.

    Compute Engine's ability to use this role
    This relies on the fact that Compute Engine Service Agent has the roles/compute.serviceAgent Role
    """
    service_account = resources["dataplane_service_account"]
    service_account_client = factory.build("iam", "v1").projects().serviceAccounts()
    try:
        resp = service_account_client.get(
            name=f"projects/-/serviceAccounts/{service_account}"
        ).execute()
    except HttpError as e:
        if e.status_code == 404:
            logger.log_resource_not_found_error(
                "Dataplane Service Account", service_account
            )
            return False
        raise e

    cloud_project = resources["project_id"]
    if resp["projectId"] != cloud_project:
        logger.internal.warning(
            "Service Account {} is in project {}, not {}. Please ensure that `constraints/iam.disableCrossProjectServiceAccountUsage` is not enforced.\n"
            "See: https://cloud.google.com/iam/docs/attach-service-accounts#enabling-cross-project for more information.".format(
                service_account, resp["projectId"], cloud_project
            )
        )

    project_client = factory.resourcemanager_v3.ProjectsClient()
    project_iam_bindings = project_client.get_iam_policy(
        resource=f"projects/{cloud_project}"
    )
    if not check_policy_bindings(
        project_iam_bindings.bindings,
        f"serviceAccount:{service_account}",
        {"roles/artifactregistry.reader", "roles/viewer"},
    ):
        logger.internal.warning(
            f"The dataplane Service Account {service_account} does not have `roles/artifactregistry.reader` or `roles/viewer` on {cloud_project}.\n"
            "This is safe to ignore if you are not using your own container images or are configuring access a different way."
        )

    return True


def _verify_firewall_policy(
    factory: GoogleCloudClientFactory, resources: Dict, logger: GCPLogger,
) -> bool:
    """Checks if the given firewall exists at either the Global or Regional level."""
    project = resources["project_id"]
    region = resources["region"]
    firewall_policy = resources["firewall_name"]
    vpc_name = resources["vpc_name"]

    firewall = compute_v1.types.compute.FirewallPolicy()
    try:
        firewall = factory.compute_v1.NetworkFirewallPoliciesClient().get(
            project=project, firewall_policy=firewall_policy
        )
    except NotFound:
        logger.internal.info(
            f"Global firweall policy {firewall_policy} not found, trying in region: {region}."
        )
    if not firewall:
        try:
            firewall = factory.compute_v1.RegionNetworkFirewallPoliciesClient().get(
                project=project, firewall_policy=firewall_policy, region=region
            )
        except NotFound:
            logger.log_resource_not_found_error("FirewallPolicy", firewall_policy)
            return False

    if not any(
        association.name == vpc_name or association.name.split("/")[-1] == vpc_name
        for association in firewall.associations
    ):
        logger.internal.error(
            "Firewall policy {} is not associated with the VPC {}, but is associated with the following VPCs: {}".format(
                firewall_policy, resources["vpc_name"], firewall.associations
            )
        )
        return False

    subnet_obj = factory.compute_v1.SubnetworksClient().get(
        project=project, subnetwork=resources["subnet_name"], region=region
    )
    subnet = ipaddress.ip_network(subnet_obj.ip_cidr_range)

    rules = _firewall_rules_from_proto_resp(firewall.rules)
    if not check_inbound_firewall_permissions(
        rules, Protocol.tcp, {22}, ipaddress.ip_network("0.0.0.0/0")
    ):
        logger.internal.warning(
            "Firewall policy does not allow inbound access on port 22. Certain features may be unavailable."
        )
    if not check_inbound_firewall_permissions(
        rules, Protocol.tcp, {443}, ipaddress.ip_network("0.0.0.0/0")
    ):
        logger.internal.warning(
            "Firewall policy does not allow inbound access on port 443. Accessing features like Jupyter & Ray Dashboard may not work."
        )

    if not check_inbound_firewall_permissions(rules, Protocol.tcp, None, subnet):
        logger.internal.error(
            "Firewall policy does not allow for internal communication, see https://cloud.google.com/vpc/docs/using-firewalls#common-use-cases-allow-internal for how to configure such a rule."
        )
        return False
    return True


def _firewall_rules_from_proto_resp(
    rules: Iterable[compute_v1.types.compute.FirewallPolicyRule],
) -> List[FirewallRule]:
    """Convert Firewall Rules into a Python class suitable for comparison.

    NOTE: We only check "ALLOW" rules & do not check priority.
    """
    return [
        FirewallRule(
            direction=rule.direction,
            protocol=Protocol.from_val(l4config.ip_protocol),
            ports=l4config.ports,
            network=ipaddress.ip_network(addr),
        )
        for rule in rules
        if rule.action == "allow"
        for addr in rule.match.src_ip_ranges
        for l4config in (
            rule.match.layer4_configs
            or [
                compute_v1.types.compute.FirewallPolicyRuleMatcherLayer4Config(
                    ip_protocol="all"
                )
            ]
        )
    ]


def _verify_filestore(
    factory: GoogleCloudClientFactory, resources, logger: GCPLogger
) -> bool:
    """Verify Filestore exists & that it is connected to the correct VPC.

    TODO: Warn about Filestore size if it is 'too small'."""
    file_store_id = resources["filestore_id"]
    client = factory.filestore_v1.CloudFilestoreManagerClient()
    try:
        file_store = client.get_instance(
            name="projects/{}/locations/{}/instances/{}".format(
                resources["project_id"], resources["filestore_location"], file_store_id
            )
        )
    except NotFound:
        logger.log_resource_not_found_error("Filestore", file_store_id)
        return False

    # TODO(ilr) Update to checking if file_store.Tier.ENTERPRISE once google.cloud.file_store>1.5.1 is  released.
    # https://github.com/googleapis/python-filestore/pull/140 Needs to be in the new release
    if int(file_store.tier) != 6:
        logger.internal.warning(
            f"Filestore is running with tier {file_store.tier}, ENTERPRISE is the suggested tier."
        )

    file_store_networks = [v.network for v in file_store.networks]
    vpc_name = resources["vpc_name"]
    if vpc_name not in file_store_networks:
        logger.internal.error(
            f"Filestore is not connected to {vpc_name}, but to {file_store_networks}. "
            f"This cannot be edited on an existing Filestore instance. Please recreate the filestore and connect it to {vpc_name}."
        )
        return False

    return True


def _verify_cloud_storage(
    factory: GoogleCloudClientFactory, resources, logger: GCPLogger
):
    """Verify that the Google Cloud Storage Bucket exists & raises warnings about improper configurations."""
    bucket_client = factory.storage.Client(resources["project_id"])
    bucket_name = resources["bucket_name"]
    try:
        bucket = bucket_client.get_bucket(bucket_name)
    except NotFound:
        logger.log_resource_not_found_error("Google Cloud Storage Bucket", bucket_name)
        return False

    if not bucket.iam_configuration.uniform_bucket_level_access_enabled:
        logger.internal.warning(
            f"Bucket {bucket_name}, does not have Uniform Bucket Access enabled, "
            "this impedes Anyscale's ability to verify bucket access."
        )

    public_access_protection = bucket.iam_configuration.public_access_prevention
    if public_access_protection not in (
        PUBLIC_ACCESS_PREVENTION_INHERITED,
        PUBLIC_ACCESS_PREVENTION_ENFORCED,
    ):
        logger.internal.warning(
            f"Bucket {bucket_name} has public access prevention set to {public_access_protection}, not enforced or inherited."
        )

    cloud_region = resources["region"]
    correct_region, bucket_region = _check_bucket_region(bucket, cloud_region)
    if not correct_region:
        logger.internal.warning(
            f"Bucket {bucket_name} is in region {bucket_region}, but this cloud is being set up in {cloud_region}."
            "This can result in degraded cluster launch & logging performance."
        )

    if not any(
        (
            ANYSCALE_HOST in cors_config.get("origin")
            and "*" in cors_config.get("responseHeader", [])
            and "GET" in cors_config.get("method", [])
        )
        for cors_config in bucket.cors
    ):
        # TODO: Update CORS doc link for GCloud
        logger.internal.warning(
            f"Bucket {bucket_name} does not have the correct CORS rule for Anyscale. This is safe to ignore if you are not using Anyscale UI.\n"
            "If you are using the UI, please create the correct CORS rule for Anyscale according to https://docs.google.com/document/d/12QE0nZwZELvR6ocW_mDISzA568VGOQgwYXECNlvCcVk"
        )

    iam_policy = bucket.get_iam_policy()
    iam_bindings = binding_from_dictionary(iam_policy.bindings)

    permission_warning = (
        "The {location} Service Account {email} requires the following permissions on Bucket {bucket} to operate correctly:\n"
        "* storage.buckets.get\n* storage.objects.[ get | list | create ]\n* storage.multipartUploads.[ abort | create | listParts ]\n"
        "We suggest granting the predefined roles of `roles/storage.legacyBucketReader` and `roles/storage.objectAdmin`."
    )

    access_service_account = resources["anyscale_access_service_account"]
    if not _verify_service_account_on_bucket(access_service_account, iam_bindings):
        logger.confirm_missing_permission(
            permission_warning.format(
                location="Anyscale access",
                email=access_service_account,
                bucket=bucket_name,
            )
        )

    dataplane_service_account = resources["dataplane_service_account"]
    if not _verify_service_account_on_bucket(dataplane_service_account, iam_bindings):
        logger.confirm_missing_permission(
            permission_warning.format(
                location="Dataplane",
                email=dataplane_service_account,
                bucket=bucket_name,
            )
        )

    return True


def _verify_service_account_on_bucket(
    service_account: str, iam_bindings: List[Binding]
) -> bool:
    """Verifies that the given service account has roles that ensure the following list of permissions:
    * storage.buckets.get: Get bucket info
    * storage.objects.[ get | list | create ]
    * storage.multipartUploads.[ abort | create | listParts ]
    """
    if check_policy_bindings(iam_bindings, service_account, {"roles/storage.admin"},):
        return True
    return any(
        check_required_policy_bindings(iam_bindings, service_account, combination)
        for combination in [
            {
                # Best Permissions (legacy for `buckets.get`)
                "roles/storage.legacyBucketReader",
                "roles/storage.objectViewer",
                "roles/storage.objectCreator",
            },
            {
                # Most Brief permissions (legacy for `buckets.get`)
                "roles/storage.objectAdmin",
                "roles/storage.legacyBucketReader",
            },
            {
                # Optimal Legacy Roles
                "roles/storage.legacyBucketWriter",
                "roles/storage.legacyObjectReader",
            },
            {
                # Legacy Roles (extra object permissions)
                "roles/storage.legacyBucketWriter",
                "roles/storage.legacyObjectOwner",
            },
            {
                # Legacy Roles (extra bucket permissions)
                "roles/storage.legacyBucketOwner",
                "roles/storage.legacyObjectReader",
            },
            {
                # Legacy Roles (extra bucket/object permissions)
                "roles/storage.legacyBucketOwner",
                "roles/storage.legacyObjectOwner",
            },
        ]
    )


def _check_bucket_region(bucket: Bucket, region: str) -> Tuple[bool, str]:
    if bucket.location_type == "dual-region":
        return region.upper() in bucket.data_locations, ",".join(bucket.data_locations)
    elif bucket.location_type == "region":
        return region.upper() == bucket.location, bucket.location

    # Bucket is `multi-region`, so check if the location (`EU`, `ASIA`, `US`)
    # is the 'prefix' of the region.
    return region.upper().startswith(bucket.location), bucket.location
