"""
    File regrouping all constants used in PowerBi client
"""

DEFAULT_TIMEOUT_IN_SECS = 30
SCAN_READY = "Succeeded"
# ModifiedSince params should not be older than 30 days
RECENT_DAYS = 30

GET = "GET"
POST = "POST"


class Urls:
    """PowerBi's urls"""

    REST_API_BASE_PATH = "https://api.powerbi.com/v1.0/myorg"
    CLIENT_APP_BASE = "https://login.microsoftonline.com/"
    DEFAULT_SCOPE = "https://analysis.windows.net/powerbi/api/.default"

    # PBI rest API Routes
    REPORTS = f"{REST_API_BASE_PATH}/admin/reports"
    DASHBOARD = f"{REST_API_BASE_PATH}/admin/dashboards"
    GROUPS = f"{REST_API_BASE_PATH}/admin/groups"
    METADATA_POST = f"{REST_API_BASE_PATH}/admin/workspaces/getInfo"
    METADATA_WAIT = f"{REST_API_BASE_PATH}/admin/workspaces/scanStatus"
    METADATA_GET = f"{REST_API_BASE_PATH}/admin/workspaces/scanResult"
    WORKSPACE_IDS = (
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified"
    )


class Batches:
    """Batches used within PowerBI api calls"""

    DEFAULT = 100
    # The route we use to fetch workspaces info can retrieve a maximum of
    # 100 workspaces per call
    # More: https://learn.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-post-workspace-info#request-body
    METADATA = 100


class QueryParams:
    """
    Frequently used PowerBi query params
    """

    METADATA_SCAN = {
        "datasetExpressions": True,
        "datasetSchema": True,
        "datasourceDetails": True,
        "getArtifactUsers": True,
        "lineage": True,
    }
    ACTIVE_WORKSPACE_FILTER = "state eq 'Active' and type eq 'Workspace'"


class Keys:
    ACCESS_TOKEN = "access_token"
    VALUE = "value"
    WORKSPACES = "workspaces"
    INACTIVE_WORKSPACES = "excludeInActiveWorkspaces"
    PERSONAL_WORKSPACES = "excludePersonalWorkspaces"
    MODIFIED_SINCE = "modifiedSince"
    ID = "id"
    STATUS = "status"


class Assertions:
    """Assertion's messages"""

    BATCH_TOO_BIG = f"Can not retrieve more than {Batches.METADATA} at the time"
    DATETIME_TOO_OLD = "Date must be within 30 days range"
