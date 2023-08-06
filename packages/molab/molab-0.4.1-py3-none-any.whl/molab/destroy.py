import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_instance_existence(url,headers,ids):
    """
    The check_instance_existence function takes in a URL, headers and a list of instance IDs. It then checks to see if the instances exist on the server by making an API call for each ID in the list. If it does exist, it will add that instance ID to a new list called instances which is returned at the end of this function.
    
    :param url: Specify the url of the server
    :param headers: Pass the api key to the function
    :param ids: Pass in the ids of the instances that are to be checked
    :return: A list of instances that exist in the instance_ids list
    :doc-author: Trelent
    """
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.get(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            instance = resp.json()
            id = instance["instance"]["id"]
            instances.append(id)
    return(instances)

def unlock_instances(url,headers,ids:list):
    """
    The unlock_instances function will unlock the instances passed to it.
    It takes three arguments:
    url - The URL of the server you want to unlock instances on.
    headers - A dictionary of headers that contains your API key and a content type header for ReST requests. 
    ids - A list of instance IDs that you want to unlock.
    
    :param url: Specify the url of the instance
    :param headers: Pass the api key to the request
    :param ids:list: Pass a list of instance ids to the unlock_instances function
    :return: A list of instances that were unlocked
    :doc-author: Trelent
    """
    logger.info(f'Attempting to unlock instances: {ids}')
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.put(f'{url}{endpoint}{i}/unlock', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            for k in resp["results"].keys():
                logger.info(f'Instance {k} unlocked')
                instances.append(k)
    return(instances)

def delete_instances(url,headers,ids:list):
    """
    The delete_instances function accepts a list of instance IDs and deletes them from the ASM UI.
    It returns a dictionary with two keys: success and error. If success is True, then all instances were deleted successfully.
    If it is False, then one or more instances failed to delete.
    
    :param url: Specify the url of the instance
    :param headers: Pass the api key to the function
    :param ids:list: Pass a list of ids to the delete_instances function
    :return: A list of dicts that contain the instance id and whether or not deletion was successful
    :doc-author: Trelent
    """
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.delete(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            logger.info(f'Successfully initiated teardowm of instance')
        return(resp)

def delete_classroom_labs(url,headers,master_instance_id,tag_name):
    """
    The delete_classroom_labs function deletes all the instances that are tagged with a specific tag name.
    The function first gets the tags of the master instance and then loops through each tag to find one that matches
    the specified tag name. Once it finds a match, it parses out all of the instance ids from that particular tag and 
    then calls unlock_instances() to unlock those instances before calling delete_instances() to delete them.
    
    :param url: Specify the url of the instance
    :param headers: Pass the authentication token to the api calls
    :param master_instance_id: Identify the master instance
    :param tag_name: Find the tag that contains the instance ids
    :return: Nothing
    :doc-author: Trelent
    """
    endpoint = "/api/instances"
    tags = requests.get(f'{url}{endpoint}/{master_instance_id}',headers=headers, verify=False).json()["instance"]["tags"]
    for t in tags:
        if tag_name in t["name"]:
            logger.info(f'Found the defined tag.')
            ids = t["value"]
            ids = json.loads(ids)
            logger.info(f'Unlocking the instances.')    
            unlock_instances(url,headers,ids)
            logger.info(f'Deleting the instances')
            delete_instances(url,headers,ids)
            return()
        
