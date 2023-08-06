""" Module for spark and os environment for developer_service with minimal dependencies. """

import os

# library management
from importlib import util  # library management

# error handling
from subprocess import check_output, Popen, PIPE, CalledProcessError
import subprocess

#  data
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

class EnvironmentCore:
    """ EnvironmentCore class with minimal dependencies for the developer service.
    - This class is used to configure the python environment.
    - This class also provides a broad set of generic utility functions.
    """

    @classmethod
    def print_version(cls) -> str:
        """ Prints version of library

        Returns:
            str: version of library
        """

        print_version_command = ["poetry", "version"]
        print_version_command_string = ' '.join(print_version_command)
        print(print_version_command_string)
        current_working_dir = os. getcwd()
        print_version_result = f"current_working_dir:{current_working_dir}"
        try:
            print_version_result = check_output(print_version_command)
            # print_version_result = cls.execute(print_version_command)
            print_version_result = f"{str(print_version_result)}:{print_version_command_string} succeeded"
        except subprocess.CalledProcessError as ex_called_process:
            error_string = ex_called_process.output
            print_version_result = str(print_version_result)
            if error_string is None:
                new_error_string = f": {print_version_command_string} succeeded with Exception"
                print_version_result = print_version_result + new_error_string

            else:
                print_version_result = print_version_result + f"Error: {error_string}"

        print_version_result = str(print_version_result)
        print(print_version_result)
        return print_version_result
