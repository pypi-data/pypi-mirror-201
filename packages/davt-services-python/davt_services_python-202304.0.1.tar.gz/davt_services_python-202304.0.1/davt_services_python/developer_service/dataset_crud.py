""" Module with a variety of create, read, update and delete
functions for Spark data frames. """

import sys  # don't remove required for error handling
import os


from pathlib import Path
from urllib.parse import urlparse
from io import BytesIO

# types
import json
from collections import defaultdict

# libraries
from importlib import util

# util
import hashlib

# adls and azure security
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

# file excel
import openpyxl
import openpyxl.utils.cell

# DAVT
import davt_services_python.developer_service.dataset_core as davt_ds_core
import davt_services_python.developer_service.environment_file as davt_env_file
import davt_services_python.developer_service.security_core as davt_sec_core
import davt_services_python.developer_service.environment_core as davt_env_core

# spark / data
import uuid
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.utils
import pyspark.sql.functions as f
from pyspark.sql.functions import (
    col,
    lit,
    concat_ws,
    udf
)

from pyspark.sql.types import StructType, StructField, LongType, StringType
uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())

from delta.tables import DeltaTable
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    import pyspark.pandas as pd
    # bug - pyspark version will not read local files in the repo
    # import pandas as pd
else:
    import pandas as pd


