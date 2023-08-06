from typing import List

from .constants import Urls


class Credentials:
    """Class to handle PowerBI rest API permissions"""

    def __init__(
        self,
        *,
        tenant_id: str,
        client_id: str,
        secret: str,
        scopes: List[str] = None,
    ):

        if scopes is None:
            scopes = [Urls.DEFAULT_SCOPE]

        self.tenant_id = tenant_id
        self.client_id = client_id
        self.secret = secret
        self.scopes = scopes
