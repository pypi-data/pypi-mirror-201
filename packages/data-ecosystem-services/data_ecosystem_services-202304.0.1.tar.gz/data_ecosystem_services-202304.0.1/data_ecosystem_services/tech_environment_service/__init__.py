"""Initialize the tech_environment_service subpackage of pade_python package"""

# allow absolute import from the root folder
# whatever its name is.
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\tech_environment_service
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


import data_ecosystem_services.tech_environment_service.dataset_core
import data_ecosystem_services.tech_environment_service.dataset_crud
import data_ecosystem_services.tech_environment_service.environment_core
import data_ecosystem_services.tech_environment_service.environment_file
import data_ecosystem_services.tech_environment_service.environment_spark
import data_ecosystem_services.admin_service.environment_logging
import data_ecosystem_services.security_service.security_core
import data_ecosystem_services.tech_environment_service.repo_core
import data_ecosystem_services.tech_environment_service.job_core
