from click import ClickException
from google.api_core.exceptions import NotFound
import pytest

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)
from anyscale.utils.gcp_utils import get_gcp_filestore_config


@pytest.mark.parametrize(
    ("filestore_id", "response", "not_found", "expected_result"),
    [
        pytest.param(
            "regional-filestore",
            ("200 OK", "regional_filestore.json"),
            False,
            GCPFileStoreConfig(
                instance_name="projects/anyscale-bridge-deadbeef/locations/us-central1/instances/regional-filestore",
                root_dir="something",
                mount_target_ip="172.22.236.2",
            ),
            id="regional",
        ),
        pytest.param(
            "zonal-filestore",
            ("200 OK", "zonal_filestore.json"),
            False,
            GCPFileStoreConfig(
                instance_name="projects/anyscale-bridge-deadbeef/locations/us-central1/instances/zonal-filestore",
                root_dir="test",
                mount_target_ip="172.27.155.250",
            ),
            id="zonal",
        ),
        pytest.param(
            "regional-filestore",
            ("200 OK", "regional_filestore_wrong_vpc.json"),
            False,
            None,
            id="wrong_vpc",
        ),
        pytest.param(
            "regional-filestore", ("404 Not Found", None), True, None, id="not_found"
        ),
    ],
)
def test_get_gcp_filestore_config(
    setup_mock_server, filestore_id, capsys, response, not_found, expected_result,
):
    factory, tracker = setup_mock_server
    mock_project_id = "anyscale-bridge-deadbeef"
    mock_vpc_name = "vpc_one"
    mock_filestore_region = "us-central1"
    tracker.reset({".*": [response]})
    if expected_result:
        assert (
            get_gcp_filestore_config(
                factory,
                mock_project_id,
                mock_vpc_name,
                mock_filestore_region,
                filestore_id,
                BlockLogger(),
            )
            == expected_result
        )
    else:
        if not_found:
            with pytest.raises(NotFound):
                get_gcp_filestore_config(
                    factory,
                    mock_project_id,
                    mock_vpc_name,
                    mock_filestore_region,
                    filestore_id,
                    BlockLogger(),
                )
            _, err = capsys.readouterr()
            assert "Could not find Filestore with id" in err
        else:
            with pytest.raises(ClickException):
                get_gcp_filestore_config(
                    factory,
                    mock_project_id,
                    mock_vpc_name,
                    mock_filestore_region,
                    filestore_id,
                    BlockLogger(),
                )
            _, err = capsys.readouterr()
            assert "This cannot be edited on an existing Filestore instance." in err
