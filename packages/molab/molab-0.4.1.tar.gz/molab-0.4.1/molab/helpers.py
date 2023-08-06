import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time
from morpheuscypher import Cypher
import sys
import os

def _get_instance_ids_from_names(url,headers,names:list):
    """
    The _get_instance_ids_from_names function accepts a list of names and returns a list of instance IDs.
    It does this by making an API call to the AS API for each name in the provided list, and then returning
    the ID from that response.
    
    :param url: Specify the url of the instance
    :param headers: Pass the api key to the _get_instance_ids_from_names function
    :param names:list: Pass a list of names to the _get_instance_ids_from_names function
    :return: A list of instance ids based on a list of names
    :doc-author: Trelent
    """
    session = FuturesSession()
    endpoint = "/api/instances"
    ids = []
    futures=[session.get(f'{url}{endpoint}?name={n}',headers=headers,verify=False) for n in names]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            i = resp.json()["instances"][0]
            ids.append(i["id"])
    return(ids)

def _get_morpheus_license_from_cypher(url,token,cypher_name):
    """
    The _get_morpheus_license_from_cypher function is a helper function that retrieves the Morpheus License from the Cypher
    database.  It accepts three parameters: url, token, and cypher_name.  The url parameter is required for making an API call to
    the Morpheus service.  The token parameter is required for making an API call to the Morpheus service.  The cypher_name
    parameter specifies which Cypher query will be used in order to retrieve license information from the database.
    
    :param url: Specify the morpheus api url
    :param token: Authenticate the user to morpheus
    :param cypher_name: Specify which cypher query to run
    :return: The license information from the morpheus api
    :doc-author: Trelent
    """
    logger.info(f'Begin get_morpheus_license_from_cypher')
    c = Cypher(url=url,token=token,ssl_verify=False)
    out = c.get(cypher_name)
    return(out)

def _get_code_repo_id_by_integration_name(url,headers,integration_name):
    # TODO: Run trelent
    _validate_url(url)
    logger.info(f'Searching for an integration by the name of: {integration_name}')
    e1 = "/api/integrations"
    e2 = "/api/options/codeRepositories"
    try:
        resp = requests.get(f'{url}{e1}?name={integration_name}',headers=headers, verify = False)
        if "200" in str(resp):
            i = resp.json()["integrations"]
            logger.info("Checking the count of integrations with that name")
            if len(i) > 1:
                logger.error('There is more than one integration with that name. Not sure what to do. Exiting...')
                return
            if len(i) < 1:
                logger.info(f'There is no integration by the name: {integration_name}')
                return(0)
            if i[0]["type"] != "git":
                logger.error(f'This is not a git based integration. No code repo to find')
                return
            logger.info(f'Collecting the name of the code repository')
            cr = i[0]["url"].split("/")[-1]
            integration_id = i[0]["id"]
            try:
                logger.info(f'Attempting to make the API call for: {url}{e2}?name={cr} - {integration_name}')
                resp = requests.get(f'{url}{e2}?phrase={cr}',headers=headers)
                if "200" in str(resp):
                    logger.info("Success!")
                    i = resp.json()["data"]
                    if len(i) > 1:
                        logger.info('Found more than one code repo this url...thinking....')
                        for r in i:
                            if integration_name in r:
                                data = r["value"]
                    code_repo_id = i[0]["value"] 
                else:
                    data = resp
            except Exception as e:
                logger.error(f'Encountered an error: {e}')
                return
    except Exception as e:
        logger.error(f'Encountered an error: {e}')
        return
    integration_info = {
            "integration_id": integration_id,
            "linked_code_repo_id": code_repo_id
            }
    return(integration_info)

