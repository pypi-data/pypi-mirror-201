""" Module for security_core for developer_service with minimal dependencies. """

# core
from distutils.log import error
import os
import sys  # don't remove required for error handling
sys.path.append(".")

# errors
import traceback  # don't remove required for error handling

# text
import json
from html.parser import HTMLParser  # web scraping html

# http
import requests

# security
from adal import AuthenticationContext

import davt_services_python.developer_service.environment_logging as davt_env_log

class SecurityCore:
    """ Security functions with minimal dependencies
    """

    @classmethod
    def acquire_access_token_with_client_credentials(cls, sp_client_id: str, sp_client_secret: str, sp_tenant_id: str,
                                                     sp_redirect_url: str, sp_authority_host_url: str,
                                                     sp_azure_databricks_resource_id: str, project_id: str) -> dict:
        """Takes in config dictionary, client_id and client secret and returns config_user with access_token
        - initial call

        Args:
            config (dict): global config dictionary
            sp_client_id (str): service principal client id
            sp_client_secret (str): service principal secret
            sp_tenant_id (str): service principal tenant id
            sp_redirect_url (str): service principal redirect url
            sp_azure_databricks_resource_id (str): service principal azure databricks resource id
            project_id(str): project id for logging

        Returns:
            dict: config_user dictionary with access_token populated
        """

        info_message = f"acquire_access_token_with_client_credentials for {project_id}"
        print(info_message)

        config_user = cls.setup_user_configuration(sp_client_id, sp_client_secret, sp_tenant_id, sp_redirect_url,
                                                   sp_authority_host_url, sp_azure_databricks_resource_id)

        authority_url = config_user["authority_url"]
        azure_databricks_resource_id = config_user["azure_databricks_resource_id"]
        print(f"authority_url:{authority_url}")
        print(f"sp_client_id:{sp_client_id}")
        print(f"azure_databricks_resource_id:{azure_databricks_resource_id}")
        context = AuthenticationContext(authority_url)

        token_response = {"accessToken": "not_set"}

        #resource='https://management.core.windows.net/'
        #resource = "https://database.windows.net/"

        # Get token using username password first
        try:
            token_response = context.acquire_token_with_client_credentials(
                azure_databricks_resource_id, sp_client_id, sp_client_secret)
        except Exception as ex_access_token_with_client_credentials:
            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()
            error_string = "Error: Unable to acquire_access_token_with_client_credentials with sp_client_id"
            error_string = error_string + f":{sp_client_id}: Details: {str(ex_access_token_with_client_credentials)}"
            error_string = error_string + ": Extended:"
            for trace in trace_back:
                error_string = f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}"
                error_string = error_string + f", Message : {trace[3]}, Type : {ex_type}"
                error_string = error_string + f", Value : {ex_value}"
                stack_trace.append(error_string)
            print(error_string)
        # self.validate_token_response_username_password(token_response)

        print(f"token_response: [REDACTED]: length:{len(str(token_response))}")
        # Use returned refresh token to acquire a new token.
        access_token = token_response["accessToken"]
        config_user["access_token"] = access_token

        return config_user

    @classmethod
    def acquire_access_token_with_refresh_token(cls, sp_client_id: str, sp_client_secret: str, sp_tenant_id: str,
                                                sp_redirect_url: str, sp_authority_host_url: str,
                                                sp_azure_databricks_resource_id: str) -> dict:
        """Takes in config dictionary, client_id and client secret and returns config_user with access_token
        - refresh token call

        Args:
            config (dict): global config dictionary
            sp_client_id (str): service principal client id
            sp_client_secret (str): service principal secret

        Returns:
            dict: config_user with refresh_token populated
        """

        config_user = cls.setup_user_configuration(sp_client_id, sp_client_secret, sp_tenant_id, sp_redirect_url,
                                                   sp_authority_host_url, sp_azure_databricks_resource_id)

        if config_user is None:
            print("config_user is None")
        else:
            print(f"config_user exists: {str(config_user)}")

        authority_url = config_user["authority_url"]
        # client_id = config_user['client_id']
        azure_databricks_resource_id = config_user["azure_databricks_resource_id"]
        print(f"creating context for authority_url:{authority_url}")
        context = AuthenticationContext(authority_url)
        if context is None:
            print(f"AuthenticationContext: None : not acquired for authority_url:{authority_url}")
        elif len(str(context)) == 0:
            print(f"AuthenticationContext: empty string : not acquired for authority_url:{authority_url}")
        else:
            print(f"AuthenticationContext acquired for authority_url:{authority_url}")

        user_id = "zfi4@cdc.gov"  # TO DO MAKE Configurable
        print(f"attempting to acquire token for azure_databricks_resource_id:{azure_databricks_resource_id}")
        token_response = context.acquire_token(azure_databricks_resource_id, user_id, sp_client_id)

        if token_response is None:
            print(f"token_response not found:{str(token_response)}")
            config_user["refresh_token"] = "error"
        else:
            t_s = f"acquired token_response:{str(token_response)} for azure_databricks_resource_id"
            t_s = t_s + f":{str(azure_databricks_resource_id)}"
            refresh_token = token_response["refreshToken"]
            config_user["refresh_token"] = refresh_token

        config_user_result = cls.refresh_access_token(config_user)

        return config_user_result

    @staticmethod
    def setup_user_configuration(sp_client_id: str, sp_client_secret: str, sp_tenant_id: str, sp_redirect_url: str,
                                 sp_authority_host_url: str, sp_azure_databricks_resource_id: str) -> dict:
        """Takes in a config dictionary, client_id and client_secret and returns populated config_user dictionary

        Args:
            config (dict): global config dictionary
            sp_client_id (str): service principal client id
            sp_client_secret (str): service principal client secret
            sp_tenant_id (str): service principal tenant id
            sp_redirect_url (str): service principal redirect url
            sp_authority_host_url (str): service principal authority host url
            sp_azure_databricks_resource_id (str): service principal azure databricks resource id

        Returns:
            dict: populated config_user dictionary
        """

        sp_authority_url = "".join([sp_authority_host_url.rstrip("/"), "/", sp_tenant_id])

        # todo change from check if all exist rather than any
        # client_secret_exists = coalesce(sp_tenant_id, sp_redirect_url, sp_client_id, sp_client_secret)

        # if (client_secret_exists is None):
        #    client_secret_exists = False

        config_user = {
            "tenant": sp_tenant_id,
            "client_id": sp_client_id,
            "redirect_uri": sp_redirect_url,
            "client_secret": sp_client_secret,
            "authority_host_url": sp_authority_host_url,
            "azure_databricks_resource_id": sp_azure_databricks_resource_id,
            "authority_url": sp_authority_url,
        }

        # print(f"config_user:{str(config_user)}")
        return config_user

    @staticmethod
    def refresh_access_token(config_user: dict) -> dict:
        """Takes in config_user dictionary, returns config_user with access and refresh token

        Args:
            config_user (dict): config_user dictionary

        Returns:
            dict: config_user dictionary populated with with refresh token
        """

        authority_url = config_user["authority_url"]
        client_id = config_user["client_id"]
        client_secret = config_user["client_secret"]
        refresh_token = config_user["refresh_token"]
        azure_databricks_resource_id = config_user["azure_databricks_resource_id"]

        context = AuthenticationContext(authority_url)
        token_response = context.acquire_token_with_refresh_token(
            refresh_token, client_id, azure_databricks_resource_id, client_secret
        )

        refresh_token = token_response["refreshToken"]
        access_token = token_response["accessToken"]

        config_user["refresh_token"] = refresh_token
        config_user["access_token"] = access_token

        print(str("config_user:{config_user}"))

        return config_user

    @staticmethod
    def get_pat_tokens(config: dict, token: str):
        """Takes in a config dictionary, token and base_path, returns populated list of pat tokens

        Args:
            config (dict): global config dictionary
            token (str): token

        Returns:
            list: list of pat tokens
        """

        databricks_instance_id = config["databricks_instance_id"]
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/preview/permissions/authorization/tokens"

        print(f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers)
        data = None

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received credentials with length : {len(str(response_text))} when posting to : "
            msg = msg + "{url}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            results = data["access_control_list"]

        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")
            results = []

        return results

    @staticmethod
    def get_credentials_git(config: dict, token: str):
        """Takes in a config dictionary, token and base_path, returns populated list of files

        Args:
            config (dict): global config dictionary
            token (str): token
            base_path (str): path to list files

        Returns:
            list: list of files at the path location
        """

        databricks_instance_id = config["databricks_instance_id"]
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/git-credentials"

        print(f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers)
        data = None

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received credentials with length : {len(str(response_text))} when posting to : "
            msg = msg + "{url}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            results = data["credentials"]

        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")
            results = []

        return results

    @staticmethod
    def set_credentials_git(config: dict, token: str):
        """Takes in a config dictionary, token and base_path, returns populated list of files

        Args:
            config (dict): global config dictionary
            token (str): token
            base_path (str): path to list files

        Returns:
            list: list of files at the path location
        """

        databricks_instance_id = config["databricks_instance_id"]
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/git-credentials"

        print(f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers)
        data = None

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received credentials with length : {len(str(response_text))} when posting to : "
            msg = msg + "{url}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            results = data["credentials"]

        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")
            results = []

        return results

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
