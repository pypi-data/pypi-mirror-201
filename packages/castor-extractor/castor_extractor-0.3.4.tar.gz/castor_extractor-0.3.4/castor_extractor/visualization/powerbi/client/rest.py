import logging
from datetime import datetime
from time import sleep
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

import msal  # type: ignore
import requests

from ..assets import PowerBiAsset
from .constants import (
    DEFAULT_TIMEOUT_IN_SECS,
    GET,
    POST,
    SCAN_READY,
    Batches,
    Keys,
    QueryParams,
    Urls,
)
from .credentials import Credentials
from .utils import batch_size_is_valid_or_assert, datetime_is_recent_or_assert

logger = logging.getLogger(__name__)


class Client:
    """
    PowerBI rest admin api
    https://learn.microsoft.com/en-us/rest/api/power-bi/admin
    """

    def __init__(self, credentials: Credentials):
        self.creds = credentials

    def _access_token(self) -> dict:
        client_app = f"{Urls.CLIENT_APP_BASE}{self.creds.tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=self.creds.client_id,
            authority=client_app,
            client_credential=self.creds.secret,
        )

        token = app.acquire_token_silent(self.creds.scopes, account=None)

        if not token:
            token = app.acquire_token_for_client(scopes=self.creds.scopes)

        return token

    def _header(self) -> Dict:
        """Return header used in following rest api call"""
        token = self._access_token()
        return {"Authorization": f"Bearer {token[Keys.ACCESS_TOKEN]}"}

    def _call(
        self,
        url: str,
        method: str = GET,
        *,
        params: Optional[Dict] = None,
        data: Optional[dict] = None,
        processor: Optional[Callable] = None,
    ) -> Any:
        """
        Make either a get or a post http request.Request, by default
        result.json is returned. Optionally you can provide a processor callback
        to transform the result.
        """
        result = requests.request(
            method, url, headers=self._header(), params=params, data=data
        )
        result.raise_for_status()

        if processor:
            return processor(result)

        return result.json()

    def _get(
        self,
        url: str,
        *,
        params: Optional[Dict] = None,
        processor: Optional[Callable] = None,
    ) -> Any:
        return self._call(url, GET, params=params, processor=processor)

    def _post(
        self,
        url: str,
        *,
        params: Optional[dict],
        data: Optional[dict],
        processor: Optional[Callable] = None,
    ) -> Any:
        return self._call(
            url, POST, params=params, data=data, processor=processor
        )

    def _workspace_ids(
        self, modified_since: Optional[datetime] = None
    ) -> List[str]:
        """
        Get workspaces ids from powerBI admin API.
        If modified_since, take only workspaces that have been modified since

        more: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-modified-workspaces
        """

        def result_callback(call_result: requests.models.Response) -> List[str]:
            return [x["id"] for x in call_result.json()]

        params: Dict[str, Union[bool, str]] = {
            Keys.INACTIVE_WORKSPACES: True,
            Keys.PERSONAL_WORKSPACES: True,
        }

        if modified_since:
            datetime_is_recent_or_assert(modified_since)
            modified_since_iso = f"{modified_since.isoformat()}0Z"
            params[Keys.MODIFIED_SINCE] = modified_since_iso

        result = self._get(
            Urls.WORKSPACE_IDS,
            params=params,
            processor=result_callback,
        )

        return result

    def _create_scan(self, workspaces_ids: List[str]) -> int:
        batch_size_is_valid_or_assert(workspaces_ids)
        request_body = {"workspaces": workspaces_ids}
        params = QueryParams.METADATA_SCAN
        scan_id = self._post(
            Urls.METADATA_POST,
            params=params,
            data=request_body,
        )
        return scan_id[Keys.ID]

    def _wait_for_scan_result(self, scan_id: int) -> bool:
        url = f"{Urls.METADATA_WAIT}/{scan_id}"
        waiting_seconds = 0
        sleep_seconds = 1
        while True:
            result = self._get(url, processor=lambda x: x)
            if result.status_code != 200:
                return False
            if result.json()[Keys.STATUS] == SCAN_READY:
                logger.info(f"scan {scan_id} ready")
                return True
            if waiting_seconds >= DEFAULT_TIMEOUT_IN_SECS:
                break
            waiting_seconds += sleep_seconds
            logger.info(
                f"Waiting {sleep_seconds} sec for scan {scan_id} to be ready..."
            )
            sleep(sleep_seconds)
        return False

    def _get_scan(self, scan_id: int) -> List[dict]:
        url = f"{Urls.METADATA_GET}/{scan_id}"
        return self._get(url)[Keys.WORKSPACES]

    def _reports(self) -> List[Dict]:
        """
        Returns a list of reports for the organization.
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-reports-as-admin
        """
        return self._get(Urls.REPORTS)[Keys.VALUE]

    def _dashboards(self) -> List[Dict]:
        """
        Returns a list of dashboards for the organization.
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/dashboards-get-dashboards-as-admin
        """
        return self._get(Urls.DASHBOARD)[Keys.VALUE]

    def _metadata(
        self, modified_since: Optional[datetime] = None
    ) -> Iterator[List[Dict]]:
        """
        Fetch metadata by workspace.
        https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-metadata-scanning
        """
        ids = self._workspace_ids(modified_since)

        for ix in range(0, len(ids), Batches.METADATA):
            batch_ids = [w_id for w_id in ids[ix : ix + Batches.METADATA]]
            scan_id = self._create_scan(batch_ids)
            self._wait_for_scan_result(scan_id)
            yield self._get_scan(scan_id)

    def fetch(
        self, asset: PowerBiAsset, modified_since: datetime = None
    ) -> List[Dict]:
        """
        Given a PowerBi asset, returns the corresponding data using the
        appropriate client.
        """
        asset = PowerBiAsset(asset)

        if asset == PowerBiAsset.DASHBOARDS:
            return self._dashboards()

        if asset == PowerBiAsset.REPORTS:
            return self._reports()

        assert asset == PowerBiAsset.METADATA
        return [
            item for batch in self._metadata(modified_since) for item in batch
        ]
