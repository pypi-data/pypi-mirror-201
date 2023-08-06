""" Module for environment_metadata for the developer service with
metadata config file dependencies. """


# core
import sys  # don't remove required for error handling
import os
from pathlib import Path

# text
import json
from html.parser import HTMLParser  # web scraping html

import logging
import logging.config

# data
import uuid
from datetime import datetime

# davt
from davt_services_python.developer_service \
    import security_core as davt_sec_core
from davt_services_python.developer_service \
    import environment_file as davt_env_file
from davt_services_python.creator_service \
    import logging_metadata as davt_log_metadata

from dotenv import load_dotenv, find_dotenv, set_key

# spark
from pyspark.sql import (SparkSession, DataFrame)
from pyspark.sql.functions import (col, concat_ws, lit,
                                   udf, trim)
from pyspark.sql.types import (StringType, StructType)


# http
import requests

# Import from sibling directory ..\developer_service
OS_NAME = os.name


uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())


class EnvironmentMetaData:
    """This is a conceptual class representation of an Environment
    It is a static class libary
    Todo
    Note which variables require manual updates from the centers and which
    can be prepopulated
    Note which variables are EDAV or Peraton specific
    Separate out config.devops.dev, config.davt.dev and config.core.dev
    """

    @classmethod
    def check_configuration_files(cls, config: dict, dbutils: object) -> dict:
        """Takes in config dictionary and dbutils objects, returns populated
            check_files dictionary with check results

        Args:
            config (dict): global config dictionary
            dbutils (object): databricks dbutils object

        Returns:
            dict: check_files dictionary with results of file configuration
                    checks
        """

        running_local = config["running_local"]
        # confirm ingress_folder
        ingress_folder = config["ingress_folder"]
        ingress_folder_files_exists = str(cls.file_exists(
                                          running_local,
                                          ingress_folder, dbutils))

        # confirm config_folder
        config_folder = config["config_folder"]
        config_folder_files_exists = str(cls.file_exists(
                                         running_local, config_folder,
                                         dbutils))

        # confirm database path
        davt_database_folder = config["davt_database_folder"]
        files_exists = cls.file_exists(running_local,
                                       davt_database_folder, dbutils)
        davt_database_folder_files_exists = str(files_exists)

        s_text = f"ingress_folder_files_exists exists test result:\
            {ingress_folder_files_exists}"
        s_text_1 = f"davt_database_folder_files_exists exists test result:\
            {davt_database_folder_files_exists}"
        s_text_2 = f"{config['davt_database_name']} at davt_database_folder:\
            {davt_database_folder}"
        ingress_folder_files_exists_test = s_text
        config_folder_files_exists_test = f"config_folder_files_exists exists\
            test result: {config_folder_files_exists}"
        check_files = {
            "ingress_folder": f"{ingress_folder}",
            "ingress_folder_files_exists_test":
            ingress_folder_files_exists_test,
            "config_folder": f"{config_folder}",
            "config_folder_files_exists_test": config_folder_files_exists_test,
            "davt_database_folder": f"{davt_database_folder}",
            "davt_database_folder_files_exists test": s_text_1,
            "creating new davt_database_name": s_text_2
        }

        return check_files

    @classmethod
    def get_job_list(cls, job_name: str, config: dict, spark: SparkSession) -> DataFrame:
        """Get list of jobs actions for a selected job

        Args:
            job_name (str): Selected Job name
            config (dict): Configuration dictionary
            spark (SparkSession): Spark object

        Returns:
            DataFrame: Dataframe with list of job actions
        """

        obj_env_log = davt_log_metadata.LoggingMetaData()

        ingress_folder_sps = config["ingress_folder_sps"]
        ingress_folder_sps = ingress_folder_sps.rstrip("/")
        config_jobs_path = f"{ingress_folder_sps}/bronze_sps_config_jobs.csv"

        project_id = config["project_id"]
        info_msg = f"config_jobs_path:{config_jobs_path}"
        obj_env_log.log_info(config, info_msg)

        first_row_is_header = "true"
        delimiter = ","
        df_jobs = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                config_jobs_path, forceLowercaseNames=True, inferLong=True
            )
        )
        df_jobs = df_jobs.withColumn('job_name', trim('job'))
        df_jobs = df_jobs.filter(df_jobs.job_name == job_name)
        df_jobs.show(truncate=False)

        return df_jobs

    @classmethod
    def get_column_list(cls, config: dict, spark: SparkSession,
                        dbutils: object) -> DataFrame:
        """Takes in dataset config dictionary, spark object, dbutils object\
        and returns dataframe
        with list of columns for dataset

        Args:
            config (dict): dataset config dictionary
            spark (SparkSession): spark session
            dbutils (object): databricks dbutils object

        Returns:
            DataFrame: dataframe popluated with list of columns for dataset
        """

        first_row_is_header = "true"
        delimiter = ","

        dataset_name = config["dataset_name"]
        running_local = config["running_local"]
        ingress_folder_sps = config["ingress_folder_sps"]
        project_id = config["project_id"]
        ingesttimestamp = datetime.now()

        file_path = f"{ingress_folder_sps}bronze_sps_config_columns.csv"
        # check if size of file is 0
        file_size = cls.get_file_size(running_local, file_path, dbutils, spark)

        print(f"file_size: {str(file_size)}")

        # default to empty DataFrame
        df_results = spark.createDataFrame([], StructType([]))

        if file_size > 0:
            df_results = (
                spark.read.format("csv")
                .option("header", first_row_is_header)
                .option("sep", delimiter)
                .option("inferSchema", True)
                .option("inferLong", True)
                .option("multiline", True)
                .option("inferDecimal", True)
                .option("inferInteger", True)
                .option("forceLowercaseNames", True)
                .load(file_path)
                .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
                .withColumn(
                    "row_id",
                    concat_ws(
                        "-", col("project_id"), col("dataset_name"),
                        col("column_name")
                    ),
                )
            )

            # bronze_sps_config_columns_df.select(col("column_batch_group").cast("int").as("column_batch_group"))
            if df_results.count() == 0:
                print("File hase 0 rows")
            else:
                if dataset_name == "sps":
                    project_filter = f"(project_id == '{project_id}')"
                    df_results = df_results.filter(project_filter)
        else:
            print("File is empty")

        return df_results

    @staticmethod
    def get_file_size(running_local: bool,
                      file_path: str,
                      dbutils, spark) -> int:
        """Gets file size as integer for file_path

        Args:
            running_local (bool): _description_
            file_path (str): _description_
            dbutils (_type_): _description_
            spark (_type_): _description_

        Returns:
            int: _description_
        """

        obj_env_file = davt_env_file.EnvironmentFile()
        file_size = obj_env_file.get_file_size(running_local,
                                               file_path, dbutils, spark)
        return file_size

    @staticmethod
    def file_exists(running_local: bool, path: str, dbutils) -> bool:
        """Takes in path, dbutils object, returns whether file exists at provided path

        Args:
            running_local: bool
            path (str): path to file
            dbutils (object): databricks dbutils

        Returns:
            bool: True/False indication if file exists
        """

        obj_env_file = davt_env_file.EnvironmentFile()
        file_exists = obj_env_file.file_exists(running_local, path, dbutils)
        return file_exists

    @staticmethod
    def convert_windows_dir(path: str) -> str:
        """Takes in path and returns path with backslashes converted to forward slashes

        Args:
            path (str): path to be converted

        Returns:
            str: converted path
        """
        obj_env_file = davt_env_file.EnvironmentFile()
        converted_path = obj_env_file.convert_windows_dir(path)
        return converted_path

    @staticmethod
    def load_environment(running_local: bool, sp_tenant_id: str,
                         subscription_id: str,
                         sp_client_id: str,
                         environment: str,
                         project_id: str,
                         dbutils):
        """Loads the environment file to configure the enviornment

        Args:
            running_local (bool): _description_
            sp_tenant_id (str): _description_
            subscription_id (str): _description_
            sp_client_id (str): _description_
            environment (str): _description_
            project_id (str): _description_
            dbutils (_type_): _description_
        """

        path = sys.executable + "\\.."
        sys.path.append(os.path.dirname(os.path.abspath(path)))
        env_path = os.path.dirname(os.path.abspath(path))
        env_share_path = env_path + "\\share"
        folder_exists = os.path.exists(env_share_path)
        if not folder_exists:
            # Create a new directory because it does not exist
            os.makedirs(env_share_path)
        env_share_path_2 = sys.executable + "\\..\\share"
        sys.path.append(os.path.dirname(os.path.abspath(env_share_path_2)))

        print( f"env_share_path: {env_share_path}")

        if running_local is True:
            print(f"running_local: {running_local}")
            env_file_path = env_share_path + "\\.env"
            print(f"env_file_path: {env_file_path}")
            # don't delete line below - it creates the file
            env_file = open(env_file_path, "w+", encoding="utf-8")
            dotenv_file = find_dotenv(env_file_path)
            print(f"dotenv_file: {dotenv_file}")
            set_key(dotenv_file, "AZURE_TENANT_ID", sp_tenant_id)
            set_key(dotenv_file, "AZURE_SUBSCRIPTION_ID", subscription_id)
            set_key(dotenv_file, "AZURE_CLIENT_ID", sp_client_id)
        else:
            print(f"running_local: {running_local}")
            env_file_path = f"/mnt/{environment}/{project_id}"
            print(f"env_file_path: {env_file_path}")
            env_file_path = env_file_path + "/config/config_{environment}.txt"
            dbutils.fs.put(env_file_path, f"""AZURE_TENANT_ID {sp_tenant_id}
AZURE_SUBSCRIPTION_ID {subscription_id}
AZURE_CLIENT_ID {sp_client_id}
            """, True)
            dotenv_file = find_dotenv(env_file_path)
            load_dotenv(dotenv_file)

        return "Success"

    @classmethod
    def get_configuration_common(cls, parameters: dict, dbutils) -> dict:
        """Takes in parameters dictionary and returns config dictionary

        Args:
            parameters (dict): global parameters dictionary

        Returns:
            dict: update global configuration dictionary
        """

        if isinstance(parameters['running_local'], (bool)) is False:
            running_local = parameters['running_local'].lower() in ['true', '1', 't', 'y', 'yes']
        else:
            running_local = parameters['running_local']

        project_id = parameters["project_id"]
        print(f"running_local: {running_local}")
        azure_client_secret_key = parameters['azure_client_secret_key']
        environment = parameters["environment"]
        project_id_root = parameters["project_id_root"]
        yyyy_param = parameters["yyyy"]
        mm_param = parameters["mm"]
        dd_param = parameters["dd"]
        dataset_name = parameters["dataset_name"]
        cicd_action = parameters["cicd_action"]
        repository_path = parameters["repository_path"]

        # create logger
        logger = logging.getLogger(project_id)
        logger.setLevel(logging.DEBUG)

        config_string = "config"
        cicd_action_string = "cicd"

        os_name_check = os.name
        if os_name_check.lower() == "nt":
            print("windows: nt")
            repository_path = cls.convert_windows_dir(repository_path)

        env_folder_path = repository_path.rstrip('/') + "/" + project_id_root + "/" + project_id + "/" + config_string
        environment_json_path = env_folder_path + "/" + f"{config_string}.{environment}.json"
        environment_json_path_default =  env_folder_path + "/" + f"{config_string}.{environment}.json"
        # some times notebooks are not 2 folders deep - try parent folder
        print(f"environment_json_path check 1: {environment_json_path}")
        environment_json_path_defaault =  env_folder_path + "/" + f"{config_string}.{environment}.json"
        if cls.file_exists(running_local, environment_json_path, None) is False:
            repository_path_temp = os.getcwd()
            repository_path_temp = str(Path(repository_path_temp).parent)
            repository_path_temp = cls.convert_windows_dir(repository_path_temp)
            repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
            environment_json_path = repository_path_temp + f"{config_string}.{environment}.json"
            print(f"environment_json_path check 2: {environment_json_path}")
            if cls.file_exists(running_local, environment_json_path, None) is False:
                repository_path_temp = os.getcwd()
                repository_path_temp = str(Path(repository_path_temp).parent.parent)
                repository_path_temp = cls.convert_windows_dir(repository_path_temp)
                repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
                environment_json_path = repository_path_temp + f"{config_string}.{environment}.json"
                print(f"environment_json_path check 3: {environment_json_path}")
                if cls.file_exists(running_local, environment_json_path, None) is False:
                    repository_path_temp = os.getcwd()
                    repository_path_temp = str(Path(repository_path_temp).parent.parent.parent)
                    repository_path_temp = cls.convert_windows_dir(repository_path_temp)
                    repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
                    environment_json_path = repository_path_temp + f"{config_string}.{environment}.json"
                    print(f"environment_json_path check 4: {environment_json_path}")
                    if cls.file_exists(running_local, environment_json_path, None) is False:
                        environment_json_path = environment_json_path_default

        cicd_folder = f"{repository_path}{project_id_root}/{project_id}/{cicd_action_string}/"
        cicd_action_path = f"{cicd_folder}" + f"{cicd_action}" + f".{environment}.json"

        print("---- WORKING REPOSITORY FILE REFERENCE -------")
        print(f"environment_json_path: {environment_json_path}")
        print(project_id, "----------------------------------------------")

        with open(environment_json_path, mode="r", encoding="utf-8") as json_file:
            config = json.load(json_file)

        config['running_local'] = running_local
        config["yyyy"] = yyyy_param
        config["mm"] = mm_param
        config["dd"] = dd_param
        config["dataset_name"] = dataset_name
        config["dataset_type"] = "TABLE"
        config["repository_path"] = repository_path
        config["environment_json_path"] = environment_json_path
        config["cicd_action_path"] = cicd_action_path
        config["azure_client_secret_key"] = azure_client_secret_key
        config["ingress_folder_sps"] = "".join([config["config_folder"], "davt/"])
        config["project_id"] = config["davt_project_id"]
        config["project_id_root"] = config["davt_project_id_root"]
        config["project_id_individual"] = config["davt_project_id_individual"]
        project_id_individual = config["project_id_individual"]
        config["databricks_instance_id"] = config["davt_databricks_instance_id"]
        config["environment"] = config["davt_environment"]
        config["override_save_flag"] = "override_with_save"
        config["is_using_dataset_folder_path_override"] = False
        config["is_using_standard_column_names"] = "force_lowercase"
        config["is_export_schema_required_override"] = True
        config["ingress_mount"] = f"/mnt/{environment}/{project_id_individual}/ingress"

        project_id = config["project_id"]
        davt_database_folder = config["davt_database_folder"]
        schema_dataset_file_path = (
            davt_database_folder.rstrip("/") + "/bronze_clc_schema"
        )
        config["schema_dataset_file_path"] = schema_dataset_file_path

        if config:
            print(f"Configuration found environment_json_path: {environment_json_path}")
        else:
            error_message = "Error: no configurations were found."
            error_message = error_message + f"Check your settings file: {environment_json_path}."
            print(error_message)

        scope = config['davt_databricks_kv_scope']
        kv_client_id_key = config['davt_oauth_sp_kv_client_secret_key']
        kv_client_secret_key = config['davt_oauth_sp_kv_client_secret_key']

        if kv_client_id_key.strip() == '':
            kv_client_id_key = None

        if kv_client_secret_key.strip() == '':
            kv_client_secret_key = None

        sp_redirect_url = config["davt_oauth_sp_redirect_url"]
        sp_authority_host_url = config["davt_oauth_sp_authority_host_url"]
        sp_tenant_id = config["davt_azure_tenant_id"]
        subscription_id = config["davt_azure_subscription_id"]
        sp_client_id = config['azure_client_id']
        sp_azure_databricks_resource_id = config['davt_oauth_databricks_resource_id']

        # Write changes to .env file - create .env file if it does not exist
        cls.load_environment(running_local, sp_tenant_id,
                             subscription_id,
                             sp_client_id,
                             environment,
                             project_id,
                             dbutils)

        if running_local is True:
            print(f"azure_client_secret_key:{azure_client_secret_key}")
            sp_client_secret = os.getenv(azure_client_secret_key)
        else:
            sp_client_secret = dbutils.secrets.get(scope=scope,
                                                   key=kv_client_secret_key)

        config["client_id"] = sp_client_id
        config["client_secret"] = sp_client_secret
        config["tenant"] = sp_tenant_id

        if sp_client_secret is None:
            config["error_message"] = "azure_client_secret_value_not_set_error"
        else:
            obj_security_core = davt_sec_core.SecurityCore()

            config_user = \
                obj_security_core.acquire_access_token_with_client_credentials(sp_client_id,
                                                                               sp_client_secret,
                                                                               sp_tenant_id,
                                                                               sp_redirect_url,
                                                                               sp_authority_host_url,
                                                                               sp_azure_databricks_resource_id,
                                                                               project_id)
            config["redirect_uri"] = config_user["redirect_uri"]
            config["authority_host_url"] = config_user["authority_host_url"]
            config["azure_databricks_resource_id"] = config_user["azure_databricks_resource_id"]
            config["authority_url"] = config_user["authority_url"]
            config["access_token"] = config_user["access_token"]

        return config

    @staticmethod
    def get_dataset_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictioarny, spark object, returns list of datasets in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of datasets in project
        """

        obj_env_log = davt_log_metadata.LoggingMetaData()

        first_row_is_header = "true"
        delimiter = ","

        csv_file_path = config["ingress_folder_sps"]
        csv_file_path = csv_file_path + '\\'
        csv_file_path = csv_file_path + "bronze_sps_config_datasets.csv"
        project_id = config["project_id"]
        ingesttimestamp = datetime.now()

        df_results = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                csv_file_path, forceLowercaseNames=True,
                inferLong=True
            )
            .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
            .withColumn(
                "row_id", concat_ws("-", col("project_id"), col("dataset_name"))
            )
        )

        # sort
        if df_results.count() > 0:
            # df_results.show()
            df_results = df_results.sort("pipeline_batch_group")
        else:
            err_message = f"No datasets found for project_id:{project_id}"
            obj_env_log.log_error(project_id, err_message)
            print(err_message)

        return df_results

    @staticmethod
    def get_pipeline_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictionary, spark session object, returns dataframe with list of pipelines in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of pipelines in project
        """

        first_row_is_header = "true"
        delimiter = ","

        ingress_folder_sps = config["ingress_folder_sps"]
        ingesttimestamp = datetime.now()
        project_id = config["project_id"]

        bronze_sps_config_pipelines_df = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                f"{ingress_folder_sps}bronze_sps_config_pipelines.csv",
                forceLowercaseNames=True,
                inferLong=True,
            )
            .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
            .withColumn("row_id", concat_ws("-", col("project_id"), col("view_name")))
        )

        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.filter(
            "project_id == '" + project_id + "' "
        )

        # sort by load group to ensure dependencies are run in order
        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.sort(
            "pipeline_batch_group"
        )

        return bronze_sps_config_pipelines_df

    @classmethod
    def list_files(cls, config: dict, token: str, base_path: str) -> list:
        """Takes in a config dictionary, token and base_path, returns
        populated list of files

        Args:
            config (dict): global config dictionary
            token (str): token
            base_path (str): path to list files

        Returns:
            list: list of files at the path location
        """

        obj_env_log = davt_log_metadata.LoggingMetaData()

        databricks_instance_id = config["databricks_instance_id"]
        json_text = {"path": base_path}
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/workspace/list"
        project_id = config["project_id"]
        obj_env_log.log_info(config, f"------- Fetch {base_path}  -------")
        obj_env_log.log_info(config, f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        obj_env_log.log_info(config, f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers, json=json_text,
                                timeout=120)
        data = None
        results = []

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received list_files with length : {len(str(response_text))} when posting to : "
            msg = msg + f"{url} to list files for : {base_path}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            lst = data["objects"]

            for i in lst:
                if i["object_type"] == "DIRECTORY" or i["object_type"] == "REPO":
                    path = i["path"]
                    results.extend(cls.list_files(config, token, path))
                else:
                    path = i["path"]
                    results.append(path)
        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")

        return results

    @classmethod
    def setup_databricks_configuration(cls, config: dict, spark: SparkSession) -> str:
        """Takes in config dictionary, spark object, returns configured spark object

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            str: folder_database_path
        """

        davt_database_name = config["davt_database_name"]
        davt_database_folder = config["davt_database_folder"]

        running_local = config["running_local"]

        if running_local is True:
            # use default location
            sql_statement = f"create database if not exists {davt_database_name};"
        else:
            sql_statement = f"create database if not exists {davt_database_name}  LOCATION '{davt_database_folder}';"

        print(sql_statement)
        spark.sql(sql_statement)

        # davt_databricks_owner_group = config["davt_databricks_owner_group"]
        # sql_statement = f"alter schema {davt_database_name} owner to `{davt_databricks_owner_group}`;"
        # print(sql_statement)
        # spark.sql(sql_statement)

        sql_statement = f"Describe database {davt_database_name}"
        df_db_schema = spark.sql(sql_statement)

        if running_local is True:
            df_db_schema.show(truncate=False)

        df_db_schema = df_db_schema.filter(df_db_schema.database_description_item == "Location")
        rdd_row = df_db_schema.first()

        if rdd_row is not None:
            folder_database_path = rdd_row["database_description_value"]
        else:
            folder_database_path = "missing dataframe value error"

        return folder_database_path

    @staticmethod
    def setup_spark_configuration(spark: SparkSession, config: dict) -> SparkSession:
        """Takes spark session, global config dictionary
        and return configured Spark session

        Args:
            spark (SparkSession): spark session
            config (dict): global config dictionary

        Returns:
            SparkSession: configured spark session
        """

        obj_env_log = davt_log_metadata.LoggingMetaData()

        c_ep = config["davt_oauth_sp_authority_host_url"]
        c_id = config["client_id"]
        c_secret = config["client_secret"]
        sp_tenant_id = config["davt_azure_tenant_id"]
        running_local = config['running_local']
        project_id = config['project_id']

        client_secret_exists = True
        if c_id is None or c_secret is None:
            client_secret_exists = False
        storage_account = config["davt_azure_storage_account"]

        client_token_provider = "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
        provider_type = "OAuth"

        # stack overflow example
        fs_prefix_e1 = "fs.azure.account.auth."
        fso_prefix_e1 = "fs.azure.account.oauth"
        fso2_prefix_e1 = "fs.azure.account.oauth2"
        fso3_prefix_e1 = "fs.azure.account.oauth2.client.secret"  # spark.hadoop
        fs_suffix_e1 = f".{storage_account}.dfs.core.windows.net"
        fso3_prefix_e1 = fso3_prefix_e1 + fs_suffix_e1

        if client_secret_exists is None:
            client_secret_exists = False

        print(f"client_secret_exists:{str(client_secret_exists)}")
        print(f"endpoint:{str(c_ep)}")

        config["run_as"] = "service_principal"
        run_as = config["run_as"]
        print(f"running databricks access using run_as:{run_as}")

        if (client_secret_exists is True) and (run_as == "service_principal") and running_local is True:

            spark.conf.set(f"{fs_prefix_e1}type{fs_suffix_e1}", provider_type)
            spark.conf.set(f"{fso_prefix_e1}.provider.type{fs_suffix_e1}", client_token_provider)
            spark.conf.set(f"{fso2_prefix_e1}.client.id{fs_suffix_e1}", c_id)
            spark.conf.set(f"{fso2_prefix_e1}.client.secret{fs_suffix_e1}", c_secret)
            client_endpoint_e1 = f"https://login.microsoftonline.com/{sp_tenant_id}/oauth2/token"
            spark.conf.set(f"{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}", client_endpoint_e1)

            obj_env_log.log_info(config, f'spark.conf.set "({fs_prefix_e1}type{fs_suffix_e1}", "{provider_type}")')
            obj_env_log.log_info(config, f'spark.conf.set "({fso_prefix_e1}.provider.type{fs_suffix_e1}", \
                "{client_token_provider}")')
            obj_env_log.log_info(config, f'spark.conf.set "({fso2_prefix_e1}.client.id{fs_suffix_e1}", "{c_id}")')
            obj_env_log.log_info(config, f'spark.conf.set "{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}" \
                = "{client_endpoint_e1}"')

        spark.conf.set("spark.databricks.io.cache.enabled", "true")
        # Enable Arrow-based columnar data transfers
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
        # sometimes azure storage has a delta table not found bug - in that scenario try filemount above
        spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")
        spark.conf.set("spark.databricks.pyspark.enablePy4JSecurity", "false")
        # Enable Delta Preview
        spark.conf.set("spark.databricks.delta.preview.enabled ", "true")

        if running_local is False and project_id != 'ezdx_foodnet':
            spark.sql("SET spark.databricks.delta.schema.autoMerge.enabled = true")
            davt_checkpoint_folder = config["davt_checkpoint_folder"]
            print(f"davt_checkpoint_folder: {davt_checkpoint_folder}")
            spark.sparkContext.setCheckpointDir(davt_checkpoint_folder)

        # Checkpoint
        return spark


class HTMLFilter(HTMLParser):
    """Parses HTMLData

    Args:
        HTMLParser (_type_): _description_
    """

    text = ""

    def handle_data(self, data):
        """Parses HTMLData

        Args:
            data (_type_): _description_
        """
        self.text += data
