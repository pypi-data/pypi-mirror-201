from xclientai.utils.requests_utils import do_request
from xclientai.config import Config
from xclientai.dtypes.executor import ExecutionJob
from typing import List


class ExecutionJobsClient:
    
    @classmethod
    def get_jobs(cls) -> List[ExecutionJob]:        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.EXECUTION_BASE_URL_X_BACKEND
            ),
            http_method="get"
        )
        
        list_job_dicts = response.json()["data"]
        jobs = []
        
        for job_dict in list_job_dicts:
            job = ExecutionJob.parse_obj(job_dict)
            jobs.append(job)
            
        return jobs
    
    @classmethod
    def get_job_by_name(cls, job_name: str) -> ExecutionJob:        
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get"
        )
        
        job_dict = response.json()["data"]
        job = ExecutionJob.parse_obj(job_dict)
        
        return job
    
    @classmethod
    def get_logs(cls, job_name: str) -> List[ExecutionJob]:        
        response = do_request(
            url="{}/v1/jobs/{}/logs".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get"
        )
        
        logs = response.json()["data"]
        
        if logs is not None:
            logs = [log for log in logs if log is not None]
            logs = "\n".join(logs)
        
        return logs
    
    @classmethod
    def delete_job(cls, job_name: str) -> ExecutionJob:
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="delete"
        )
        
        job_dict = response.json()["data"]
        job = ExecutionJob.parse_obj(job_dict)
        return job
    
    @classmethod
    def create_job(cls, job: ExecutionJob) -> ExecutionJob:        
        job_dict = job.dict()
        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.EXECUTION_BASE_URL_X_BACKEND
            ),
            http_method="post",
            json_data=job_dict
        )
        
        returned_job_dict = response.json()["data"]
        returned_job = ExecutionJob.parse_obj(returned_job_dict)
        
        return returned_job
       