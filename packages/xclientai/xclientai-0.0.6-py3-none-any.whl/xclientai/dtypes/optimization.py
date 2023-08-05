from typing import List, Any, Dict, Optional
from pydantic import BaseModel, validator
import numpy as np
import re
from xclientai.dtypes.shared import Status, Credentials
from xclientai.utils.logging import configure_logger
from xclientai.config import Config
from urllib.parse import urlparse


logger = configure_logger(__name__)

    
class Signature(BaseModel):
    name: str
    shape: List[int]
    data: Optional[Any]
    datatype: str
    
    @validator("name")
    def name_is_valid(cls, v):
        assert isinstance(v, str), "Name property should be a string"        
        return v

    @validator("datatype")
    def datatype_is_valid(cls, v):
        valid_datatypes = [
            "int8",
            "int16",
            "int32",
            "int64",
            "fp16",
            "fp32",
            "fp64"
        ]

        assert v in valid_datatypes, f"datatype {v} is not valid. Use one of these: {valid_datatypes}"

        return v
    
    @validator("shape")
    def validate_shape(cls, v):
        return v

    @validator("data")
    def data_match_with_shape(cls, v, values, **kwargs):
        if v is not None:
            data_shape = list(np.array(v).shape)
            given_shape = values["shape"]

            assert len(data_shape) == len(given_shape), f"The data and the shape on the given input or output does not match: {values}"

            for given_dim, data_dim in zip(given_shape, data_shape):
                if given_dim != data_dim:
                    assert given_dim == -1, f"The data and the shape on the given input or output does not match: {values}"

        return v
    
    class Config:
        validate_all = True


class BenchmarkConfig(BaseModel):
    name: str
    dim: int
    resize_values: List[int]


class BenchmarkResults(BaseModel):
    baseline_model: Optional[List[Dict]]
    accelerated_model: Optional[List[Dict]]


class Accelerator(BaseModel):
    type: Optional[str]
    precision: Optional[str]
    
    @validator("type")
    def validate_accelerator_type(cls, v):
        valid_types = ["tensorrt"]
        
        assert v in valid_types, "{} is not a valid accelerator. Valid accelerators: {}".format(v, valid_types)
        
        return v
    
    @validator("precision")
    def validate_accelerator_precision(cls, v): 
        v = str(v) 
        valid_precisions = ["32", "16"]
        
        assert v in valid_precisions, "{} is not a valid accelerator precision. Valid accelerator precisions: {}".format(v, valid_precisions)
        
        return v

 
class BenchmarkInfo(BaseModel):
    benchmark_config: List[BenchmarkConfig]
    warmup: int = 3
    repeat: int = 3
    hardware: str = "gpu"
    accelerator: Optional[Accelerator]
    results: Optional[BenchmarkResults]
    
    @validator("hardware")
    def validate_hardware(cls, v):
        valid_hardware = ["cpu", "gpu"]
        assert v in valid_hardware, "{} is not a valid hardware. Valid hardwares: {}".format(v, valid_hardware)
        
        return v


class AccelerationInfo(BaseModel):
    input_model_path: str
    input_model_type: str
    output_model_path: str
    output_model_type: Optional[str]
    inputs: List[Signature]
    outputs: List[Signature]
    
    @validator("input_model_type")
    def validate_input_model_type(cls, v):
        valid_model_types = ["pt"]
        
        assert v in valid_model_types, "input_model_type should be one of the following values: {}".format(valid_model_types)
        
        return v


class Notification(BaseModel):
    headers: Optional[Dict]
    url: Optional[str]
    type: Optional[str]
    exclude_data_signature: bool = True
    
    @validator("url")
    def validate_url(cls, v):
        if v is not None:
            parsed_url_obj = urlparse(v)
            
            assert parsed_url_obj.scheme != '', "The URL should have the following format http://domain-name.com/path/. Don't forget the schema http or https"
        
        return v
    
    @validator("type")
    def validate_type(cls, v, values, **kwargs):
        valid_notification_methods = ["webhook"]
        assert v in valid_notification_methods, f"The valid notification methods are: {valid_notification_methods}"
        
        if v == "webhook":
            assert values.get("url") is not None, "If notification type is webhook, you should specify the field url with a string"
        
        return v


class NotificationResult(BaseModel):
    type: str
    message: str
    status_code: int


class AccelerationJob(BaseModel):
    job_name: str
    status: Status = Status.NOT_STARTED
    panel_url: Optional[str]
    error: Optional[str]
    notification_result: Optional[NotificationResult]
    credentials: Credentials
    acceleration: AccelerationInfo
    benchmark: BenchmarkInfo = None
    notification: Notification = None
    started: Optional[int]
    ended: Optional[int]
    
    @validator("panel_url")
    def validate_panel_url(cls, v, values: dict, **kwargs):
        if values["status"] == Status.SUCCESSFUL:
            v = "{}/jobs/{}".format(
                Config.PANEL_DOMAIN,
                values["job_name"]
            )
        
        return v     
        
    @validator("job_name")
    def validate_job_name(cls, v):
        regex = "^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$"
        
        assert len(v) < 30, "The job name cannot be longuer than 30 characters. Currently {}".format(len(v))
        
        assert bool(re.match(regex, v)), "The job_name must consist of lower case alphanumeric characters. Regex used for validation is '^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'"
        
        return v  
    
    @validator("benchmark")
    def validate_benchmark(cls, v: BenchmarkInfo, values: dict, **kwargs):
        n_dims = len(values["acceleration"].inputs[0].shape)
        
        for benchmark_config_item in v.benchmark_config:
            assert benchmark_config_item.dim < n_dims, "Benchmark dim cannot be greater than the number of dims in the input. Benchmark config: {}".format(benchmark_config_item)
            
        return v
    
    class Config:
        validate_all = True
