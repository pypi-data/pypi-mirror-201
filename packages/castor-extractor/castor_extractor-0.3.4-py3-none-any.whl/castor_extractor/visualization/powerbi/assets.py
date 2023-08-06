from enum import Enum


class PowerBiAsset(Enum):
    """PowerBi assets"""

    REPORTS = "reports"
    DASHBOARDS = "dashboards"
    USERS = "users"
    TABLES = "tables"
    METADATA = "metadata"


class MetadataAsset(Enum):
    """
    Assets extracted from the Metadata file, they are not directly fetch
    from the PowerBi api.
    """

    USERS = "users"
    TABLES = "tables"
