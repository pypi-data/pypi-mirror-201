from xclientai.utils.requests_utils import do_request
from xclientai.config import Config
from xclientai.dtypes.optimization import AccelerationJob
from typing import List

class AccelerationJobsClient:
    
    @classmethod
    def get_jobs(cls, exclude_data_signature: bool = True) -> List[AccelerationJob]:        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.ACCELERATION_BASE_URL_X_BACKEND
            ),
            http_method="get",
            params={
                "exclude_data_signature": exclude_data_signature
            }
        )
        
        list_job_dicts = response.json()["data"]
        jobs = []
        
        for job_dict in list_job_dicts:
            job = AccelerationJob.parse_obj(job_dict)
            jobs.append(job)
            
        return jobs
    
    @classmethod
    def get_job_by_name(cls, job_name: str, exclude_data_signature: bool = True) -> AccelerationJob:        
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.ACCELERATION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get",
            params={
                "exclude_data_signature": exclude_data_signature
            }
        )
        
        job_dict = response.json()["data"]
        job = AccelerationJob.parse_obj(job_dict)
        
        return job
    
    @classmethod
    def delete_job(cls, job_name: str, exclude_data_signature: bool = True) -> AccelerationJob:
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.ACCELERATION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="delete",
            params={
                "exclude_data_signature": exclude_data_signature
            }
        )
        
        job_dict = response.json()["data"]
        job = AccelerationJob.parse_obj(job_dict)
        return job
    
    @classmethod
    def create_job(cls, job: AccelerationJob, exclude_data_signature: bool = True) -> AccelerationJob:
        # Assert data in signature is not None
        for signature in job.acceleration.inputs + job.acceleration.outputs:
            assert signature.data is not None, "The data in signature cannot be None when creating a job"
        
        job_dict = job.dict()
        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.ACCELERATION_BASE_URL_X_BACKEND
            ),
            http_method="post",
            json_data=job_dict,
            params={
                "exclude_data_signature": exclude_data_signature
            }
        )
        
        returned_job_dict = response.json()["data"]
        returned_job = AccelerationJob.parse_obj(returned_job_dict)
        
        return returned_job
       