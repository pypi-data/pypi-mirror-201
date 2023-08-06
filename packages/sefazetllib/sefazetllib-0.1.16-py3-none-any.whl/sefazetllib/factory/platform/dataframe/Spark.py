from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    current_date,
    lit,
    monotonically_increasing_id,
    xxhash64,
)
from pyspark.sql.types import StructType

from sefazetllib.config.CustomLogging import logger
from sefazetllib.factory.platform.Platform import Platform


class Spark(Platform):
    def __init__(self, name="Spark Job", configs=[]) -> None:
        self.name = name
        session = SparkSession.builder.appName(name)
        if configs != []:
            for config in configs:
                session = session.config(*config)
        self.session = session.getOrCreate()

    def __get_key_method(self, name):
        return {
            "SurrogateKey": xxhash64,
            "IncrementalKey": monotonically_increasing_id,
        }[name]

    def __define_properties(self, df, type_format, url, properties):
        if type_format == "jdbc":
            properties.pop("operation", None)
        return df.options(**properties)

    def __define_load(self, df, type_format, url):
        if type_format == "jdbc":
            return df.load()
        return df.load(url)

    def __define_save(self, df, type_format, url):
        if type_format == "jdbc":
            return df.save()
        return df.save(url)

    def read(self, **kwargs):
        type_format = kwargs["file_format"]
        url = kwargs["url"]
        format_properties = kwargs["format_properties"]
        optional = kwargs["optional"]
        columns = kwargs["columns"]
        duplicates = kwargs["duplicates"]

        df = self.session.read.format(type_format)

        if bool(format_properties):
            df = self.__define_properties(df, type_format, url, format_properties)

        try:
            df = self.__define_load(df, type_format, url)

            if bool(columns):
                df = df.select(columns)

            if duplicates:
                df = df.dropDuplicates()
            return df

        except Exception as e:
            if not optional:
                logger.error("The 'optional' attribute is set to False. Error: %s", e)
                raise
            schema = StructType([])
            df = self.session.createDataFrame([], schema)
            for cols in columns:
                df = df.withColumn(cols, lit(None))
            return df

    def load(self, **kwargs):
        df = kwargs["df"]
        sk_name = kwargs["sk_name"]
        key = kwargs["key"]
        columns = kwargs["columns"]
        duplicates = kwargs["duplicates"]
        type_format = kwargs["file_format"]
        format_properties = kwargs["format_properties"]
        url = kwargs["url"]
        mode = kwargs["mode"]

        if key.name is not None:
            sk_name = key.name

        key.setMethod(self.__get_key_method(type(key).__name__))

        df_writer = df.withColumn("DAT_CARGA", current_date()).withColumn(
            sk_name, key.get()
        )

        if bool(columns):
            df_writer = df_writer.select(sk_name, *columns, "DAT_CARGA")

        if duplicates:
            df_writer = df_writer.dropDuplicates()

        if (
            "operation" in format_properties
            and format_properties["operation"] == "upsert"
        ):
            df_old = self.read(
                format=type_format,
                url=url,
                format_properties={**format_properties},
                optional=True,
                columns=df_writer.columns,
                duplicates=duplicates,
            ).drop("DAT_CARGA")

            df_writer = df_writer.join(df_old, sk_name, "full")

            for column in columns:
                df_writer = df_writer.drop(df_old[column])

        writer_format = df_writer.write.format(type_format)

        if bool(format_properties):
            writer_format = self.__define_properties(
                writer_format, type_format, url, format_properties
            )

        if mode is not None:
            writer_format = writer_format.mode(mode)

        self.__define_save(writer_format, type_format, url)

        return df_writer
