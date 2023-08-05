from typing import List, Any, Dict, Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from fastapi import HTTPException
import re
from xclientai.dtypes.shared import Status, Credentials, Instance
    
   
class ModelSpecs(BaseModel):
    model_path: str


class Batcher(BaseModel):
    max_batch_size: Optional[int]
    # Max latency in milliseconds
    max_lantecy: Optional[int] 
    timeout: Optional[int]


class Scaling(BaseModel):
    min: Optional[int] = 1
    max: Optional[int] = 1
    scale_metric: Optional[str]
    target_scaling_value: Optional[Any]
    
    
class DeploymentSpecs(BaseModel):
    image: Optional[str]
    batcher: Optional[Batcher]
    scaling: Optional[Scaling]
    
    
class Inference(BaseModel):
    base_endpoint: Optional[str]
    is_ready_endpoint: Optional[str]
    infer_endpoint: Optional[str]
    

class Deployment(BaseModel):
    deployment_name: str
    status: Status = Status.NOT_STARTED
    error: Optional[str]
    model_specs: ModelSpecs
    deployment_specs: Optional[DeploymentSpecs]
    inference: Optional[Inference]
    credentials: Credentials
    logs: Optional[str]
    started: Optional[int]
    ended: Optional[int]
    instance: Optional[Instance] = Instance.G4DN_XLARGE
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
    @validator("deployment_name")
    def validate_deployment_name(cls, v):
        regex = "^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$"
        
        assert len(v) <= 30, "The deployment name cannot be longuer than 30 characters. Currently {}".format(len(v))
        
        assert bool(re.match(regex, v)), "The deployment_name must consist of lower case alphanumeric characters. Regex used for validation is '^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'"
        
        return v   
