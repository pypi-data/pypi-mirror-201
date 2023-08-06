from typing import Any, Dict, List

from sefazetllib.Builder import Builder, field
from sefazetllib.factory.platform.dataframe.Default import Default
from sefazetllib.factory.platform.Platform import Platform
from sefazetllib.factory.platform.PlatformFactory import PlatformFactory
from sefazetllib.load.Load import Load
from sefazetllib.utils.key import DefaultKey, Key


@Builder
class LoadSQL(Load):
    platform: Platform = field(default=Default())
    format: str = field(default="jdbc")
    operator: str = field(default=":")
    host: str = field(default="")
    port: int = field(default=0)
    database: str = field(default="")
    instance: str = field(default="")
    driver: str = field(default="")
    schema: str = field(default="")
    table: str = field(default="")
    authentication: Dict[str, Any] = field(default_factory=dict)
    url: str = field(default="")
    reference: str = field(default="")
    df_writer: Any = field(default="")
    mode: str = field(default="")
    key: Key = field(default=DefaultKey())
    columns: List[str] = field(default_factory=list)
    operation: bool = field(default=False)
    optional: bool = field(default=False)
    duplicates: bool = field(default=False)

    def __build_properties(self):
        return {
            "operation": self.operation,
            "database": self.database,
            "driver": self.driver,
            "user": self.authentication["user"],
            "password": self.authentication["password"],
            "dbtable": self.table,
            "url": self.url,
        }

    def build_connection_string(self):
        platform_db = PlatformFactory(self.database).create(
            name="get url jdbc",
        )
        self.url = platform_db.get_url(
            format=self.format,
            operator=self.operator,
            database=self.database,
            host=self.host,
            instance=self.instance,
            schema=self.schema,
            port=self.port,
        )

        self.table = platform_db.get_table_name(table=self.table, schema=self.schema)

    def execute(self, **kwargs):
        if isinstance(self.platform, Default):
            self.setPlatform(kwargs["platform"])

        sk_name = f"SK_{self.table}"
        if "/" in self.table:
            table = self.table.split("/")[1]
            sk_name = f"SK_{table}"

        self.build_connection_string()

        return self.reference, self.platform.load(
            df=self.df_writer,
            sk_name=sk_name,
            key=self.key,
            columns=self.columns,
            duplicates=self.duplicates,
            format=self.format,
            format_properties=self.__build_properties(),
            url=None,
            mode=self.mode,
        )
