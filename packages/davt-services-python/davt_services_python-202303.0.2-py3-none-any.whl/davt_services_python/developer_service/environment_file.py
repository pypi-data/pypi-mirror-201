""" Module for spark and os environment for developer_service with
 minimal dependencies. """

# library management
from importlib import util  # library management

# error handling
from subprocess import check_output, Popen, PIPE, CalledProcessError

import sys  # don't remove required for error handling
import os

# files
import glob
import fileinput
import codecs
import chardet

# error handling
import subprocess

# http
from urllib.parse import urlparse
import requests

import davt_services_python.developer_service.repo_core as davt_repo

# azcopy and adls
from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import DataLakeDirectoryClient
from azure.keyvault.secrets import SecretClient

# spark
from pyspark.sql import (SparkSession)
from pyspark.sql.types import (IntegerType, LongType, StringType, StructField,
                               StructType)

#  data
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    # import pyspark.pandas  as pd
    # bug - pyspark version will not read local files in the repo
    import pyspark.pandas as pd
else:
    import pandas as pd


class EnvironmentFile:
    """ EnvironmentFile class with minimal dependencies for the developer
    service.
    - This class is used to perform file and directory operations.
    """

    @staticmethod
    def class_exists() -> bool:
        """Basic check to make sure object is instantiated

        Returns:
            bool: true/false indicating object exists
        """
        return True

    @staticmethod
    def convert_abfss_to_https_path(abfss_path: str) -> str:
        """Converts abfs path to https path

        Args:
            abfss_path (str): abfss path

        Returns:
            str: https path
        """
        hostname = abfss_path.split('/')[2]
        file_system = hostname.split('@')[0]
        print(f"hostname:{hostname}")
        print(f"file_system:{file_system}")
        storage_account = hostname.split('@')[1]
        print(f"storage_account:{storage_account}")
        https_path = abfss_path.replace(hostname, storage_account + '/' + file_system)
        https_path = https_path.replace('abfss', 'https')
        return https_path

    @staticmethod
    def convert_windows_dir(folder_path: str) -> str:
        """Converts a window folder path to bash format

        Args:
            folder_path (str): path to convert

        Returns:
            str: _converted path
        """

        window_dir = "\\"

        if window_dir in folder_path:
            folder_path = folder_path.replace("\\", "/")
            folder_path = folder_path.lstrip("/") + "/"
        else:
            folder_path = folder_path.rstrip("/") + "/"

        return folder_path

    @staticmethod
    def execute(cmd) -> str:
        """Takes a command and executes it

        Args:
            cmd (_type_): Command to execute

        Raises:
            CalledProcessError: Error executing command

        Returns:
            str: output of command
        """

        result_string = ""

        with Popen(cmd,
                   stdout=PIPE,
                   bufsize=1,
                   universal_newlines=True) as p_output:
            if p_output is not None:
                stdout = p_output.stdout
                if stdout is not None:
                    for line in stdout:
                        # process line here
                        result_string = result_string + line
            else:
                result_string = "p_output is None"

        if p_output.returncode != 0:
            raise CalledProcessError(p_output.returncode, p_output.args)

        return result_string

    @staticmethod
    def download_file(url: str) -> str:
        """Downloads a file from a url
        May require refactoring if memory becomes an issue

        Args:
            url (str): url of the file to download

        Returns:
            str: local file name
        """
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as request_result:
            request_result.raise_for_status()
            with open(local_filename, 'wb') as file_result:
                for chunk in request_result.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    file_result.write(chunk)
        return local_filename

    @classmethod
    def prepend_line_to_file(cls, source_path: str, destination_path: str,
                             line_to_prepend: str) -> str:
        """Add line to the beginning of a file

        Args:
            source_path (str): _description_
            destination_path (str): _description_
            line_to_prepend (str): _description_

        Returns:
            str: Status of operation
        """

        result = "running"
        print(f"source_path: {source_path}")
        print(f"destination_path: {destination_path}")
        with open(source_path,
                  'r',
                  encoding='utf-8') as original:
            data = original.read()
        with open(destination_path,
                  'w',
                  encoding='utf-8') as modified:
            modified.write(f"{line_to_prepend}\n" + data)
        result = "Success"
        return result

    @classmethod
    def combine_files(cls, source_path: str, file_mask: str,
                      destination_path: str) -> str:
        """Joins/combines multilple files

        Args:
            source_path (str): _description_
            file_mask (str): _description_
            destination_path (str): _description_

        Returns:
            str: Status of operation
        """
        result = "running"
        source_files = f"{source_path}{file_mask}"
        all_files = glob.glob(source_files)
        with open(destination_path,
                  'w+',
                  encoding='utf-8',
                  newline='\n') as f_output:
            for filename in all_files:
                print(f"filename:{filename}")
                with open(filename,
                          'r',
                          encoding="utf-8",
                          newline='\n') as f_input:
                    for line in f_input:
                        f_output.write(line)
        result = "Success"
        return result

    @classmethod
    def rename_directory(cls, config: dict, source_path, new_directory_name) -> str:
        """Rename ABFSS directory

        Args:
            config (dict): _description_
            source_path (_type_): _description_
            new_directory_name (_type_): _description_

        Returns:
            str: rename_status
        """

        try:
            client_id = config['client_id']
            client_secret = config['client_secret']

            result = "file_adls_copy failed"

            if client_secret is None:
                azure_client_secret_key = str(config["azure_client_secret_key"])
                key = azure_client_secret_key
                client_secret = f"Environment variable: {key} not found"

            os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
            tenant_id = config['tenant']

            running_local = config['running_local']
            print(f"running_local:{running_local}")
            print(f"source_path:{source_path}")
            print(f"new_directory_name:{new_directory_name}")

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            storage_account_loc = urlparse(source_path).netloc
            storage_path = urlparse(source_path).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            account_url = f"https://{storage_account_loc}"

            service_client = DataLakeServiceClient(account_url=account_url,
                                                   credential=credential)
            file_system_client = service_client.get_file_system_client(storage_container)

            dir_path = storage_path.replace(f"{storage_container}" + "/", "")

            is_directory = None
            directory_client: DataLakeDirectoryClient
            try:
                directory_client = file_system_client.get_directory_client(dir_path)
                if directory_client.exists():
                    is_directory = True
                else:
                    is_directory = True

                if is_directory:
                    directory_client.rename_directory(new_directory_name)
                    result = "Success"
                else:
                    result = f"rename_directory failed: {dir_path} does not exist"
            except Exception as ex:
                directory_client = DataLakeDirectoryClient("empty", "empty", "empty")
                print(ex)
                result = "rename_directory failed"
        except Exception as ex_rename_directory:
            print(ex_rename_directory)
            result = "rename_directory failed"
        result = str(result)
        return result

    @classmethod
    def folder_adls_create(cls, config, dir_path: str, dbutils) -> str:

        running_local = config['running_local']
        client_id = config['client_id']
        client_secret = config['client_secret']

        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret = f"Environment variable: {azure_client_secret_key} not found"

        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        tenant_id = config['tenant']

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
        file_system_client = service_client.get_file_system_client(storage_container)
        directory_client = file_system_client.create_directory(dir_path)

        return "True"

    @classmethod
    def file_adls_copy(cls, config, source_path: str, destination_path: str, from_to: str, dbutils) -> str:
        """copies local file to azure storage

        Args:
            config (dict): configuration dictionary
            source_path (str): source path to copy
            destination_path (str): destination path of copy or 'bytes' if should return byte array
            from_to (str): either BlobFSLocal or LocalBlobFS
            dbutils: Databricks dbutils object
        Returns:
            str: copy_status
        """
        result = "file_adls_copy failed"
        running_local = config['running_local']
        client_id = config['client_id']
        client_secret = config['client_secret']

        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret = f"Environment variable: {azure_client_secret_key} not found"

        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        tenant_id = config['tenant']

        print(f"running_local:{running_local}")
        print(f"from_to:{from_to}")
        print(f"source_path:{source_path}")
        print(f"destination_path:{destination_path}")

        if (running_local is True and (from_to == 'BlobFSLocal' or from_to == 'LocalBlobFS')):

            p_1 = f"--application-id={client_id}"
            p_2 = f"--tenant-id={tenant_id}"
            arr_azcopy_command = ["azcopy", "login", "--service-principal", p_1, p_2]
            arr_azcopy_command_string = ' '.join(arr_azcopy_command)
            print(arr_azcopy_command_string)

            try:
                check_output(arr_azcopy_command)
                result_1 = f"login --service-principal {p_1} to {p_2} succeeded"
            except subprocess.CalledProcessError as ex_called_process:
                result_1 = str(ex_called_process.output)

            print(result_1)

            if from_to == 'BlobFSLocal':
                arr_azcopy_command = [
                    'azcopy', 'copy', f"{source_path}", f"{destination_path}",
                    f'--from-to={from_to}', '--recursive',
                    '--trusted-microsoft-suffixes=', '--log-level=INFO']
            elif from_to == 'LocalBlobFS':
                arr_azcopy_command = [
                    'azcopy', 'copy', f"{source_path}", f"{destination_path}",
                    '--log-level=DEBUG', f'--from-to={from_to}']
            else:
                arr_azcopy_command = [f"from to:{from_to} is not supported"]

            arr_azcopy_command_string = ' '.join(arr_azcopy_command)
            print(arr_azcopy_command_string)

            try:
                check_output(arr_azcopy_command)
                result_2 = f"copy from {source_path} to {destination_path} succeeded"
            except subprocess.CalledProcessError as ex_called_process:
                result_2 = str(ex_called_process.output)

            result = result_1 + result_2
        elif ((running_local is False) and from_to == 'BlobFSLocal'):
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            storage_account_loc = urlparse(source_path).netloc
            storage_path = urlparse(source_path).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            account_url = f"https://{storage_account_loc}"
            service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
            file_system_client = service_client.get_file_system_client(storage_container)
            dir_path = storage_path.replace(f"{storage_container}" + "/", "")
            is_directory = None
            directory_client: DataLakeDirectoryClient
            try:
                directory_client = file_system_client.get_directory_client(dir_path)
                if directory_client.exists():
                    is_directory = True
                else:
                    is_directory = True
            except Exception as ex:
                directory_client = DataLakeDirectoryClient("empty", "empty", "empty")
                print(ex)

            obj_repo = davt_repo.RepoCore()

            if is_directory is True:

                azure_files = []

                try:
                    azure_files = file_system_client.get_paths(path=dir_path)
                except Exception as ex:
                    print(ex)

                for file_path in azure_files:
                    print(str(f"file_path:{file_path}"))
                    file_path_name = file_path.name
                    file_name = os.path.basename(file_path_name)
                    file_client = directory_client.get_file_client(file_path)
                    file_data = file_client.download_file()
                    file_bytes = file_data.readall()
                    file_string = file_bytes.decode("utf-8")
                    first_200_chars_of_string = file_string[0:200]
                    destination_file_path = destination_path + "/" + file_path_name

                    if len(file_string) > 0:
                        try:
                            # os.remove(destination_file_path)
                            dbutils.fs.rm(destination_file_path)
                        except OSError as ex_os_error:
                            # if failed, report it back to the user
                            print(f"Error: {ex_os_error.filename} - {ex_os_error.strerror}.")
                        try:
                            print(f"dbutils.fs.put({destination_file_path}, {first_200_chars_of_string}, True)")
                            result = dbutils.fs.put(destination_file_path, file_string, True)
                        except Exception as ex_os_error:
                            # if failed, report it back to the user
                            print(f"Error: {ex_os_error}.")

                        content_type = "bytes"
                        result = obj_repo.import_file(config, file_bytes, content_type, destination_file_path)

                    else:
                        result = f"destination_file_path:{destination_file_path} is empty"
                    # file_to_copy = io.BytesIO(file_bytes)
                    # print(f"destination_file_path:{destination_file_path}")
            else:
                file_path = storage_path.replace(f"{storage_container}" + "/", "")
                print(f"file_path:{file_path}")
                file_client = file_system_client.get_file_client(file_path)
                file_data = file_client.download_file()
                file_bytes = file_data.readall()
                file_string = file_bytes.decode("utf-8")
                file_name = os.path.basename(file_path)
                destination_file_path = destination_path + "/" + file_name
                first_200_chars_of_string = file_string[0:500]
                if len(file_string) > 0:

                    try:
                        # os.remove(destination_file_path)
                        dbutils.fs.rm(destination_file_path)
                    except OSError as ex_os_error:
                        # if failed, report it back to the user
                        print(f"Error: {ex_os_error.filename}-{ex_os_error.strerror}.")

                    try:
                        print(f"dbutils.fs.put({destination_file_path}, {first_200_chars_of_string}, True)")
                        result = dbutils.fs.put(destination_file_path, file_string, True)
                    except Exception as ex_os_error:
                        # if failed, report it back to the user
                        print(f"Error: {ex_os_error}.")

                    content_type = "bytes"
                    result = obj_repo.import_file(config, file_bytes, content_type, destination_file_path)
                else:
                    result = f"destination_file_path:{destination_file_path} is empty"
        elif ((running_local is False) and from_to == 'LocalBlobFS'):
            url = destination_path
            storage_account_loc = urlparse(url).netloc
            storage_path = urlparse(url).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            file_name = os.path.basename(destination_path)
            dir_path = storage_path.replace(file_name, "")
            dir_path = dir_path.replace(storage_container + '/', "")
            account_url = f"https://{storage_account_loc}"
            print(f"account_url:{account_url}")
            print(f"url:{url}")
            print(f"storage_path:{storage_path}")
            print(f"storage_container:{storage_container}")
            print(f"dir_path:{dir_path}")
            print(f"file_name:{file_name}")

            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
            file_system_client = service_client.get_file_system_client(storage_container)
            directory_client = file_system_client.get_directory_client(dir_path)
            file_client = directory_client.create_file(file_name)
            local_file = open(source_path, "r", encoding="utf-8")
            file_contents = local_file.read()
            file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
            result = file_client.flush_data(len(file_contents))

            # with open(source_path) as f_json:
            #     json_data = json.load(f_json)
            # result = file_client.upload_data(json_data, overwrite=True, max_concurrency=5)

            # file_client = file_system_client.get_file_client(file_path)
            # file_data = file_client.download_file(0)
            # result = file_data.readall()

            # print(f" dbutils.fs.cp({source_path}, {destination_path})")
            # result = dbutils.fs.cp(source_path, destination_path)
        else:
            result = "invalid config: must download/client config files from azure to local"
            result = result + " - functionality not available on databricks"
            print(result)

        result = str(result)

        return result

    @classmethod
    def get_file_size(cls, running_local: bool, path: str, dbutils, spark: SparkSession) -> int:
        """Takes in file path, dbutils object and spark obejct, returns file size of provided path

        Args:
            path (str): path to check file size
            dbutils (object): Databricks dbutils object
            spark (SparkSession): spark session object

        Returns:
            int:  file size
        """

        if dbutils is not None:

            file_exists = cls.file_exists(running_local, path, dbutils)

            if file_exists is True:
                ddl_schema_3 = StructType(
                    [
                        StructField("path", StringType()),
                        StructField("name", StringType()),
                        StructField("size", IntegerType())
                    ]
                )

                ddl_schema_4 = StructType(
                    [
                        StructField("path", StringType()),
                        StructField("name", StringType()),
                        StructField("size", IntegerType()),
                        StructField("modification_time", LongType()),
                    ]
                )

                print(f"command: dbutils.fs.ls({path})")
                sk_list = dbutils.fs.ls(path)
                print(f"num_elements:{len(sk_list)}")

                df_file_list = None

                if len(sk_list) > 0:
                    if len(sk_list[0]) == 3:
                        df_file_list = spark.createDataFrame(sk_list, ddl_schema_3)
                    elif len(sk_list[0]) == 4:
                        df_file_list = spark.createDataFrame(sk_list, ddl_schema_4)

                    if df_file_list is None:
                        file_size = 0
                    else:
                        first = df_file_list.first()
                        if first is not None:
                            file_size = first.size
                        else:
                            file_size = -1

                    # df_file_list = df_file_list.toPandas()
                    # file_size = df_file_list.iloc[0, df_file_list.columns.get_loc("size")]

                    file_size = int(str(file_size))
                else:
                    file_size = -1
            else:
                file_size = -1
        else:
            file_size = -1

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

        if running_local is True:
            b_exists = os.path.exists(path)
        else:
            try:
                path = path.replace("/dbfs", "")
                if dbutils is not None:
                    dbutils.fs.ls(path)
                    b_exists = True
                else:
                    b_exists = False
            except Exception as exception_result:
                if "java.io.FileNotFoundException" in str(exception_result):
                    b_exists = False
                else:
                    b_exists = False
                    raise

        return b_exists

    @classmethod
    def copy_url_to_blob(cls, config: dict, src_url: str,
                         dest_path: str, file_name: str) -> str:
        """download file from source url and upload the file to the azure storage destination path

        Args:
            src_url (str): description
            dest_path (str): description
            file_name (str): description

        Returns:
            str: upload status message
        """

        info_message = f"copy_url_to_blob: src_url:{src_url}, dest_path:{dest_path}, file_name:{file_name}"
        print(info_message)

        client_id = config['client_id']
        client_secret = config['client_secret']
        tenant_id = config['tenant']
        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret=f"Environment variable: {azure_client_secret_key}not found"
            print(client_secret)
        credential = ClientSecretCredential(tenant_id, client_id,
                                            client_secret)
        storage_account_loc = urlparse(dest_path).netloc
        storage_path = urlparse(dest_path).path
        storage_path_list = storage_path.split("/")
        storage_container = storage_path_list[1]
        account_url = f"https://{storage_account_loc}"
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        dir_path = storage_path.replace(f"{storage_container}" + "/", "")
        print(f"dir_path:{dir_path}")
        file_system_client = service_client.get_file_system_client(storage_container)
        directory_client = file_system_client.get_directory_client(dir_path)
        file_response = requests.get(src_url)
        file_data = file_response.content
        try:
            file_client = directory_client.create_file(file_name)
            result = file_client.upload_data(file_data, overwrite=True, max_concurrency=5)
        except Exception as ex:
            print(ex)
            result = "upload failed"
        return result


