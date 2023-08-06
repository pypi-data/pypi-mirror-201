from enum import Enum


class TableauAsset(Enum):
    """
    Tableau assets
    """

    CUSTOM_SQL_TABLE = "custom_sql_tables"
    CUSTOM_SQL_QUERY = "custom_sql_queries"
    DATASOURCE = "datasources"
    FIELD = "fields"
    PROJECT = "projects"
    PUBLISHED_DATASOURCE = "published_datasources"
    USAGE = "views"
    USER = "users"
    WORKBOOK = "workbooks"
    WORKBOOK_TO_DATASOURCE = "workbooks_to_datasource"


class TableauGraphqlAsset(Enum):
    """
    Assets which can be fetched from Tableau
    """

    BIN_FIELD = "binFields"
    CALCULATED_FIELD = "calculatedFields"
    COLUMN_FIELD = "columnFields"
    CUSTOM_SQL = "customSQLTables"
    DATASOURCE = "datasources"
    GROUP_FIELD = "groupFields"
    WORKBOOK_TO_DATASOURCE = "workbooks"
