from fluvii.components.sqlite import SqliteConfig


class NubiumSqliteConfig(SqliteConfig):
    """Just updated defaults"""
    table_directory: str = '/opt/app-root/data'
