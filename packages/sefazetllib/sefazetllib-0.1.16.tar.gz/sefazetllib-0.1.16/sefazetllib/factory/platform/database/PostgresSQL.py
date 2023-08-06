from sefazetllib.factory.platform.DatabasePlatform import DatabasePlatform


class PostgreSQL(DatabasePlatform):
    def __init__(self, name="PostgreSQL Job", configs=[]) -> None:
        self.name = name
        self.session = None

    def get_url(self, **kwargs):
        host = kwargs["host"]
        port = kwargs["port"]
        format = kwargs["format"]
        operator = kwargs["operator"]
        database = kwargs["database"].lower()
        instance = kwargs["instance"]
        return f"{format}{operator}{database}://{host}:{port}/{instance}"

    def get_table_name(self, **kwargs):
        schema = kwargs["schema"]
        table = kwargs["table"]
        return f"{schema}.{table}"

    def read(self, **kwargs):
        pass

    def load(self, **kwargs):
        pass
