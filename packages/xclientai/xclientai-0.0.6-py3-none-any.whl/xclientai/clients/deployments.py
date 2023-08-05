from xclientai.utils.requests_utils import do_request
from xclientai.config import Config
from xclientai.dtypes.deployments import Deployment
from typing import List
import requests
from xclientai.dtypes.shared import Status
import time


class DeploymentsClient:
    
    @classmethod
    def get_deployments(cls) -> List[Deployment]:        
        response = do_request(
            url="{}/v1/deployments/".format(
                Config.DEPLOYMENTS_BASE_URL_X_BACKEND
            ),
            http_method="get"
        )
        
        list_deployment_dicts = response.json()["data"]
        deployments = []
        
        for deployment_dict in list_deployment_dicts:
            deployment = Deployment.parse_obj(deployment_dict)
            deployments.append(deployment)
            
        return deployments
    
    @classmethod
    def get_deployment_by_name(cls, deployment_name: str) -> Deployment:        
        response = do_request(
            url="{}/v1/deployments/{}".format(
                Config.DEPLOYMENTS_BASE_URL_X_BACKEND,
                deployment_name
            ),
            http_method="get"
        )
        
        deployment_dict = response.json()["data"]
        deployment = Deployment.parse_obj(deployment_dict)
        
        return deployment
    
    @classmethod
    def get_logs(cls, deployment_name: str) -> List[Deployment]:        
        response = do_request(
            url="{}/v1/deployments/{}/logs".format(
                Config.DEPLOYMENTS_BASE_URL_X_BACKEND,
                deployment_name
            ),
            http_method="get"
        )
        
        logs = response.json()["data"]
        
        return logs
    
    @classmethod
    def delete_deployment(cls, deployment_name: str) -> Deployment:
        response = do_request(
            url="{}/v1/deployments/{}".format(
                Config.DEPLOYMENTS_BASE_URL_X_BACKEND,
                deployment_name
            ),
            http_method="delete"
        )
        
        deployment_dict = response.json()["data"]
        deployment = Deployment.parse_obj(deployment_dict)
        return deployment
    
    @classmethod
    def create_deployment(cls, deployment: Deployment) -> Deployment:        
        deployment_dict = deployment.dict()
        
        response = do_request(
            url="{}/v1/deployments/".format(
                Config.DEPLOYMENTS_BASE_URL_X_BACKEND
            ),
            http_method="post",
            json_data=deployment_dict
        )
        
        returned_deployment_dict = response.json()["data"]
        returned_deployment = Deployment.parse_obj(returned_deployment_dict)
        
        return returned_deployment
       
    @classmethod
    def is_deployment_ready(cls, deployment_name: str):
        deployment = cls.get_deployment_by_name(deployment_name=deployment_name)
            
        if deployment.status == Status.RUNNING:
            response = requests.get(
                url=deployment.inference.is_ready_endpoint
            )
            
            if response.status_code == 200:
                is_deployment_ready = response.json().get("ready")
                
                if is_deployment_ready:
                    return True
                    
        return False
    
    @classmethod
    def wait_until_deployment_is_ready(cls, deployment_name: str, timeout=1000):
        sleep_time = 10
        total_time = 0
        while not cls.is_deployment_ready(deployment_name=deployment_name) and total_time < timeout:
            time.sleep(sleep_time)
            total_time += sleep_time