class DataSetCrud:
    """DataSetCrud class for Spark Datasets handling create, read, update and delete operations
    """

    @classmethod
    def upsert(
        cls,
        spark,
        config,
        dbutils,
        df_crud,
        full_dataset_name,
        dataset_file_path,
        is_using_dataset_folder_path_override,
        file_format,
        source_abbreviation,
        ingress_file_path,
        is_drop,
        partition_by,
        incremental
    ):
        """Inserts a record if it does not exist or updates the record if it exists. Stores the Dataframe as
        Delta dataset if the path is empty or tries to merge the data if found

        Args:
            spark (_type_): _description_
            config (_type_): _description_
            dbutils (_type_): _description_
            df_crud (_type_): _description_
            full_dataset_name (_type_): _description_
            dataset_file_path (_type_): _description_
            is_using_dataset_folder_path_override (bool): _description_
            file_format (_type_): _description_
            source_abbreviation (_type_): _description_
            is_drop (bool, optional): _description_. Defaults to False.
            partition_by (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """

        obj_ds_core = davt_ds_core.DataSetCore()
        obj_env_file = davt_env_file.EnvironmentFile()

        yyyy_param = config["yyyy"]
        mm_param = config["mm"]
        dd_param = config["dd"]

        if yyyy_param is None:
            yyyy_param = ""

        if mm_param is None:
            mm_param = ""

        if dd_param is None:
            dd_param = ""

        dataset_name_list = full_dataset_name.split(".")
        if dataset_name_list[0] is not None:
            database_name = dataset_name_list[0]
        else:
            database_name = None

        if dataset_name_list[1] is not None:
            dataset_name = dataset_name_list[1]
        else:
            dataset_name = None

        if file_format == "delta":
            file_format = "parquet_delta"

        is_internal_dataset = True
        test_flag = ""
        location_flag = "managed internally"

        davt_database_folder = config["davt_database_folder"]
        not_found = -1

        if dataset_file_path.find(davt_database_folder) is not_found:
            is_using_dataset_folder_path_override = True
            is_internal_dataset = False
            test_flag = " not"
            location_flag = "managed externally"
        elif (is_using_dataset_folder_path_override is True and file_format == "parquet_delta"):
            is_internal_dataset = False
            test_flag = " not"
            location_flag = "managed externally"

        table_exists_flag = obj_ds_core.table_exists(spark, dataset_name, database_name)

        print(f"database_name:{database_name} dataset_name:{dataset_name}")
        print(f"location_flag: {location_flag}")
        print(f"davt_database_folder:{davt_database_folder}")
        print(f"test_flag:{test_flag} in {dataset_file_path}")
        print(f"test if dataset exists:{dataset_name}")
        print(f"for database: {database_name} returned: {table_exists_flag}")
        print(f"partition_by:{partition_by}")
        print(f"is_internal_dataset:{is_internal_dataset}")
        print(f"is_drop:{is_drop}")
        print(f"file_format:{file_format}")
        print(f"incremental:{incremental}")

        if is_internal_dataset is False and file_format == "parquet_delta":
            if obj_env_file.file_exists(config, dataset_file_path, dbutils):
                sql_command = "DROP TABLE IF EXISTS " + full_dataset_name
                spark.sql(sql_command)
                sql_command = f"CREATE TABLE  {full_dataset_name}  USING DELTA LOCATION '{dataset_file_path}'"
                print(f"attempting sql_command:{sql_command}")
                spark.sql(sql_command)
                print(f"created Delta dataset {full_dataset_name}:")
                print(f"at {dataset_file_path}")
            else:
                print("error attempting to load a dataset file that does not exist")
                print(f"or is internal: {dataset_file_path}")

        # dataset is parquet internal to database directory and full refresh
        if (is_internal_dataset is True and incremental == "replace"):
            print("upsert for dataset")
            print("upsert is_drop: " + str(is_drop))
            print("upsert file_format: " + file_format)
            print("upsert partition_by: " + str(partition_by))
            # Consider adding delete option later but will need to support schema
            # changes and will most likely have a performance hit
            # Delete will slow down code and increase maintenance but may provide better schema change logging
            # sql_command = f"DROP TABLE IF EXISTS {full_dataset_name}"
            # sql_command = f"DELETE FROM  {full_dataset_name}"
            # spark.sql(sql_command)
            # Consider adding delete option later but will need to support schema
            # changes and will most likely have a performance hit
            # Delete will slow down code and increase maintenance but may provide better schema change logging
            # sql_command = f"DELETE FROM  {full_dataset_name}"

            # if file_format != "parquet_delta":
            # print("not parquet")
            if partition_by is not None:
                partition_by_array = partition_by.split(",")
                print(f"writing {full_dataset_name} to")
                print(f"{dataset_file_path} with partition")
                print(f"by {partition_by}")
                one = 1
                # don't merge schema for replace
                # .option( "mergeSchema", "true")
                if len(partition_by_array) is one:
                    print("paritioned (1) parquet saveastable : managed folder")
                    p_by = partition_by_array[0].strip()
                    df_crud.write.mode("overwrite").format("delta").partitionBy(p_by).saveAsTable(full_dataset_name)
                else:
                    if len(partition_by_array) > one:
                        p_by_0 = partition_by_array[0].strip()
                        p_by_1 = partition_by_array[1].strip()
                        df_crud.write.mode("overwrite").format("delta").partitionBy(
                            p_by_0).partitionBy(
                            p_by_1).saveAsTable(full_dataset_name)
                    else:
                        # no partition
                        # don't merge schema for replace
                        # .option("mergeSchema", "true")
                        print("paritioned (0) parquet saveastable : non managed folder override")
                        df_crud.write.mode("overwrite").format("delta").saveAsTable(full_dataset_name)
            else:
                print("unparitioned parquet saveastable : managed folder")
                # .option("mergeSchema", "true")
                try:
                    df_crud.write.mode("overwrite").format("delta").saveAsTable(full_dataset_name)
                except pyspark.sql.utils.AnalysisException as ex_analysis:
                    print(f"Error saving dataframe: {full_dataset_name}")
                    print("An exception occurred: " + str(ex_analysis))
                    # rename and try again
                    # .option("mergeSchema", "true")
                    sql_command = f"DROP TABLE IF EXISTS {full_dataset_name}"
                    spark.sql(sql_command)
                    try:
                        df_crud.write.mode("overwrite").format("delta").saveAsTable(full_dataset_name)
                    except pyspark.sql.utils.AnalysisException as ex_analysis_1:
                        print("Error saving dataframe: full_dataset_name")
                        print("An exception occurred: " + str(ex_analysis_1))
                        for c_original in df_crud.columns:
                            c_renamed = obj_ds_core.scrub_object_name(c_original)
                            df_crud = df_crud.withColumnRenamed(c_original, c_renamed)

        # dataset is parquet internal to database directory and incremental refresh
        print(f"is_internal_dataset:{is_internal_dataset}")
        print(f"incremental:{incremental}")
        if (is_internal_dataset is True) and (incremental == "incremental" or incremental == "incremental_with_purge"):
            table_exists = obj_ds_core.table_exists(spark, dataset_name, database_name)
            is_external_table = False
            if (file_format != "parquet_delta" or dataset_name == "bronze_clc_schema"):
                is_external_table = True
            if table_exists and is_external_table:
                if (incremental == "incremental_with_purge" and dataset_name != "bronze_clc_schema"):
                    sql_command = f"DELETE FROM {full_dataset_name} where "
                    sql_command = sql_command + " __meta_ingress_file_path = '{ingress_file_path}'"
                    print(f"attempting sql_command:{sql_command}")
                    spark.sql(sql_command)

                print(f"attempting to modifying existing dataset:{full_dataset_name}")
                print(f"with data from {ingress_file_path} in format {file_format}")
                print(f"with merge at path {dataset_file_path}")

                match_expr = "delta.row_id = updates.row_id and updates.row_id = delta.row_id"
                delta_dataset = None

                try:
                    delta_dataset = DeltaTable.forPath(spark, dataset_file_path)

                    delta_dataset.alias("delta").merge(
                        df_crud.alias("updates"), match_expr
                    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
                    return True
                except Exception as exception_check:
                    print("merge request input of the following dataframe:" + str(exception_check))
                    # display(df_crud)
                    print("merge request output of the following dataframe" + str(exception_check))
                    if delta_dataset is not None:
                        df_crud_history = delta_dataset.history()
                        # display(df_crud_history)
                    raise
            else:
                print(f"table_exists:{obj_ds_core.table_exists(spark, dataset_name, database_name)}")
                print(f"is_internal_dataset:{is_internal_dataset} dataset_name:{dataset_name}")
                print(f"database_name:{database_name} file_format:{file_format}")
                print("attempting to create Delta dataset")
                print(f"{full_dataset_name}: at")
                print(f"{dataset_file_path}")
                # Dataset hot references external file
                if is_internal_dataset is False:
                    if file_format == "parquet":
                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} "
                        sql_command = sql_command + f" USING PARQUET LOCATION '{dataset_file_path}'"
                    else:
                        sql_command = f"CREATE TABLE IF NOT EXISTS {full_dataset_name} "
                        sql_command = sql_command + f" USING DELTA LOCATION '{dataset_file_path}'"
                    spark.sql(sql_command)
                    print(f"created Delta dataset {full_dataset_name}:")
                    print(f"at {dataset_file_path}")
                else:
                    if file_format == "parquet":
                        print("error attempting to load a parquet directory")
                        print(f"that does not exist: {dataset_file_path}")
                    else:
                        if partition_by is not None:
                            partition_by_array = partition_by.split(",")
                            print(f"writing {full_dataset_name} to {dataset_file_path}")
                            print(f"with partition by {partition_by}")

                            if len(partition_by_array) == 1:
                                print(f"df_crud.write.format('delta').partitionBy({partition_by_array[0].strip()})")
                                print(f".saveAsTable({full_dataset_name})")
                                df_crud.write.format("delta").option(
                                    "mergeSchema", "true"
                                ).partitionBy(
                                    partition_by_array[0].strip()
                                ).saveAsTable(
                                    full_dataset_name
                                )
                            else:
                                if len(partition_by_array) > 1:
                                    print(f"df_crud.write.format('delta').partitionBy({partition_by_array[0].strip()})")
                                    print(f".partitionBy({partition_by_array[1].strip()}).")
                                    print(f"saveAsTable({full_dataset_name})")
                                    df_crud.write.format("delta").option(
                                        "mergeSchema", "true"
                                    ).partitionBy(
                                        partition_by_array[0].strip()
                                    ).partitionBy(
                                        partition_by_array[1].strip()
                                    ).saveAsTable(
                                        full_dataset_name
                                    )
                                else:
                                    message_text = f"df_crud.write.format('delta').saveAsTable({full_dataset_name})"
                                    print(message_text)
                                    df_crud.write.format("delta").option(
                                        "mergeSchema", "true"
                                    ).saveAsTable(full_dataset_name)
                        else:
                            print(f"writing {full_dataset_name} to ")
                            print(f"{dataset_file_path} without partition")
                            df_crud.write.format("delta").option(
                                "mergeSchema", "true"
                            ).saveAsTable(full_dataset_name)

        return "success"

    @classmethod
    def get_export_dataset_or_view_schema_config(
        cls,
        config,
        config_dataset_or_notebook,
        spark,
        sorted_df,
        view_or_schema,
        schema_df
    ):
        """Save metata data of dataset of view to delta lake
        Creates metadata for every column on the dataframe
        Creates a summary row with the column name "all" to summary metrics for the entire dataframe

        Args:
            config (_type_): _description_
            config_dataset_or_notebook (_type_): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_
            sorted_df (_type_): _description_
            view_or_schema (_type_): _description_

        Returns:
            _type_: _description_
        """

        obj_ds_core = davt_ds_core.DataSetCore()

        schema_dataset_file_path = config["schema_dataset_file_path"]
        row_id_column_names = ""
        davt_database_folder = config["davt_database_folder"]
        environment = config["environment"]
        project_id = config["project_id"]

        is_using_dataset_folder_path_override = False

        if view_or_schema == "view":
            dataset_name = config_dataset_or_notebook["view_name"]
            full_dataset_name = config_dataset_or_notebook["full_view_name"]
            dataset_file_path = "n_a"
        else:
            dataset_name = config_dataset_or_notebook["dataset_name"]
            full_dataset_name = config_dataset_or_notebook["full_dataset_name"]
            dataset_file_path = config_dataset_or_notebook["dataset_file_path"]

        row_id_keys = config_dataset_or_notebook["row_id_keys"]
        sorted_df.createOrReplaceTempView("dataset_sorted_df")

        override = config["is_export_schema_required_override"]
        davt_database_name = config['davt_database_name']
        is_export_schema_required_override = override
        schema_full_dataset_name = f"davt_{project_id}_{environment}.bronze_clc_schema"

        if is_export_schema_required_override != "force_off":
            clc_dataset_name = "bronze_clc_schema"
            if obj_ds_core.table_exists(spark, clc_dataset_name, davt_database_name) is True:
                print(f"delete {full_dataset_name} from: {clc_dataset_name}")
                delete_sql = f"Delete from {davt_database_name}.bronze_clc_schema"
                delete_sql = delete_sql + f" where full_dataset_name = '{full_dataset_name}'"
                df_deleted = spark.sql(delete_sql)
                print("deleted rows: " + str(df_deleted.count()))
            print(f"describe {full_dataset_name} for: bronze_clc_schema")
            df_schema = spark.sql("Describe Table dataset_sorted_df")
            df_schema = df_schema.distinct()
            df_schema = df_schema.withColumn("dataset_name", lit(dataset_name))
            df_schema = df_schema.withColumn("full_dataset_name", lit(full_dataset_name))
            df_schema = df_schema.withColumn("dataset_file_path", lit(dataset_file_path))
            df_schema = df_schema.withColumnRenamed("col_name", "column_name")
            df_schema = df_schema.withColumnRenamed("data_type", "data_type_name")
            row_id_keys_databricks = "col('dataset_name'),col('column_name')"
            arg_list = [eval(col_name.strip()) for col_name in row_id_keys_databricks.split(",")]
            df_schema = df_schema.withColumn("row_id_databricks", concat_ws("-", *arg_list))
            if row_id_keys is None:
                row_id_keys = ""
            col_list = [
                ((x.strip().replace("col('", "").replace("')", "")))
                for x in row_id_keys.split(",")
            ]
            row_id_column_names = str(",".join(col_list))
            print("row_id_column_names: " + row_id_column_names)
            print("updated databricks metadata for: schema_databricks_df")

            merged_df = df_schema
            merged_df = merged_df.withColumn("row_id", col("row_id_databricks"))
            merged_df = merged_df.drop("row_id_databricks")
            merged_df = merged_df.drop("row_id_koalas")
            merged_df = merged_df.withColumn("unique_count", lit(0))
            merged_df = merged_df.withColumn("null_count", lit(0))
            merged_df = merged_df.withColumn("max_length", lit(0))
            merged_df = merged_df.withColumn("min_length", lit(0))
            merged_df = merged_df.withColumn("ingress_column_name", lit(""))
            merged_df = merged_df.withColumn("ingress_column_format", lit(""))
            merged_df = merged_df.withColumn("ingress_column_label", lit(""))
            merged_df = merged_df.withColumn("unique_count_scrubbed", lit(0))
            merged_df = merged_df.withColumn("scope", lit("column"))
            merged_df = merged_df.withColumn("row_id_column", lit(row_id_column_names))
            merged_df = merged_df.withColumn("row_count",  lit(0))
            merged_df = merged_df.withColumn("ingress_row_count",  lit(0))
            merged_df = merged_df.withColumn("ingress_ordinal_position",  lit(0))
            merged_df = merged_df.withColumn("ingress_column_length",  lit(0))
            merged_df = merged_df.withColumn("ingress_table_name",  lit(0))

            schema = StructType(
                [
                    StructField("column_name", StringType(), False),
                    StructField("data_type_name", StringType(), False),
                    StructField("comment", StringType(), True),
                    StructField("dataset_name", StringType(), False),
                    StructField("full_dataset_name", StringType(), False),
                    StructField("dataset_file_path", StringType(), False),
                    StructField("row_id", StringType(), False),
                    StructField("unique_count", LongType(), True),
                    StructField("null_count", LongType(), True),
                    StructField("max_length", LongType(), True),
                    StructField("min_length", LongType(), True),
                    StructField("ingress_column_name", StringType(), True),
                    StructField("ingress_column_format", StringType(), True),
                    StructField("ingress_column_label", StringType(), True),
                    StructField("unique_count_scrubbed", LongType(), True),
                    StructField("scope", StringType(), True),
                    StructField("row_id_column", StringType(), True),
                    StructField("row_count", LongType(), True),
                    StructField("ingress_row_count", LongType(), True),
                    StructField("ingress_ordinal_position", LongType(), True),
                    StructField("ingress_column_length", LongType(), True),
                    StructField("ingress_table_name", StringType(), True),
                ]
            )

            # display(merged_df)

            schema_column_df = spark.createDataFrame(merged_df.rdd, schema=schema)
            key = "is_using_dataset_folder_path_override"
            is_using_dataset_folder_path_override = config[key]
            schema_dataset_file_path = davt_database_folder.rstrip("/") + "/bronze_clc_schema"
            schema_dataset_file_path = schema_dataset_file_path.replace("dbfs:", "")
            partitioned_by = "dataset_name"

            empty = ""
            row_id = full_dataset_name
            scope = "dataset"
            row_data = [
                (
                    ("all_columns"),
                    "n_a",
                    "",
                    dataset_name,
                    full_dataset_name,
                    dataset_file_path,
                    row_id,
                    (0),
                    (0),
                    (0),
                    (0),
                    (empty),
                    (empty),
                    (empty),
                    (0),
                    (scope),
                    "full_dataset_name",
                     (0),
                     (0),
                     (0),
                     (0),
                     (0),
                )
            ]

            print("row_data: " + str(row_data))
            schema_dataset_df = spark.createDataFrame(row_data, schema)
        else:
            partitioned_by = ""
            schema_column_df = None
            schema_dataset_df = None

        config_schema = {
            "schema_column_df": schema_column_df,
            "schema_dataset_df": schema_dataset_df,
            "schema_full_dataset_name": schema_full_dataset_name,
            "schema_dataset_file_path": schema_dataset_file_path,
            "partitioned_by": partitioned_by,
            "is_using_dataset_folder_path_override": is_using_dataset_folder_path_override,
        }

        return config_schema
