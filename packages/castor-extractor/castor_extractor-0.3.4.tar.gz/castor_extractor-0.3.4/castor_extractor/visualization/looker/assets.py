from enum import Enum


class LookerAsset(Enum):
    """Looker assets"""

    DASHBOARDS = "dashboards"
    EXPLORES = "explores"
    FOLDERS = "folders"
    LOOKS = "looks"
    LOOKML_MODELS = "lookml_models"
    USERS = "users"
    CONNECTIONS = "connections"
    PROJECTS = "projects"
    GROUPS_HIERARCHY = "groups_hierarchy"
    GROUPS_ROLES = "groups_roles"
