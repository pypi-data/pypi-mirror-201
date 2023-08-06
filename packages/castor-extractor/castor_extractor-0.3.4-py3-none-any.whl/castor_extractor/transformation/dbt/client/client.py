from enum import Enum
from typing import Optional

import requests

from .credentials import CredentialsKey, DbtCredentials, get_value

_CLOUD_URL = "https://cloud.getdbt.com/api/v2/accounts"
_DATA_KEY = "data"
_MANIFEST_PATH = "manifest.json"


class ContentType(Enum):
    JSON = "application/json"
    TEXT = "text/html"


class DbtClient:
    """
    Connect to dbt-cloud Administrative API and downloads manifest.
    https://docs.getdbt.com/docs/dbt-cloud-apis/admin-cloud-api
    """

    def __init__(self, **kwargs):
        self._credentials = DbtCredentials(
            token=get_value(CredentialsKey.TOKEN, kwargs),
            job_id=get_value(CredentialsKey.JOB_ID, kwargs),
        )
        self._session = requests.Session()
        self._account_id: int = self._infer_account_id()

    def _headers(self, content_type: ContentType) -> dict:
        return {
            "Accept": content_type.value,
            "Authorization": "Token " + self._credentials.token,
        }

    def _call(
        self,
        url: str,
        params: Optional[dict] = None,
        content_type: ContentType = ContentType.JSON,
    ) -> dict:
        headers = self._headers(content_type)
        response = self._session.get(
            url=url,
            headers=headers,
            params=params,
        )
        result = response.json()
        if content_type == ContentType.JSON:
            return result[_DATA_KEY]
        return result

    def _infer_account_id(self) -> int:
        result = self._call(url=_CLOUD_URL)
        return result[0]["id"]

    def _last_run_id(self) -> int:
        url = f"{_CLOUD_URL}/{self._account_id}/runs/"
        params = {
            "job_definition_id": self._credentials.job_id,
            "order_by": "-finished_at",
            "limit": 1,
        }
        return self._call(url, params)[0]["id"]

    def fetch_manifest(self) -> dict:
        """
        Fetch dbt manifest
        https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getArtifactsByRunId
        """
        run_id = self._last_run_id()
        url = f"{_CLOUD_URL}/{self._account_id}/runs/{run_id}/artifacts/{_MANIFEST_PATH}"
        # setting text content as a workaround to this issue
        # https://stackoverflow.com/questions/68201659/dbt-cloud-api-to-extract-run-artifacts
        return self._call(url, content_type=ContentType.TEXT)
