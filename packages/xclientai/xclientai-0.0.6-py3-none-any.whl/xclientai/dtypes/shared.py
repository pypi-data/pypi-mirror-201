from typing import List, Any, Dict, Optional
from pydantic import BaseModel, validator
import numpy as np
import re
from enum import Enum
from xclientai.utils.logging import configure_logger
from xclientai.config import Config
from urllib.parse import urlparse


logger = configure_logger(__name__)


class Instance(str, Enum):
    G4DN_XLARGE = "g4dn.xlarge"


class Status(str, Enum):
    SUCCESSFUL = "successful"
    FAILED = "failed"
    RUNNING = "running"
    NOT_STARTED = "not_started"
    CANCELLED = "cancelled"
    DEPLOYING = "deploying"
    
    
class Credentials(BaseModel):
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_region: Optional[str]
    cloud: str
    
    @validator("aws_access_key_id")
    def validate_aws_access_key_id(cls, v):
        return v
    
    @validator("aws_secret_access_key")
    def validate_aws_secret_access_key(cls, v):
        return v
    
    @validator("aws_region")
    def validate_aws_region(cls, v):
        return v
    
    @validator("cloud")
    def validate_cloud(cls, v, values, **kwargs):
        valid_clouds = ["aws", None]
        
        assert v in valid_clouds, f"Valid clouds are {valid_clouds}"
        
        if v == "aws":
            condition = "aws_access_key_id" in values and "aws_secret_access_key" in values and "aws_region" in values
            
            if not condition:
                logger.warning("AWS credentials have not been provided")
        
        return v