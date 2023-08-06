""" Module for job funciontality with minimal dependencies. """

import os
import sys  # don't remove required for error handling
from pathlib import Path
from datetime import date

import traceback  # don't remove required for error handling

class JobCore:
    """ JobCore class with minimal dependencies for the developer service.
    - This class is used to execute jobs.
    """

    @staticmethod
    def get_standard_parameters(environment: str, dbutils) -> dict:
        """Takes in dbutils and returns populated parameters dictionary

        Tries to parse virtual environment name for project name
        If virtual environment name does not have _ then the system
        looks at the current folder path to project name
        If the system can't use the environment or folder path then
        the system default to ddt_ops_dev

        Args:
            environment: Environment - if None then is extracted from directory or virtual environment
            dbutils (_type_): Databricks dbutils object

        Returns:
            dict: populated parameters dictionary
        """


        path = Path(os.getcwd())
        virtual_env = os.path.basename(os.path.normpath(sys.prefix))

        if len(virtual_env.rsplit('_', 1)) == 1:
            if len(path.parts) > 2:
                project_id = os.path.basename(os.path.normpath(path))
                virtual_env = project_id + "_dev"
            else:
                virtual_env = 'ddt_ops_dev'
                project_id = "ddt_ops"

            if environment is None or environment == "":
                environment = "dev"
        else:
            virtual_env = virtual_env.lower()
            project_id = virtual_env.rsplit('_', 1)[0]
            if environment is None or environment == "":
                environment = virtual_env.rsplit('_', 1)[1]

        project_id_root = project_id.split('_', 1)[0]
        project_id_individual = project_id.split('_', 1)[1]

        print("virtual_env: " + virtual_env)

        if dbutils is None:
            running_local = True
            repository_path = str(path.parent.parent)
            yyyy_param = str(date.today().year)
            mm_param = f"{format(date.today().month,'02')}"
            dd_param = ""
        else:
            report_yyyy_values = ["2021", "2022", str(date.today().year)]
            report_yyyy = str(date.today().year)
            report_mm_values = ["01", "02", "03", "04", "05", "06", "07", "08",
                                "09", "10", "11", "12"]
            report_mm = f"{format(date.today().month,'02')}"
            report_dd_values = ["NA", "01", "02", "03", "04", "05", "06", "07",
                                "08", "09", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20", "21", "22",
                                "23", "24", "25", "26", "27", "28", "29",
                                "30", "31"]
            report_dd = "NA"

            widgets = dbutils.widgets
            if widgets is not None:
                widgets.dropdown("report_yyyy", report_yyyy, report_yyyy_values)
                widgets.dropdown("report_mm", report_mm, report_mm_values)
                widgets.dropdown("report_dd", report_dd, report_dd_values)

            running_local = False
            repository_path = str(path.parent.parent)
            yyyy_param = dbutils.widgets.get("report_yyyy")
            if yyyy_param is None:
                yyyy_param = str(date.today().year)

            mm_param = dbutils.widgets.get("report_mm")
            if mm_param is None:
                mm_param = f"{format(date.today().month,'02')}"

            dd_param = dbutils.widgets.get("report_dd")
            if dd_param is None:
                dd_param = f"{format(date.today().day,'02')}"

        azure_client_secret_key = "DAVT_" + virtual_env.upper() + "_AZURE_CLIENT_SECRET"
        project_id_root = project_id.rsplit('_', 1)[0]
        project_id_individual = project_id.rsplit('_', 1)[1]

        dataset_name = 'all'
        cicd_action = 'pull_request'

        parameters = {
            "environment": environment,
            "project_id_root": project_id_root,
            "project_id_individual": project_id_individual,
            "project_id": project_id,
            "yyyy": yyyy_param,
            "mm": mm_param,
            "dd": dd_param,
            "repository_path": repository_path,
            "dataset_name": dataset_name,
            "cicd_action": cicd_action,
            "running_local": running_local,
            "azure_client_secret_key": azure_client_secret_key
        }

        return parameters
