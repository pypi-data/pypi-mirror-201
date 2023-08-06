"""Tests related to pod creation/instantiation."""
from pathlib import Path
from typing import Final
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from pytest import fixture
import responses
from responses import matchers

from bitfount.runners.config_schemas import PodConfig
from bitfount.runners.pod_runner import setup_pod_from_config
from bitfount.types import _S3PresignedPOSTFields, _S3PresignedPOSTURL
from tests.integration import CONFIG_DIR
from tests.integration.utils import load_pod_config
from tests.utils.helper import integration_test

BASE_URL: Final[str] = "https://not-a-real-url.com"


@fixture(autouse=True)
def patch_get_access_manager_key(
    monkeypatch: MonkeyPatch, access_manager_public_key: RSAPublicKey
) -> None:
    """Patch get_access_manager_key."""
    import bitfount.hub.api as api_

    monkeypatch.setattr(
        api_.BitfountAM,
        "get_access_manager_key",
        lambda x: access_manager_public_key,
    )


@fixture(autouse=True)
def set_bitfount_env(monkeypatch: MonkeyPatch) -> None:
    """This (un)sets the environment variable for the following tests.

    This forces the URLs to be those used in the YAML config.

    This shouldn't matter as we mock out all interactions, but guarantees we have
    a known set of URLs to mock.
    """
    monkeypatch.delenv("BITFOUNT_ENVIRONMENT", raising=False)


@integration_test
class TestPodConfigLoading:
    """Tests related to pod creation/instantiation from YAML."""

    @fixture
    def multidataset_pod_config(self, census_income_data: Path) -> PodConfig:
        """Multidataset pod config to use for tests."""
        pod_config = load_pod_config(
            CONFIG_DIR / "pod_census_income_multidatasource.yaml", census_income_data
        )
        return pod_config

    @responses.activate
    def test_multidataset_yaml_pod_creation(
        self,
        multidataset_pod_config: PodConfig,
        patch__create_bitfount_session_in_helper: Mock,
    ) -> None:
        """Test the creation of a multidataset pod.

        Checks:
            - that two logical pods are registered
            - both datasources are loaded and available
        """
        # Add endpoints for pod registration
        reg_1 = responses.add(
            "POST",
            f"{BASE_URL}/api/pods",
            match=(
                matchers.json_params_matcher(
                    {
                        "name": "e2e-csv-datasource",
                        "podDisplayName": "A test datasource",
                    },
                    strict_match=False,
                ),
            ),
            json={
                "success": True,
                "message": "Success!",
                "alreadyExisted": False,
                "uploadUrl": _S3PresignedPOSTURL("https://s3-upload_url.com"),
                "uploadFields": _S3PresignedPOSTFields({}),
            },
        )
        reg_2 = responses.add(
            "POST",
            f"{BASE_URL}/api/pods",
            match=(
                matchers.json_params_matcher(
                    {
                        "name": "e2e-csv-datasource-2",
                        "podDisplayName": "A test datasource 2",
                    },
                    strict_match=False,
                ),
            ),
            json={
                "success": True,
                "message": "Success!",
                "alreadyExisted": False,
                "uploadUrl": _S3PresignedPOSTURL("https://s3-upload_url-2.com"),
                "uploadFields": _S3PresignedPOSTFields({}),
            },
        )

        # Add endpoint for schema upload(s)
        schema_upload_1 = responses.add("POST", "https://s3-upload_url.com")
        schema_upload_2 = responses.add("POST", "https://s3-upload_url-2.com")

        pod = setup_pod_from_config(multidataset_pod_config)

        # Check that pod has both datasources
        assert len(pod.datasources) == 2
        assert "e2e-csv-datasource" in pod.datasources
        assert "e2e-csv-datasource-2" in pod.datasources
        ds_configs = list(pod.datasources.values())
        assert ds_configs[0] != ds_configs[1]

        # Check that both datasources were registered
        assert reg_1.call_count == 1
        assert reg_2.call_count == 1
        # Check that both schemas were uploaded
        assert schema_upload_1.call_count == 1
        assert schema_upload_2.call_count == 1
