""" Module for job_metadata for the developer service with metadata config file dependencies. """

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import json
import copy
import pandas as pd_legacy
from pyspark.sql.functions import trim
from pyspark.sql import (DataFrame)
import davt_services_python.creator_service.pipeline_metadata as davt_pl_metadata
import davt_services_python.creator_service.dataset_metadata as davt_ds_metadata
import davt_services_python.creator_service.environment_metadata as davt_env_metadata
import davt_services_python.creator_service.logging_metadata as davt_log_metadata
import davt_services_python.developer_service.job_core as davt_job_core
import davt_services_python.developer_service.repo_core as davt_repo_core
import davt_services_python.developer_service.dataset_crud as davt_ds_crud
import davt_services_python.developer_service.dataset_core as davt_ds_core
import davt_services_python.developer_service.environment_file as davt_env_file

IPY_ENABLED = False
running_local = ("dbutils" in locals() or "dbutils" in globals()) is not True
if running_local is True and IPY_ENABLED is True:
    from ipywidgets import Dropdown, HBox, Button, Label, Layout
    from IPython.display import display


# Import from sibling directory ..\developer_service
OS_NAME = os.name

class JobMetaData:

    """Class to drives jobs via meta data
    """

    @staticmethod
    def install_cluster_library(config) -> str:
        """Installs cluster library

        Args:
            config (dict): Dictionary of DAVT configuration parameters

        Returns:
            str: Installation status message
        """
        library_source = 'whl'
        davt_root_project_url = config["davt_root_project_url"]
        davt_services_python_version = config["davt_services_python_version"]
        davt_services_python_version = davt_services_python_version.replace("v", "")
        library_folder = f"{davt_root_project_url}dist/"
        library_file = f"{library_folder}davt_services_python-{davt_services_python_version}-py3-none-any.whl"
        obj_repo = davt_repo_core.RepoCore()
        results = obj_repo.install_cluster_library(config, library_source, library_file)
        return results

    @staticmethod
    def get_cluster_library_status(config) -> str:
        """Gets cluster library installation status

        Args:
            config (dict): Dictionary of DAVT configuration parameters

        Returns:
            str: Installation status message
        """

        library_source = 'whl'
        davt_root_project_url = config["davt_root_project_url"]
        davt_services_python_version = config["davt_services_python_version"]
        davt_services_python_version = davt_services_python_version.replace("v", "")
        library_folder = f"{davt_root_project_url}dist/"
        library_file = f"{library_folder}davt_services_python-{davt_services_python_version}-py3-none-any.whl"
        obj_repo = davt_repo_core.RepoCore()
        results = obj_repo.get_cluster_library_status(config, library_source, library_file)
        return results

    @staticmethod
    def download_config(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config: dict, dbutils: object) -> str:
        """Downloads configuration from abfss to local machine / repository

        Args:
            obj_env (davt_env_metadata.EnvironmentMetaData): DAVT environment utility
            config (dict): Dictionary of DAVT configuration parameters
            dbutils (object): Delta.io dbutils object

        Returns:
            str: File download status message
        """

        obj_file = davt_env_file.EnvironmentFile()

        config_folder = config['config_folder']
        destination_path = config['environment_json_path']
        json_file_name = os.path.basename(destination_path)
        source_path_1 = obj_file.convert_abfss_to_https_path(config_folder)
        source_message_1 = f"source_path_1:{source_path_1}"
        destination_path = destination_path.replace('/config/' + json_file_name, '')
        copy_result1 = obj_file.file_adls_copy(config, source_path_1, destination_path, 'BlobFSLocal', dbutils)
        result = f"{str(source_message_1)}-{str(copy_result1)}"
        return result

    @staticmethod
    def get_parameter_menu(config, spark, dbutils=None):
        """Configures Widget Settings for UX Parameter Dropdowns

        Args:
            config (_type_): _description_
            spark (SparkSession): _description_
            dbutils (_type_):

        Returns:
            str: HBox setting display status
        """

        obj_env = davt_env_metadata.EnvironmentMetaData()
        obj_env_log = davt_log_metadata.LoggingMetaData()
        running_local = config["running_local"]
        ingress_folder_sps = config["ingress_folder_sps"]
        sp_tenant_id = config["davt_azure_tenant_id"]
        subscription_id = config["davt_azure_subscription_id"]
        sp_client_id = config['azure_client_id']
        environment = config['environment']
        project_id = config['project_id']

        obj_env.load_environment(running_local, sp_tenant_id,
                                 subscription_id,
                                 sp_client_id,
                                 environment,
                                 project_id,
                                 dbutils)
        ingress_folder_sps = ingress_folder_sps.rstrip("/")
        config_jobs_path = f"{ingress_folder_sps}/bronze_sps_config_jobs.csv"
        first_row_is_header = "true"
        delimiter = ","
        df_jobs: DataFrame = spark.sparkContext.emptyRDD()

        # current date and time
        now = datetime.now()
        format_yyyy = "%Y"
        report_yyyy = now.strftime(format_yyyy)
        format_mm = "%m"
        report_mm = now.strftime(format_mm)
        format_dd = "%d"
        report_dd = now.strftime(format_dd)
        report_yyyy_values = ["2021", "2022"]
        report_mm_values = ["01", "02", "03", "04", "05", "06", "07", "08",
                            "09", "10", "11", "12"]
        report_dd_values = ["NA", "01", "02", "03", "04", "05", "06", "07",
                            "08", "09", "10", "11", "12", "13", "14",
                            "15", "16", "17", "18", "19", "20", "21", "22",
                            "23", "24", "25", "26", "27", "28", "29",
                            "30", "31"]

        default_job_name = "Loading Jobs..."
        try:
            print(f"config_jobs_path:{config_jobs_path}")
            print(f"SPARK_DIST_CLASSPATH:{os.getenv('SPARK_DIST_CLASSPATH')}")
            df_jobs = (
                spark.read.format("csv")
                .option("header", first_row_is_header)
                .option("sep", delimiter)
                .option("multiline", True)
                .option("inferSchema", True)
                .load(config_jobs_path)
            )
            df_jobs = df_jobs.withColumn('job_name', trim('job'))
            df_job_names = df_jobs.select('job_name').distinct()
            job_name_values = df_job_names.rdd.map(lambda x: x[0]).collect()
            job_name_values.insert(0, "Select job to run")
            info_msg = f"job_name_values:{job_name_values}"
            obj_env_log.log_info(config, info_msg)

            if len(job_name_values) > 0:
                default_job_name = job_name_values[0]

        except Exception as ex_load_jobs:
            error_msg = f"Error: Unable to load {config_jobs_path}: Details: {ex_load_jobs}"
            print(error_msg)
            obj_env_log.log_error(config, error_msg)
            default_job_name = "Error: Unable to load jobs"
            job_name_values = [default_job_name]

        if running_local is False:
            if dbutils is not None:
                widgets = dbutils.widgets
                if widgets is not None:
                    dbutils.widgets.dropdown("report_yyyy", report_yyyy,
                                             report_yyyy_values)
                    dbutils.widgets.dropdown("report_mm", report_mm,
                                             report_mm_values)
                    dbutils.widgets.dropdown("report_dd", report_dd,
                                             report_dd_values)

        ipy_enabled = False
        if running_local is True and ipy_enabled is True:
            dropdown_job_name = Dropdown(
                options=job_name_values,
                value=default_job_name,
                description='Job Name:',
                disabled=False,
                layout=Layout(width="30%"),
            )

            dropdown_report_yyyy = Dropdown(
                options=report_yyyy_values,
                value=report_yyyy,
                description='As Of YYYY:',
                disabled=False,
                layout=Layout(width="16%"),
            )

            dropdown_report_mm = Dropdown(
                options=report_mm_values,
                value=report_mm,
                description='As Of MM:',
                disabled=False,
                layout=Layout(width="12%"),
            )

            dropdown_report_dd = Dropdown(
                options=report_dd_values,
                value=report_dd,
                description='As Of DD:',
                disabled=False,
                layout=Layout(width="12%"),
            )

            label = f"Click to run: {default_job_name}"
            button_run = Button(
                description=label,
                disabled=False,
                button_style='success',
                tooltip=label,
                layout=Layout(width="30%"),
            )

            label_job = Label()

            selection_box = HBox([dropdown_report_yyyy,
                                dropdown_report_mm,
                                dropdown_report_dd,
                                dropdown_job_name,
                                button_run,
                                label_job])
        else:
            selection_box = None

        return selection_box

    @staticmethod
    def get_standard_parameters(environment: str, dbutils, spark,
                                config_jobs_path) -> dict:
        """ Get standard parameters used to populate run jobs notebook parameters
        Args:
            environment (str): Default environment
            dbutils (_type_): Datbricks dbutils object
            spark (_type_): Spark session object

        Returns:
            dict: Parameter values
        """

        obj_env_log = davt_log_metadata.LoggingMetaData()
        obj_job_core = davt_job_core.JobCore()

        parameters = obj_job_core.get_standard_parameters(environment, dbutils)
        project_id = parameters["project_id"]
        info_msg = f"config_jobs_path:{config_jobs_path}"
        print(info_msg)
        if dbutils is None:
            running_local = True
        else:
            running_local = False

        df_jobs = pd_legacy.read_csv(config_jobs_path)
        df_jobs[df_jobs.columns] = df_jobs.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df_job_names = df_jobs['job']
        job_name_values = []
        # create copy that won't change
        job_name_values = copy.copy(df_job_names.to_list())
        # remove dupes
        job_name_values_list = [*set(job_name_values)]
        # sort
        job_name_values_list.sort()
        job_name_values_list.insert(0, "Select job to run")
        default_job_name = job_name_values_list[0]

        if dbutils is None:
            print("Warning: dbutils is None")
        else:
            widgets = dbutils.widgets

        print(f"job_name_values_list:{job_name_values_list}")
        print(f"config_jobs_path:{config_jobs_path}")
        if not running_local:
            try:
                job_name = dbutils.widgets.get("job_name")
                print(f"job_name widget:{job_name}")
                if job_name == "Select job to run":
                    print("job_name widget does not have job selected")
                    dbutils.widgets.remove("job_name")
                    dbutils.widgets.dropdown("job_name", default_job_name, job_name_values_list )
            except:
                print(f"job_name widget not found")
                dbutils.widgets.dropdown("job_name", default_job_name, [str(x) for x in job_name_values_list] )
                job_name = None

        parameters["array_jobs"] = job_name_values_list

        return parameters

    @staticmethod
    def setup_project_mount(config: dict, spark, dbutils) -> str:
        """_summary_

        Args:
            config (dict): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_

        Returns:
            str: _description_
        """

        environment = config['environment']
        project_id = config['project_id']
        configs = {
            "fs.azure.account.auth.type": "CustomAccessToken",
            "fs.azure.account.custom.token.provider.class":
                spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
        }

        mount_path = f"/mnt/{environment}/{project_id}"
        source_path = config['davt_root_project_url']
        print(f"mount_path:{mount_path}")
        print(f"source_path:{source_path}")

        if dbutils is None:
            print("Error: dbutils not configured")

        if any(mount.mountPoint == mount_path for mount in dbutils.fs.mounts()):
            dbutils.fs.unmount(mount_path)

        dbutils.fs.mount(
            source=source_path,
            mount_point=mount_path,
            extra_configs=configs)

        return "Success"

    @staticmethod
    def trigger_pull_request(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config: dict, dbutils) -> str:
        """Triggers pull request

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (dict): _description_
            dbutils (_type_): _description_

        Returns:
            str: Trigger request file status message
        """

        source_path = config['cicd_action_path']
        root_parts = Path(os.getcwd()).parts
        # get first 4 parts of path should be repo
        folder_root = '/'.join(root_parts[0:5])
        print(f"folder_root:{folder_root}")
        print(f"source_path:{source_path}")

        obj_file_core = davt_env_file.EnvironmentFile()
        obj_repo_core = davt_repo_core.RepoCore()
        destination_path = obj_repo_core.get_cicd_destination_path(folder_root)
        copy_result = obj_file_core.file_adls_copy(config, source_path, destination_path, 'LocalBlobFS', dbutils)
        return copy_result

    @staticmethod
    def run_publish_config(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config: dict, spark,
                           dbutils) -> str:
        """Runs publish configuration

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (dict): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_

        Returns:
            str: Configuration publish status message
        """

        environment = config["environment"]
        sql_statement = f"Select json_value from davt_ezdx_foodnet_{environment}"
        sql_statement = sql_statement + ".silver_export_translationfoodnet_json_vw"
        print("sql_statement:" + sql_statement)
        df_json = spark.sql(sql_statement)

        ingress_mount = config['ingress_mount']
        json_data = json.loads(df_json.toPandas().to_json(orient="columns"))
        json_string = json_data["json_value"]["0"]
        print(json_string)
        config_mount_path = "".join(['/dbfs', ingress_mount.rstrip('/'), '/davt/translationFoodnet.json'])
        with open(config_mount_path, 'w', encoding='UTF-8') as f_translation:
            f_translation.write(json_string)
            f_translation.close()

        return "Success"

    @staticmethod
    def run_publish_release(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config) -> str:
        """Publishes a release to the appropriate environment in Databricks.  This fucntion is not complete.

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (_type_): _description_

        Returns:
            str: _description_
        """

        return "Success"

    @staticmethod
    def run_pull_request(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config) -> str:
        """Triggers pull request from the repository

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (_type_): _description_

        Returns:
            str: _description_
        """

        obj_repo_core = davt_repo_core.RepoCore()
        environment = config['environment']
        token = config["access_token"]
        branch_name = environment.upper()
        obj_repo_core.pull_repository_latest(config, token, '/Repos/DEV/', 'DAVT', branch_name)
        return "Success"

    @staticmethod
    def run_data_processing(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config, spark, dbutils,
                            export_schema, filter_column_name, filter_value) -> str:
        """Runs data processing:  This is the second step in the 5 step (IDEAS) process.

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (_type_): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_
            export_schema (_type_): _description_
            filter_column_name (_type_): _description_
            filter_value (_type_): _description_

        Returns:
            str: Data processing status message
        """

        project_id = config["project_id"]
        running_local = config["running_local"]
        print(f"running_local:{running_local}")

        if export_schema == "export":
            config["is_export_schema_required_override"] = True

        # setup database
        davt_database_folder = obj_env_metadata.setup_databricks_configuration(config, spark)
        config['davt_database_folder'] = davt_database_folder
        df_datasets = obj_env_metadata.get_dataset_list(config, spark)
        if running_local is False:
            display(df_datasets)

        count_string = str(df_datasets.count())
        msg = f"df_datasets unfiltered count:{count_string}"
        print(msg)
        df_columns = obj_env_metadata.get_column_list(config, spark, dbutils)

        # Make sure apply table filters to columns dataframe
        if filter_column_name is not None and filter_column_name != "all":
            filter_text = f"{filter_column_name} == '{filter_value}'"
            df_datasets = df_datasets.filter(filter_text)
            # filter for current project
            count_string = str(df_datasets.count())
            msg = f"df_datasets filtered count:{count_string}"
            print(msg)
            msg = f"filter_text:{filter_text}"
            print(msg)
            msg = f"dataset_name:{df_datasets}"
            print(msg)

        data_collect = df_datasets.collect()

        for dataset_metadata in data_collect:
            obj_dataset = davt_ds_metadata.DataSetMetaData()
            config_dataset = obj_dataset.get_configuration_for_dataset(config, dataset_metadata)
            if config_dataset["is_active"] is True:
                return_text = obj_dataset.save_dataset(config, spark, dbutils,
                                                       df_columns, config_dataset)
                print(return_text)

        return "Success"

    @staticmethod
    def run_analytics_processing(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config: dict, spark, dbutils,
                                 export_schema: str, filter_column_name: str, filter_value: str) -> str:
        """Run analytics processing.  This is the third step in the 5 step (IDEAS) process.

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (dict): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_
            export_schema (str): _description_
            filter_column_name (str): _description_
            filter_value (str): _description_

        Returns:
            str: Analytic processing status message
        """

        obj_ds_crud = davt_ds_crud.DataSetCrud()
        obj_ds_core = davt_ds_core.DataSetCore()

        environment = config["environment"]
        project_id = config["project_id"]

        if export_schema == "export":
            config["is_export_schema_required_override"] = True

        bronze_sps_config_pipelines_df = obj_env_metadata.get_pipeline_list(config, spark)

        if filter_column_name is not None and filter_column_name != "all":
            filter_text = f"(project_id == '{project_id}') and {filter_column_name} == '{filter_value}'"
            bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.filter(filter_text)
        data_collect = bronze_sps_config_pipelines_df.collect()

        for row in data_collect:
            obj_pipeline = davt_pl_metadata.PipelineMetaData()
            config_pipeline = obj_pipeline.get_configuration_for_pipeline(config, row)
            pipeline_name = config_pipeline['pipeline_name']
            # only a few views need to export schema metrics
            export_schema_metrics = config_pipeline['export_schema_metrics']
            execute_flag = config_pipeline["execute_flag"]
            pipeline_type = "databricks_sql"

            # configure to download and save sql only in dev
            # In future, add support for notebook pipelines in addition to sql pipelines
            if environment == "dev":
                save_flag = "save"
                print(f"save_flag: {save_flag}")
                response_text = ""
                response_text = obj_pipeline.save_pipeline_sql(config, config_pipeline)
                print(response_text)
            else:
                # save_flag = config_pipeline['save_flag']
                save_flag = 'skip_save'
                print(f'skip save requested: {pipeline_name}')

            # conditionally execute
            print(f"execute_flag: {execute_flag}")
            if execute_flag is None:
                execute_flag = 'skip_execute'
            else:
                if execute_flag == 'skip_execute':
                    print(f'skip execute requested: {pipeline_name}')
                else:
                    execute_flag = 'execute'
                    if pipeline_type == "databricks_sql":
                        print(f'execute_flag requested: {pipeline_name}')
                        config_pipeline = obj_pipeline.get_execute_pipeline_parameters(config, config_pipeline)
                        path_to_execute = config_pipeline["path_to_execute"]
                        arg_dictionary = config_pipeline["arg_dictionary"]
                        # time out in 15 minutes: 900 sec or 600 10 min
                        dbutils.notebook.run(path_to_execute, 900, arg_dictionary)
                    elif pipeline_type == "databricks_export":
                        print("run generic export")
                        export_format = "parquet"
                        environment = config["environment"]
                        query_name = config_pipeline["query_name"]
                        query_name = query_name.split(".", 1)[1]
                        davt_parquet_folder = config["davt_database_folder"].replace("/delta", "/" + export_format)
                        davt_parquet_path = davt_parquet_folder.rstrip("/") + ("/") + query_name + "." + export_format
                        sql_command = config_pipeline["view_name"]
                        sql_command = sql_command.replace("{environment}", environment)
                        print(f"sql_command:{sql_command}")
                        print(f"davt_parquet_path:{davt_parquet_path}")
                        df_export = spark.sql(f"{sql_command}")
                        df_export.repartition(1).write.format(export_format).mode("overwrite").save(davt_parquet_path)

            # conditionally export schema metrics
            # only a few views need to export schema metrics
            if export_schema_metrics is None:
                export_schema_metrics = 'skip_export'
                print(f'export_schema_metrics: {pipeline_name}')
            else:
                if export_schema_metrics == 'export':
                    sorted_df = obj_pipeline.get_view_dataframe(config, spark, config_pipeline)

                    # move row_id generation upstream to view and dataset
                    if set(['row_id']).issubset(sorted_df.columns) is False:
                        yyyy_param = config["yyyy"]
                        if yyyy_param is None:
                            yyyy_param = ""
                        mm_param = config["mm"]
                        if mm_param is None:
                            mm_param = ""
                        dd_param = config["dd"]
                        if dd_param is None:
                            dd_param = ""

                        row_id_keys = "column_name, full_dataset_name"

                        sorted_df = obj_ds_core.add_row_id_to_dataframe(sorted_df, row_id_keys, yyyy_param,
                                                                        mm_param, dd_param)
                    view_or_schema = "view"

                    if sorted_df is None:
                        print("Error: sorted_df is None")
                    schema_df = None
                    config_schema = obj_ds_crud.get_export_dataset_or_view_schema_config(config, config_pipeline, spark,
                                                                                         sorted_df, view_or_schema, schema_df)
                    print(str(config_schema))
                    schema_dataset_df = config_schema['schema_dataset_df']
                    schema_column_df = config_schema['schema_column_df']

                    obj_ds_crud.upsert(spark, config, dbutils, schema_dataset_df,
                                       config_schema['schema_full_dataset_name'],
                                       config_schema['schema_dataset_file_path'],
                                       config_schema['is_using_dataset_folder_path_override'],
                                       "parquet_delta", "sps", "calculated_table",
                                       False, config_schema['partitioned_by'], 'incremental')

                    obj_ds_crud.upsert(spark, config, dbutils, schema_column_df,
                                       config_schema['schema_full_dataset_name'],
                                       config_schema['schema_dataset_file_path'],
                                       config_schema['is_using_dataset_folder_path_override'],
                                       "parquet_delta", "sps", "calculated_table",
                                       False, config_schema['partitioned_by'], 'incremental')

        return "Success"

    @classmethod
    def on_dropdown_job_change(cls, change, config: dict, button_run) -> str:
        """Dropdown job on change handler

        Args:
            change (dict): _description_

        Returns:
            str: New Value
        """

        if change['type'] == 'change' and change['name'] == 'value':
            config['dropdown_job_name'] = change
            result = f"Click to run: {change['new']}"
            button_run.description = result
            button_run.tooltip = result
        else:
            result = "No job change"

        return result

    @classmethod
    def run_job_name(cls, obj_env, spark, job_name, config, dbutils) -> str:
        """Run a job by name

        Args:
            obj_env (_type_): _description_
            spark (_type_): _description_
            job_name (_type_): _description_
            config (_type_): _description_
            parameters (_type_): _description_
            dbutils (_type_): _description_

        Returns:
            str: status
        """

        print(f"job_name:{job_name}")
        result = ""
        ingress_folder_sps = config["ingress_folder_sps"]
        ingress_folder_sps = ingress_folder_sps.rstrip("/")
        config_jobs_path = f"{ingress_folder_sps}/bronze_sps_config_jobs.csv"
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
        if df_jobs.count() > 0:
            array_jobs = df_jobs.collect()
            j_a = array_jobs[0].asDict()
            export_schema = j_a.get('export_schema_metrics')
            if export_schema is None or export_schema == '':
                export_schema = "default"

            result = cls.run_job_action(obj_env, spark, config, dbutils,
                                        j_a.get('job_action'),
                                        export_schema,
                                        j_a.get('filter_column_name'),
                                        j_a.get('filter_value'))

        result = f"Finished processing:{result}"
        print(result)
        return result

    @classmethod
    def run_job_action(cls, obj_env, spark, config: dict, dbutils,
                       action, export_schema, filter_column_name="", filter_value="") -> str:
        """Runs job action step based on job metadata configuration. Jobs can contain multiple steps/actions.

        Args:
            obj_env (_type_): _description_
            spark (_type_): _description_
            parameters (dict): _description_
            dbutils (_type_): _description_
            action (_type_): _description_
            export_schema (_type_): _description_
            filter_column_name (_type_, optional): _description_. Defaults to empty string.
            filter_value (_type_, optional): _description_. Defaults to empty string.

        Returns:
            str: Results status message
        """

        if filter_column_name is not None:
            filter_column_name = filter_column_name.strip()

        if filter_value is not None:
            filter_value = filter_value.strip()

        if action == 'install_cluster_library':
            results = cls.install_cluster_library(config)
        elif action == 'get_cluster_library_status':
            results = cls.get_cluster_library_status(config)
        elif action == 'setup_project_mount':
            results = cls.setup_project_mount(config, spark, dbutils)
        elif action == 'trigger_pull_request':
            results = cls.trigger_pull_request(obj_env, config, dbutils)
        elif action == 'run_pull_request':
            results = cls.run_pull_request(obj_env, config)
        elif action == 'run_publish_release':
            results = cls.run_publish_release(obj_env, config)
        elif action == 'run_publish_config':
            results = cls.run_publish_config(obj_env, config, spark, dbutils)
        elif action == 'run_ingress_processing':
            results = cls.run_ingress_processing(obj_env, config, spark, dbutils,
                                                 filter_column_name, filter_value)
        elif action == 'run_data_processing':
            results = cls.run_data_processing(obj_env, config, spark, dbutils,
                                              export_schema, filter_column_name, filter_value)
        elif action == 'run_analytics_processing':
            results = cls.run_analytics_processing(obj_env, config, spark, dbutils,
                                                   export_schema, filter_column_name, filter_value)
        elif action == 'download_config':
            results = cls.download_config(obj_env, config, dbutils)
        else:
            results = 'unimplemented action'

        print(f"action:{action}:results:{results}")

        return results

    @classmethod
    def run_job_action_list(cls, config: dict, job_action_list: list,
                            obj_env_metadata: davt_env_metadata.EnvironmentMetaData, spark: object, dbutils: object):
        """Run a list of actions for a project configured for the specified job name

        Args:
            project_id (str)): DAVT two part project id: example: ddt_ops
            environment (str): Environment name: example: dev
            job_action_list (list): List of actions to run
            obj_env (str): DAVT EnvironmentCore object
            spark (object): Configured SparkSession
            dbutils (object)): Delta.io dbutils object
        """

        for j_a in job_action_list:
            export_schema = j_a.get('export_schema')
            if export_schema is None or export_schema == '':
                export_schema = "default"

            cls.run_job_action(obj_env_metadata, spark, config, dbutils,
                               j_a.get('action'),
                               export_schema,
                               j_a.get('filter_column_name'),
                               j_a.get('filter_value'))

    @staticmethod
    def run_ingress_processing(obj_env_metadata: davt_env_metadata.EnvironmentMetaData, config, spark, dbutils,
                               filter_column_name, filter_value) -> str:
        """Runs ingress processing:  This is the first step in the 5 step (IDEAS) process.

        Args:
            obj_env_metadata (davt_env_metadata.EnvironmentMetaData): _description_
            config (_type_): _description_
            spark (_type_): _description_
            dbutils (_type_): _description_
            filter_column_name (_type_): _description_
            filter_value (_type_): _description_

        Returns:
            str: Ingress processing status message
        """

        project_id = config["project_id"]
        running_local = config["running_local"]
        print(f"running_local:{running_local}")

        # setup database
        df_datasets = obj_env_metadata.get_dataset_list(config, spark)

        # In future, make sure to apply table filters to columns dataframe
        if filter_column_name is not None and filter_column_name != "all":
            filter_text = f"(project_id == '{project_id}') and {filter_column_name} == '{filter_value}'"
            filter_text = filter_text + " and is_active not in ('False', 'FALSE','false','0')"
            df_datasets = df_datasets.filter(filter_text)
            # filter for current project
            count_string = str(df_datasets.count())
            msg = f"df_datasets count:{count_string}"
            print(msg)
            msg = f"filter_text:{filter_text}"
            print(msg)
            msg = f"dataset_name:{df_datasets}"
            print(msg)

        data_collect = df_datasets.collect()

        for dataset_metadata in data_collect:
            obj_dataset = davt_ds_metadata.DataSetMetaData()
            config_dataset = obj_dataset.get_configuration_for_dataset(config, dataset_metadata)
            return_text = obj_dataset.copy_ingress_file(config, config_dataset)
            print(return_text)

        return "Success"
