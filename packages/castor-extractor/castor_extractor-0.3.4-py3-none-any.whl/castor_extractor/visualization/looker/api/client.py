import logging
from typing import Callable, Iterator, List, Optional, Sequence, Tuple

from ....utils import Pager, PagerLogger, SafeMode, safe_mode
from ..env import page_size
from ..fields import format_fields
from .constants import (
    CONNECTION_FIELDS,
    DASHBOARD_FIELDS,
    FOLDER_FIELDS,
    GROUPS_HIERARCHY_FIELDS,
    GROUPS_ROLES_FIELDS,
    LOOK_FIELDS,
    LOOKML_FIELDS,
    LOOKML_PROJECT_NAME_BLOCKLIST,
    PROJECT_FIELDS,
    USER_FIELDS,
)
from .sdk import (
    Credentials,
    Dashboard,
    DBConnection,
    Folder,
    GroupHierarchy,
    GroupSearch,
    Look,
    LookmlModel,
    LookmlModelExplore,
    Project,
    User,
    has_admin_permissions,
    init40,
)

logger = logging.getLogger(__name__)


OnApiCall = Callable[[], None]


class ApiPagerLogger(PagerLogger):
    def __init__(self, on_api_call: Optional[OnApiCall]):
        self._on_api_call = on_api_call

    def on_page(self, page: int, count: int):
        logger.info(f"Fetched page {page} / {count} results")
        self._on_api_call and self._on_api_call()

    def on_success(self, page: int, total: int):
        logger.info(f"All page fetched: {page} pages / {total} results")


class ApiClient:
    """Looker client"""

    def __init__(
        self,
        credentials: Credentials,
        on_api_call: OnApiCall = lambda: None,
        safe_mode: Optional[SafeMode] = None,
    ):
        sdk = init40(credentials)
        if not has_admin_permissions(sdk):
            raise PermissionError("User does not have admin access.")
        else:
            self._sdk = sdk
        self._on_api_call = on_api_call
        self._logger = ApiPagerLogger(on_api_call)
        self.per_page = page_size()
        self._safe_mode = safe_mode

    def folders(self) -> List[Folder]:
        """Lists folders of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[Folder]:
            return self._sdk.search_folders(
                fields=format_fields(FOLDER_FIELDS),
                per_page=per_page,
                page=page,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def dashboards(self) -> List[Dashboard]:
        """Lists dashboards of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[Dashboard]:
            return self._sdk.search_dashboards(
                fields=format_fields(DASHBOARD_FIELDS),
                per_page=per_page,
                page=page,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def _search_looks(self) -> List[Look]:
        """
        fetch looks via `search_looks`
        https://developers.looker.com/api/explorer/4.0/methods/Look/search_looks
        """

        def _search(page: int, per_page: int) -> Sequence[Look]:
            return self._sdk.search_looks(
                fields=format_fields(LOOK_FIELDS), per_page=per_page, page=page
            )

        logger.info("Use search_looks endpoint to retrieve Looks")
        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def _all_looks(self) -> List[Look]:
        """
        fetch looks via `all_looks`
        https://castor.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/Look/all_looks
        """
        logger.info("Use all_looks endpoint to retrieve Looks")

        # No pagination : see https://community.looker.com/looker-api-77/api-paging-limits-14598
        return list(self._sdk.all_looks(fields=format_fields(LOOK_FIELDS)))

    def looks(self, all_looks_endpoint: Optional[bool] = False) -> List[Look]:
        """Lists looks of the given Looker account

        By default, uses the endpoint `search_looks` that allow pagination.
        If `all_looks_endpoint` parameter is set to True, it uses `all_looks` endpoint.
        """
        if all_looks_endpoint:
            return self._all_looks()

        return self._search_looks()

    def users(self) -> List[User]:
        """Lists users of the given Looker account"""

        def _search(page: int, per_page: int) -> Sequence[User]:
            # HACK:
            # We use verified_looker_employee=False (filter out Looker employees)
            # Else api returns an empty list when no parameters are specified
            return self._sdk.search_users(
                fields=format_fields(USER_FIELDS),
                per_page=per_page,
                page=page,
                verified_looker_employee=False,
            )

        return Pager(_search, logger=self._logger).all(per_page=self.per_page)

    def lookml_models(self) -> List[LookmlModel]:
        """Iterates LookML models of the given Looker account"""

        models = self._sdk.all_lookml_models(
            fields=format_fields(LOOKML_FIELDS)
        )

        logger.info("All LookML models fetched")
        self._on_api_call()

        return [
            model
            for model in models
            if model.project_name not in LOOKML_PROJECT_NAME_BLOCKLIST
        ]

    def explores(
        self, explore_names=Iterator[Tuple[str, str]]
    ) -> List[LookmlModelExplore]:
        """Iterates explores of the given Looker account for the provided model/explore names"""

        @safe_mode(self._safe_mode)
        def _call(model_name: str, explore_name: str) -> LookmlModelExplore:

            explore = self._sdk.lookml_model_explore(model_name, explore_name)

            logger.info(f"Explore {model_name}/{explore_name} fetched")
            self._on_api_call()
            return explore

        explores = [
            _call(model_name, explore_name)
            for model_name, explore_name in explore_names
        ]
        return list(filter(None, explores))

    def connections(self) -> List[DBConnection]:
        """Lists databases connections of the given Looker account"""

        connections = self._sdk.all_connections(
            fields=format_fields(CONNECTION_FIELDS)
        )

        logger.info("All looker connections fetched")
        self._on_api_call()

        return list(connections)

    def projects(self) -> List[Project]:
        """Lists projects of the given Looker account"""

        projects = self._sdk.all_projects(fields=format_fields(PROJECT_FIELDS))

        logger.info("All looker projects fetched")
        self._on_api_call()

        return list(projects)

    def groups_hierarchy(self) -> List[GroupHierarchy]:
        """Lists groups with hierarchy of the given Looker account"""
        groups_hierarchy = self._sdk.search_groups_with_hierarchy(
            fields=format_fields(GROUPS_HIERARCHY_FIELDS)
        )
        logger.info("All looker groups_hierarchy fetched")
        return list(groups_hierarchy)

    def groups_roles(self) -> List[GroupSearch]:
        """Lists groups with roles of the given Looker account"""
        groups_roles = self._sdk.search_groups_with_roles(
            fields=format_fields(GROUPS_ROLES_FIELDS)
        )
        logger.info("All looker groups_roles fetched")
        return list(groups_roles)
