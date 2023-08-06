from unittest.mock import patch

import pytest
from castor_extractor.visualization.looker import (  # type: ignore
    ApiClient,
    Credentials,
)


def _credentials():
    return Credentials(
        base_url="base_url",
        client_id="client_id",
        client_secret="secret",
    )


@patch("castor_extractor.visualization.looker.api.client.init40")
@patch("castor_extractor.visualization.looker.api.client.has_admin_permissions")
def test_api_client_has_admin_permissions(
    mock_has_admin_permission, mock_init40
):
    mock_has_admin_permission.return_value = False
    with pytest.raises(PermissionError):
        ApiClient(_credentials())

    mock_has_admin_permission.return_value = True
    mock_init40.return_value = "sdk"
    client = ApiClient(_credentials())
    assert client._sdk == "sdk"
