""" Module for rep_core for it_admin_service that handles repository and cluster functions with minimal dependencies. """

import os
import sys  # don't remove required for error handling

import traceback  # don't remove required for error handling
from importlib import util  # library management

from calendar import c
import json
from html.parser import HTMLParser  # web scraping html
from string import Formatter
import base64
import csv
import requests
from io import BytesIO

from datetime import date, datetime


# http
from urllib.parse import urlparse

# certs
import certifi

class RepoCore:

    @staticmethod
    def describe_cluster_library_state(library_object, cluster_id, status):
        """Converts cluster library status response to a verbose message"""

        lib_title = library_object.title()
        lib_obj = library_object
        ni_msg = f"{lib_title} library is not installed on cluster {cluster_id}."
        inst_msg = f"{lib_obj} library is already installed on cluster {cluster_id}."
        pend_msg = "Pending installation of {} library on cluster {} . . ."
        resolve_msg = f"Retrieving metadata for the installation of {lib_obj} library on cluster {cluster_id} . . ."
        install_msg = f"Installing {lib_obj} library on cluster {cluster_id} . . ."
        failed_msg = f"{lib_title} library failed to install on cluster {cluster_id}."
        uninst_msg = f"{lib_title} library installed on cluster {cluster_id} has been marked for removal upon restart."

        result_map = {
            "NOT_INSTALLED": ni_msg,
            "INSTALLED": inst_msg,
            "PENDING": pend_msg,
            "RESOLVING": resolve_msg,
            "INSTALLING": install_msg,
            "FAILED": failed_msg,
            "UNINSTALL_ON_RESTART": uninst_msg
        }

        return result_map[status.upper()]

    @staticmethod
    def get_cicd_destination_path(config_folder: str) -> str:
        """Create file path for cicd storage event trigger

        Args:
            config (dict): configuration dictionary

        Returns:
            str: cicd destination path

        """

        cicd_action_folder = config_folder.replace('config', 'cicd')

        current_date_time = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")

        cicd_action_folder = cicd_action_folder.replace('abfss', 'https')
        url = urlparse(cicd_action_folder)
        container = url.netloc.split("@")[0]
        base_address = url.netloc.split("@")[1]
        path = url.path
        destination_path = f"https://{base_address}/{container}{path}pull_request_{current_date_time}.json"

        return destination_path

    @staticmethod
    def call_databricks_install_api(config, end_point, body, method="GET", verbose=True):
        """Execute HTTP request against Databricks REST API 2.0"""

        token = config['access_token']
        domain = config["davt_databricks_instance_id"]
        base_url = f"https://{domain}/api/"
        cluster_id = config['davt_databricks_cluster']

        bearer = "Bearer " + token
        headers = {"Authorization": bearer, "Content-Type": "application/json"}

        method = method.upper()
        url = base_url + end_point

        if method == "GET":
            response_install = requests.get(url, headers=headers, json=body)
        elif method == "POST":
            response_install = requests.post(url, headers=headers, json=body)

        data = None

        try:
            data = json.loads(response_install.text)
            response_install_text = json.dumps(response_install.json())
            print("- response : success  -")
            response_install_text_message = "Received Cluster API Response : "
            response_install_text_message += f"{response_install_text} when posting to : {url}  "
            response_install_text_message += f"to install library: {body}"
            response_install_text_message += f"to {response_install}"

            if response_install.status_code == 200:
                statuses = response_install.json()
                if "library_statuses" in statuses:
                    for status in statuses["library_statuses"]:
                        if status["library"] == "TODO":
                            if verbose is True:
                                msg = cls.describe_cluster_library_state("library_source", cluster_id, status["status"])
                                response_install_text_message += msg
                            else:
                                response_install_text_message += status["status"]
                        else:
                            response_install_text_message += str(status)

        except Exception as exception_check:
            html_filter = HTMLFilter()
            html_filter.feed(response_install.text)
            response_install_text_message = html_filter.text
            print(f"- response : error - {str(exception_check)}")
            print("Error SAVE-PYTHON-RESPONSE converting response")
            print(f"text:{response_install} to json")

        if data is None:
            response_install_text_message = "Error Install Library"

        return response_install_text_message

    @classmethod
    def get_cluster_library_status(cls, config, library_source, properties, verbose=True):
        """Gets the current library status """

        library_source = library_source.lower()

        # Validate input
        error_message_1 = "Error: Invalid library source specified. Valid sources are: jar, egg, whl, pypi, maven, cran"
        assert library_source in ("jar", "egg", "whl", "pypi", "maven", "cran"), error_message_1
        assert properties is not None, "Error: Empty properties provided"

        # Get the cluster ID from the Spark environment
        cluster_id = config['davt_databricks_cluster']

        # Set default result to not installed
        result = cls.describe_cluster_library_state(library_source, cluster_id, "NOT_INSTALLED")

        # Execute REST API request to get the library statuses
        endpoint = f"2.0/libraries/cluster-status?cluster_id={cluster_id}"
        result = cls.call_databricks_install_api(config, endpoint, None, "GET", verbose)

        return result

    @classmethod
    def install_cluster_library(cls, config, library_source, content_data):
        """
        Installs a cluster library given correct source and properties are provided
        For examples see https://docs.databricks.com/api/latest/libraries.html#install
        """

        library_file = content_data
        library_source = library_source.lower()

        # Validate input
        err_msg = "Error: Invalid library source specified. Valid sources are: jar, egg, whl, pypi, maven, cran"
        assert library_source in ("jar", "egg", "whl", "pypi", "maven", "cran"), err_msg
        assert library_file is not None, "Error: Empty library_file provided"

        # Get the cluster ID from the Spark environment
        cluster_id = config['davt_databricks_cluster']

        status = cls.get_cluster_library_status(config, library_source, library_file, False).upper()
        if status != "INSTALLED":
            # Create the HTTP request body based on the cluster ID, library source and properties
            libraries = f'"{library_source}": "{library_file}"'
            json_string = '{"cluster_id": "' + cluster_id + '", "libraries":[{' + libraries + '}]}'
            print(f"json_string:{json_string}")
            body = json.loads(json_string)
            # Execute REST API request to install the library
            result = cls.call_databricks_install_api(config, "2.0/libraries/install", body, "POST")
            if result == '- response : success  -':
                print("Installation started . . .")
            else:
                print(result)
        else:
            print(cls.describe_cluster_library_state(library_source, cluster_id, status))

        return status

    @staticmethod
    def write_issues(r, csvout):
        "output a list of issues to csv"
        if not r.status_code == 200:
            raise Exception(r.status_code)
        for issue in r.json():
            Tag=[]
            labels = issue['labels']
            for label in labels:
                Tag.append(label['name'])

            csvout.writerow([issue['number'], issue['title'].encode('utf-8'),Tag,issue['state'] ,issue['created_at'], issue['closed_at']])

    @classmethod
    def import_issues_to_csv_from_github(cls, config: dict) -> str:
        """Uses basic authentication (Github username + password) to retrieve Issues
        from a repository that username has access to and writes the issues to a csv file.
        Supports Github API v3.

        Args:
            config (dict): Environment configuration dictionary

        Returns:
            str: Import status message
        """

        GITHUB_USER = 'USER NAME'
        GITHUB_PASSWORD = 'PASSWORD'
        REPO = 'REPO NAME'  # format is username/repo
        ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
        AUTH = (GITHUB_USER, GITHUB_PASSWORD)
        arg="?state=all"

        response = requests.get(ISSUES_FOR_REPO_URL+arg)
        file_csv = '%s-issues.csv' % (REPO.replace('/', '-'))
        file_csv_o = open(file_csv, 'wb')
        out_csv = csv.writer(file_csv_o)
        out_csv.writerow(('id', 'Title', 'Tag', 'State', 'Open Date', 'Close Date'))

        cls.write_issues(r, out_csv)

        #more pages? examine the 'link' header returned
        if 'link' in response.headers:
            pages = dict(
                [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                    [link.split(';') for link in
                        response.headers['link'].split(',')]])

            while 'last' in pages and 'next' in pages:
                response = requests.get(pages['next'], auth=AUTH)
                cls.write_issues(response, out_csv)
                if pages['next'] == pages['last']:
                    break
                pages = dict(
                [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                    [link.split(';') for link in
                        response.headers['link'].split(',')]])

        file_csv_o.close()

        return "Success"

    @staticmethod
    def import_file(config, content_data, content_type, file_path) -> bool:
        """Imports file from abfss to repo library

        Args:
            config (_type_): _description_
            content_data (_type_): _description_
            content_type (_type_): _description_
            file_path (_type_): _description_

        Returns:
            bool: _description_
        """

        environment = config["environment"]
        project_id = config["project_id"]
        project_id_root = config["project_id_root"]
        file_name = os.path.basename(file_path)
        databricks_instance_id = config["databricks_instance_id"]
        token = config['access_token']
        bearer = "Bearer " + token
        headers = {"Authorization": bearer, "Content-Type": "application/json"}
        headers_redacted = str(headers).replace(bearer, "[bearer REDACTED]")
        api_version = "/api/2.0"
        databricks_instance_id = config["databricks_instance_id"]
        api_command = "/workspace/import"
        url = f"https://{databricks_instance_id}{api_version}{api_command}"

        file_path = file_path.replace("/Workspace", "")

        print(f"content_type:{content_type}")
        print(f"url:{url}")

        if content_type == "bytes":
            headers_import = {"Authorization": bearer} # , "Content-Type": "multipart/form-data"
            headers_redacted = str(headers_import).replace(
                bearer, "[bearer REDACTED]"
            )
            try:
                content_data.decode("UTF-8")
            except (UnicodeDecodeError, AttributeError):
                content_data = bytes(content_data, 'utf-8')
                pass

            files = {"upload_file": content_data}

            multipart_form_data = {
                'path': f"{file_path}"
            }

            print(f"multipart_form_data:{str(multipart_form_data)}")
            print(f"headers:{headers_redacted}")

            # binary
            # https://dbc-a1b2345c-d6e7.cloud.databricks.com/api/2.0/workspace/import \
            # --header 'Content-Type: multipart/form-data' \
            # --form path=/Users/me@example.com/MyFolder/MyNotebook \
            # --form content=@myCode.py.zip

            response_binary = DAVTObject()
            response_binary.text = 'Empty. Unable to retrieve post response'
            # data=multipart_form_data,
            try:
                response_binary = requests.post(url=url, files=files, data=multipart_form_data, headers=headers_import)
                print(f"post : success : {url} ")
                response_binary_text = json.loads(response_binary.text)
                response_binary_text = json.dumps(response_binary_text.json())
                print(f"parse : success : {url}")
                response_binary_text_message = "Received Cluster API Response : "
                response_binary_text_message += f"{response_binary_text} when posting to : {url}  "
                response_binary_text_message += f"to import file: {file_path}"
            except Exception as exception_check:
                html_filter = HTMLFilter()
                html_filter.feed(response_binary.text)
                response_install_text_message = html_filter.text
                print(f"url : error - {str(exception_check)}")
                print("Error IMPORT-FILE-RESPONSE")
                print(f"response error code:{str(response_binary)}")
                print(f"response error message:{response_install_text_message}")
        elif content_type == "text":

            # text
            # curl -n -X POST https://<databricks-instance>/api/2.0/workspace/import
            # -F path="/Users/user@example.com/new-notebook" -F format=SOURCE -F language=SCALA -F overwrite=true -F content=@notebook.scala

            headers_import = {"Authorization": bearer, "Accept": "application/json"}
            headers_redacted = str(headers_import).replace(
                bearer, "[bearer REDACTED]"
            )

            print(f"headers:{headers_redacted}")
            print(f"json:{str(content_data[ 0 : 100 ])}...")

            response_json = requests.post(
                url=url, json=content_data, headers=headers_import
            )

        return True

    @classmethod
    def pull_repository_latest(
        cls,
        config: dict,
        token: str,
        base_path: str,
        repository_name: str,
        branch_name: str
    ) -> str:
        """Pulls the lastest repository branch for the given repo

        Args:
            config (dict): global config dictionary
            token (str): security token
            base_path (str): reository base path location to pull
            repository_name (str): repository name to pull
            branch_name (str): repository branch name to pull

        Returns:
            str: result message from pull request
        """

        databricks_instance_id = config["databricks_instance_id"]
        json_text = {"path": base_path}
        headers = {"Authentication": f"Bearer {token}"}
        api_url = f"https://{databricks_instance_id}"
        url = f"{api_url}/api/2.0/workspace/list"
        verify = certifi.where()

        print(f"------- Fetch {base_path}  -------")
        print(f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers, json=json_text, verify=verify)
        data = None

        try:
            data = response.json()
            response_text_fetch = f"Suceess: Received list_repos with length : {len(str(data))}"
            response_text_fetch = response_text_fetch + f" when posting to : {url}"
            print(f"{response_text_fetch}")
            print(f"listed files for : {base_path}")
            print(str(data))
            lst = data["objects"]
            repos = list(filter(lambda itm: str(Path(itm['path']).stem).upper() == repository_name.upper(), lst))

            if repos[0] is None:
                repo_data = "Error Repo Not found"
            else:
                repo_object = repos[0]
                repo_id = repo_object['object_id']
                url = f"{api_url}/api/2.0/repos/{repo_id}"
                print(f"repo_id:{repo_id} branch_name:{branch_name}")
                repo_data = requests.patch(url=url, headers=headers, verify=verify, json={'branch': branch_name}).json()
        except Exception as exception_object:
            filter_object = HTMLFilter()
            filter_object.feed(response.text)
            response_text = filter_object.text
            repo_data = f"Response : error - {exception_object}: {response_text}"

        print(repo_data)

        return repo_data

class DAVTObject(object):
    pass

class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data
