from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv, find_dotenv

# IMPORTANT: dont import logger here (circular import)

env_path = find_dotenv()
load_dotenv(env_path)


class Config:
    ACCELERATION_BASE_URL_X_BACKEND = os.environ.get(
        "ACCELERATION_BASE_URL_X_BACKEND", 
        "https://xcloud-api.stochastic.ai/backend"
    )
    EXECUTION_BASE_URL_X_BACKEND = os.environ.get(
        "EXECUTION_BASE_URL_X_BACKEND", 
        "https://xcloud-api.stochastic.ai/executor/backend"
    )
    DEPLOYMENTS_BASE_URL_X_BACKEND = os.environ.get(
        "DEPLOYMENTS_BASE_URL_X_BACKEND", 
        "https://xcloud-api.stochastic.ai/xinference/backend"
    )
    PANEL_DOMAIN = "https://xcloud.stochastic.ai"