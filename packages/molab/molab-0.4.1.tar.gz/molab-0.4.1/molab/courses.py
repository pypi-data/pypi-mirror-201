import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
from .helpers import _add_git_integration_pat_auth, _validate_url, _add_manual_option_list, _add_input, _add_select_input, _add_python_task, _add_operational_workflow, _add_workflow_catalog_item, _add_catalog_logo


def configure_automation_class(node_ip,headers,**class_configs):
    logger.info(f'Begin attempt to setup Automation Class on node: {node_ip}')
    # Ensure URL is https
    url = _validate_url(node_ip)
    # Add the GIT integration
    integration = _add_git_integration_pat_auth(url,headers,class_configs["integration_name"],class_configs["git_url"],class_configs["git_branch"],class_configs["git_username"],class_configs["git_pat"])
    logger.info(f'Integration Data: {integration}')
    # Add the manual option list
    option_list_id = _add_manual_option_list(url,headers,class_configs["option_list_name"])
    logger.info(f'Option List ID: {option_list_id}')

    ## Create inputs
    input_ids = []
    input_ids.append(_add_input(node_ip,headers,"AMI - CentOS", "amicentos", "text", "AMI - CentOS", "True"))
    input_ids.append(_add_input(node_ip,headers,"AMI - Ubuntu", "amiubuntu", "text", "AMI - Ubuntu", "True"))
    input_ids.append(_add_input(node_ip,headers,"AWS Key", "awsKey", "text", "AWS Key", "True"))
    input_ids.append(_add_input(node_ip,headers,"AWS Secret", "awsSecret", "text", "AWS Secret", "True"))
    input_ids.append(_add_input(node_ip,headers,"AWS VPC", "awsVpc", "text", "AWS VPC", "True"))
    input_ids.append(_add_input(node_ip,headers,"Internal IP", "internalHost", "text", "Internal IP", "True"))
    input_ids.append(_add_select_input(node_ip,headers,"AWS Regions", "awsRegion", option_list_id, "AWS Region", "True"))

    ## Create "Set Up My Lab" Python Task
    task_id = _add_python_task(node_ip,headers,"Set Up My Lab", "setupMyLab", "12", "jythonTask", "value", "repository", integration["linked_code_repo_id"], "/setupmylab.py", "", "requests")

    ## Create "Set Up My Lab" Workflow
    workflow_id = _add_operational_workflow(node_ip,headers,"Set Up My Lab", task_id, input_ids)

    ## Create catalog item
    catalog_id = _add_workflow_catalog_item(node_ip,headers,"Set Up My Lab", workflow_id)

    ## Add logo
    logo = _add_catalog_logo(node_ip,headers,catalog_id, "MorpheusImage.png")