"""Initialize the developer_service subpackage of davt_services_python package"""

# allow absolute import from the root folder
# whatever its name is.
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\developer_service
OS_NAME = os.name

sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


import davt_services_python.developer_service.dataset_core
import davt_services_python.developer_service.dataset_crud
import davt_services_python.developer_service.environment_core
import davt_services_python.developer_service.environment_file
import davt_services_python.developer_service.environment_spark
import davt_services_python.developer_service.environment_logging
import davt_services_python.developer_service.security_core
import davt_services_python.developer_service.repo_core
import davt_services_python.developer_service.job_core