def _add_git_integration_pat_auth(url,headers,integration_name,git_url,git_branch,git_username,git_pat):
    logger.info("Begin attempt to add git integration")
    _validate_url(url)
    endpoint = "/api/integrations"
    check = _get_code_repo_id_by_integration_name(url,headers,integration_name)
    if check:
        logger.info(f'A repo with the name {integration_name} already exists')
        return(check)
    logger.info(f'Personal access token selected as the auth method for the git repo')
    f = pkgutil.get_data(__name__, "template_files/git_auth_type_pat.json")
    jbody = json.loads(f)
    jbody["integration"]["name"] = integration_name
    jbody["integration"]["serviceUrl"] = git_url
    jbody["integration"]["config"]["defaultBranch"] = git_branch
    jbody["integration"]["serviceUsername"] = git_username
    jbody["integration"]["servicePassword"] = git_pat
    jbody["integration"]["serviceToken"] = git_pat
    body = json.dumps(jbody)
    try:
        logger.info(f'Attempting to create the Git integration')
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
        data = resp.json()
    except Exception as e:
        logger.error(e)
        return
    if data["success"]:
        logger.info(f'Successfully add GIT integration at id: {data["integration"]["id"]}')
        logger.info(f'Pausing to allow code sync')
        time.sleep(10)
        logger.info(f'Acquiring linked code repo id...')
        code_repo_id = _get_code_repo_id_by_integration_name(url,headers,integration_name)
        logger.info(f'Acquired the code repo id: {code_repo_id}')
        integration_info = {
            "integration_id": data["integration"]["id"],
            "linked_code_repo_id": code_repo_id
            }
        return(integration_info)
    else:
        logger.error(f'Something went wrong')
        logger.error(resp.text)
        return(resp.text)

