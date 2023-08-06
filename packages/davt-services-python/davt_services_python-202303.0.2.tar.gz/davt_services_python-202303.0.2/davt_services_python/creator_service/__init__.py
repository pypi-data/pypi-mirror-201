"""Initialize the it_admin_service subpackage of davt_services_python package"""
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

from . import dataset_metadata
from . import environment_metadata
from . import job_metadata
from . import logging_metadata
from . import pipeline_metadata

__all__ = ['dataset_metadata', 'environment_metadata', 'job_metadata', 'logging_metadata', 'pipeline_metadata']
