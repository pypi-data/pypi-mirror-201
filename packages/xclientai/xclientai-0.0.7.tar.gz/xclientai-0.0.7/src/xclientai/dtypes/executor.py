from typing import Dict, List, Optional, Union
from pydantic import BaseModel, validator
import re
from xclientai.dtypes.shared import Status, Credentials, Instance


class ContainerExecutionSpecs(BaseModel):
    image: str
    command: Optional[List[str]] = ["/bin/sh", "-c"]
    args: Optional[List[str]]
    env: Optional[Dict[str, str]]
    s3_code_dir: str

class PythonExecutionSpecs(BaseModel):
    requirements_file: Optional[str]
    main_py_file: str
    py_version: Optional[str] = "3.8"
    image: Optional[str]
    command: Optional[List[str]] = ["/bin/sh", "-c"]
    args: Optional[List[str]]
    env: Optional[Dict[str, str]]
    s3_code_dir: str
    
    @validator("py_version")
    def validate_py_version(cls, v):
        valid_py_versions = ["3.8"]
        
        if v is not None:
            assert v in valid_py_versions, "This Python version is not supported: {}. Supported Python versions: {}".format(v, valid_py_versions)
            
        return v
            
    @validator("image")
    def validate_image(cls, v, values):
        if values["py_version"] is not None:
            v = "python:3.8-slim-buster"
        else:
            raise ValueError("py_version cannot be None")
            
        return v    
    
    @validator("args")
    def validate_args(cls, v, values):
        if values["requirements_file"] is None:
            v = ["python {}".format(values["main_py_file"])]
        else:
            v = ["pip install -r {} ; python {}".format(
                values["requirements_file"],
                values["main_py_file"]
            )]
            
        return v
    
    class Config:
        validate_all = True
    
class ExecutionJob(BaseModel):
    job_name: str
    status: Status = Status.NOT_STARTED
    error: Optional[str]
    execution_spec: Union[ContainerExecutionSpecs, PythonExecutionSpecs]
    credentials: Credentials
    logs: Optional[List[str]]
    started: Optional[int]
    ended: Optional[int]
    instance: Optional[Instance] = Instance.G4DN_XLARGE
    num_instances: Optional[int] = 1
    
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
    @validator("job_name")
    def validate_job_name(cls, v):
        regex = "^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$"
        
        assert len(v) <= 30, "The job name cannot be longuer than 30 characters. Currently {}".format(len(v))
        
        assert bool(re.match(regex, v)), "The job_name must consist of lower case alphanumeric characters. Regex used for validation is '^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'"
        
        return v  
    
    
    @validator("execution_spec")
    def validate_execution_spec(cls, v):
        if isinstance(v, PythonExecutionSpecs):
            v = ContainerExecutionSpecs(
                s3_code_dir=v.s3_code_dir,
                image=v.image,
                command=v.command,
                args=v.args,
                env=v.env
            )
            
        return v
    
    class Config:
        validate_all = True 