def _get_option_list_id_by_name(url,headers,name):
    logger.info(f'Begin attempt to check for existing option list: {name}')
    endpoint = "/api/library/option-type-lists"
    resource_type = "optionTypeLists"
    try:
        resp = requests.get(f'{url}{endpoint}?name={name}', headers=headers, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        logger.info(f'API call successful. Parsing results....')
        resp = resp.json()
        if len(resp[resource_type]) == 1:
            logger.info(f'Found one {resource_type} with name {name} at id: {resp[resource_type][0]["id"]}')
            logger.info(f'Returning ID')
            return(resp[resource_type][0]["id"])
        if len(resp[resource_type]) == 0:
            logger.info(f'No {resource_type} by the name found')
            return 0
        if len(resp[resource_type]) > 1:
            logger.info(f'More than one {resource_type} by that name exists...not sure what to do.')
            exit(0)

def _add_manual_option_list(url,headers,name):
    # TODO: Set this up for multiple lists or manual input of initial dataset
    logger.info(f'Attempting to create the manual option list {name}')
    endpoint = "/api/library/option-type-lists"
    resource_type = "optionTypeList"
    check = _get_option_list_id_by_name(url,headers,name)
    if check:
        logger.info(f'A {resource_type} with the name {name} already exists')
        logger.info(f'Returning the ID')
        return(check)
    file_template = f'template_files/manual_option_list_{name.replace(" ","_").lower()}.json'
    logger.info(f'Attempting to load file template: {file_template}')
    f = pkgutil.get_data(__name__, file_template)
    ds = f.decode('utf-8')
    jbody = {
        "optionTypeList": {
            "name": name,
            "type": "manual",
            "visibility": "private",
            "initialDataset": ds
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}',headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created the {resource_type} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return(data[resource_type]["id"])

def _get_input_id_by_name(url,headers,input_name):
    logger.info(f'Checking for input with name: {input_name}')
    endpoint = "/api/library/option-types"
    resource_type = "optionTypes"
    try:
        resp = requests.get(f'{url}{endpoint}?name={input_name}', headers=headers, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        logger.info(f'API call successful. Parsing results....')
        resp = resp.json()
        if len(resp[resource_type]) == 1:
            logger.info(f'Found one {resource_type} input with name {input_name} at id: {resp[resource_type][0]["id"]}')
            logger.info(f'Returning ID')
            return(resp[resource_type][0]["id"])
        if len(resp[resource_type]) == 0:
            logger.info(f'No {resource_type} by the name found')
            return 0
        if len(resp[resource_type]) > 1:
            logger.info(f'More than one {resource_type} by that name exists...not sure what to do.')
            exit(0)

def _add_input(url,headers,input_name, field_name, input_type, field_label, required):
    logger.info(f'Begin attempt to add input: {input_name}')
    endpoint = "/api/library/option-types"
    resource_type = "optionType"
    check = _get_input_id_by_name(url,headers,input_name)
    if check:
      logger.info(f'Found one {resource_type} by that name. Using it\'s id')
      return check
    jbody = {
      "optionType": {
        "name": input_name,
        "fieldName": field_name,
        "type": input_type,
        "fieldLabel": field_label,
        "required": required,
        "exportMeta": False
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created {resource_type} {input_name} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return data[resource_type]["id"]

def _add_select_input(url, headers, input_name, field_name, option_list_id, field_label, required):
    logger.info(f'Begin attempt to add input: {input_name}')
    endpoint = "/api/library/option-types"
    resource_type = "optionType"
    check = _get_input_id_by_name(url,headers,input_name)
    if check:
      logger.info(f'Found one {resource_type} by that name. Using it\'s id')
      return check
    jbody = {
      "optionType": {
        "name": input_name,
        "fieldName": field_name,
        "type": "select",
        "optionList": {
          "id": option_list_id
        },
        "fieldLabel": field_label,
        "required": required,
        "exportMeta": False
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created {resource_type} {input_name} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return data[resource_type]["id"]

def _get_task_id_by_name(url,headers,name):
    logger.info(f'Begin attempt to get task id by name')
    endpoint = "/api/tasks"
    resource_type = "tasks"
    try:
        resp = requests.get(f'{url}{endpoint}?name={name}',headers=headers,verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        logger.info(f'API call successful. Parsing results...')
        resp = resp.json()
        if len(resp[resource_type]) == 1:
            logger.info(f'Found one {resource_type} with name {name} at id: {resp[resource_type][0]["id"]}')
            logger.info(f'Returning ID')
            return(resp[resource_type][0]["id"])
        if len(resp[resource_type]) == 0:
            logger.info(f'No {resource_type} by the name {name} found')
            return 0
        if len(resp[resource_type]) > 1:
            logger.info(f'More than one {resource_type} by that name exists...not sure what to do.')
            exit(0)


def _add_python_task(url,headers,name, code, task_type_id, script_code, result_type, source_type, repo_id, content_path, pythonargs, packages):
    logger.info(f'Begin attempt to create python task')
    endpoint = "/api/tasks"
    resource_type = "task"
    check = _get_task_id_by_name(url,headers,name)
    if check:
      logger.info(f'Found one {resource_type} by that name. Using it\'s id')
      return check
    jbody = {
      "task": {
        "name": name,
        "code": code,
        "taskType": {
          "id": task_type_id,
          "code": script_code
        },
        "resultType": result_type,
        "file": {
          "sourceType": source_type,
          "repository": {
            "id": repo_id
          },
          "contentPath": content_path,
          "contentRef": "master"
        },
        "taskOptions": {
          "pythonArgs": pythonargs,
          "pythonAdditionalPackages": packages
        },
        "executeTarget": "local",
        "retryable": False,
        "allowCustomConfig": False
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created {resource_type} {name} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return data[resource_type]["id"]

def _get_workflow_id_by_name(url,headers,name):
    logger.info(f'Begin attempt to get workflow by name')
    endpoint = "/api/task-sets"
    resource_type = "taskSets"
    try:
        resp = requests.get(f'{url}{endpoint}?name={name}',headers=headers,verify=False)
    except Exception as e:
        logger.error(e)
    if "200" in str(resp):
        logger.info(f'API call successful. Parsing results...')
        resp = resp.json()
        if len(resp["taskSets"]) == 1:
            logger.info(f'Found one {resource_type} with name {name} at id: {resp[resource_type][0]["id"]}')
            logger.info(f'Returning ID')
            return(resp[resource_type][0]["id"])
        if len(resp[resource_type]) == 0:
            logger.info(f'No {resource_type} by the name found')
            return 0
        if len(resp[resource_type]) > 1:
            logger.info(f'More than one {resource_type} by that name exists...not sure what to do.')
            exit(0)

def _add_operational_workflow(url,headers,name, taskid, inputs):
    # TODO: Get multiple tasks working
    logger.info(f'Begin attempt to create workflow')
    endpoint = "/api/task-sets"
    resource_type = "taskSet"
    check = _get_workflow_id_by_name(url,headers,name)
    if check:
      logger.info(f'Found one {resource_type} by that name. Using it\'s id')
      return check
    jbody = {
      "taskSet": {
        "name": name,
        "type": "operation",
        "tasks": [
          {
            "taskId": taskid,
            "taskPhase": "operation"
          }
        ],
        "optionTypes": inputs
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created {resource_type} {name} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return data[resource_type]["id"]

def _get_catalog_id_by_name(url,headers,name):
    logger.info(f'Begin attempt to get catalog item by name')
    endpoint = "/api/catalog-item-types"
    resource_type = "catalogItemTypes"
    try:
        resp = requests.get(f'{url}{endpoint}?name={name}',headers=headers,verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        logger.info(f'API call successful. Parsing results...')
        resp = resp.json()
        if len(resp[resource_type]) == 1:
            logger.info(f'Found one {resource_type} with name {name} at id: {resp[resource_type][0]["id"]}')
            logger.info(f'Returning ID')
            return(resp[resource_type][0]["id"])
        if len(resp[resource_type]) == 0:
            logger.info(f'No {resource_type} by the name found')
            return 0
        if len(resp[resource_type]) > 1:
            logger.info(f'More than one {resource_type} by that name exists...not sure what to do.')
            exit(0)

def _add_workflow_catalog_item(url,headers,name, workflow_id):
    logger.info(f'Begin attempt to create catalog item')
    endpoint = "/api/catalog-item-types"
    resource_type = "catalogItemType"
    check = _get_catalog_id_by_name(url,headers,name)
    if check:
      logger.info(f'Found one {resource_type} by that name. Using it\'s id')
      return check
    jbody = {
      "catalogItemType": {
           "type": "workflow",
           "enabled": True,
           "featured": False,
           "workflow": {
                "id": workflow_id
           },
           "name": name,
           "context": "appliance"
      }
    }
    body = json.dumps(jbody)
    try:
        resp = requests.post(f'{url}{endpoint}', headers=headers, data=body, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        data = resp.json()
        logger.info(f'Successfully created {resource_type} {name} at ID: {data[resource_type]["id"]}')
        logger.info(f'Returning {resource_type} ID')
        return data[resource_type]["id"]

def _add_catalog_logo(url,headers,catalog_id, image):
    logger.info(f'Begin attempt to add logo to catalog item')
    endpoint = "/api/catalog-item-types"
    module = pkgutil.get_loader('molab')
    module_path = module.path.rsplit('/',1)[0]
    path  = f'{module_path}/template_files/{image}'
    logger.info(f'Attempting to open file at path: {path}')
    files = {'catalogItemType.logo': open(path, "rb")}
    newheaders = {
        "Authorization": headers["Authorization"],
    }
    try:
        resp = requests.put(f'{url}{endpoint}/{catalog_id}',headers=newheaders, files=files, verify=False)
    except Exception as e:
        logger.error(e)
        return
    if "200" in str(resp):
        logger.info(f'Successfully uploaded logo')
        return(resp.json())
    else:
        logger.info(f'I don\'t think it worked captain')
        return(resp.text)

def _validate_url(url):
    logger.info('Ensuring https in url')
    if "https://" not in url:
        url = f'https://{url}'
    return(url)

def sleep(time):
    """
    The sleep function is used to pause the program for a specified amount of time.
    It can be useful when waiting for an external service to respond, or when polling
    a database.
    
    :param time: Specify how long the function should sleep for
    :return: None
    :doc-author: Trelent
    """
    logger.info(f'Sleeping for {time}')
    time.sleep(time)