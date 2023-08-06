import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from loguru import logger
import requests
import pkgutil
import time
from .helpers import _get_morpheus_license_from_cypher

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_aio(node_ip,account_name,user_name,password,email,license):
    """
    The setup_aio function is used to configure a Morpheus Appliance.
    It will take the following parameters:
        node_ip - The IP address of the appliance you wish to configure.
        account_name - The name of the account you wish to create on this appliance. This should be all lowercase letters and numbers only, no special characters or spaces. 
        user_name - The username for this new account (should match your email address). This should be all lowercase letters and numbers only, no special characters or spaces.
     
    :param node_ip: Determine the ip address of the node to be configured
    :param account_name: Set the account name for the new user
    :param user_name: Set the admin user name
    :param password: Set the password for the first user created
    :param email: Set the email address for the admin user
    :param license: Pass in the license file
    :return: A string
    :doc-author: Trelent
    """
    logger.info(f'Begin attempt to set up Morpheus AIO')
    try:
        ping = ""
        timeout = 1
        while "MORPHEUS PING" not in ping:
            logger.info(f'Timeout count now at {timeout}')
            try:
                ping = _get_appliance_node_status(node_ip)
                if "Morpheus is Loading..." in ping:
                    logger.info(f'{ping} checking again in 60 seconds')
                    time.sleep(60)
                    timeout = timeout + 1
                elif "404" in str(ping):
                    logger.info(f'Encountered a 404. Assuming it is still initializing. Waiting 60 seconds to check again.')
                    time.sleep(60)
                    timeout = timeout + 1
                elif "Could not reach node:" in ping:
                    logger.info(f'Unable to reach the node. Assuming it is still initializing. Waiting 60 seconds to check again.')
                    time.sleep(60)
                    timeout = timeout + 1
                elif timeout >= 45:
                    return("Timout waiting for the system to come up")
            except Exception as e:
                logger.error(f'Unhandled exception occurred')
                return(e)
        try:
            logger.info(f'Attempting to configure with the follow configuration:')
            _apply_morpheus_setup_config(node_ip,account_name,user_name,password,email)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
        try:
            token = get_morpheus_api_token(node_ip,user_name,password)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
        try:
            _apply_morpheus_license(node_ip,token,license)
        except Exception as e:
            logger.error(f'Unhandled exception: {e}')
            return(e)
    except Exception as e:
        logger.error(f'Unhandled exception occurred: {e}')


def setup_three_node():
    pass

def _apply_morpheus_setup_config(node_ip,account_name,user_name,password,email):
    """
    The _apply_morpheus_setup_config function is used to configure the Morpheus Appliance. 
    It takes in a node_ip, account_name, user_name, password and email as arguments. It then performs a POST request to the /api/setup/init endpoint on that node using those credentials.
    
    :param node_ip: Specify the ip address of the node to configure
    :param account_name: Set the morpheus appliance name
    :param user_name: Specify the username that will be used to login to morpheus
    :param password: Set the password for the initial user account
    :param email: Provide a default email address to be used in the initial configuration of morpheus
    :return: The response from the api call
    :doc-author: Trelent
    """
    logger.info("Begin attempt to configure Morpheus")
    url = f'https://{node_ip}'
    endpoint = "/api/setup/init"
    headers={'Content-Type': 'application/json',"Accept":"application/json"}
    body={"applianceUrl": url, "applianceName": account_name, "accountName": account_name, "username": user_name, "password": password, "email": email, "firstName": user_name }
    try:
        logger.info(f'Attempting to perform first time setup on node {node_ip}')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=json.dumps(body))
    except Exception as e:
        logger.error(f'Something went wrong: {e}')
    if "200" in str(resp):
        logger.info(f'Initial configuration of Morpheus successful')
    else:
        logger.error(f'It appears something went wrong')
    return(resp)

def _get_appliance_node_status(node_ip):
    """
    The _get_appliance_node_status function is used to check if the Morpheus UI is up on a given node.
    It takes in a single argument, which is the IP address of the node you want to check. It returns either
    the string &quot;Morpheus UI Up&quot; or an error message.
    
    :param node_ip: Pass the ip address of the node to be checked
    :return: The response from the node
    :doc-author: Trelent
    """
    headers = {'Content-Type': 'application/json'}
    url = f'https://{node_ip}'
    endpoint = "/ping"
    try:
        logger.info(f'Checking for Morpheus UI to be up: {node_ip}')
        resp = requests.get(f'{url}{endpoint}',headers=headers,verify=False)
    except Exception as e:
        logger.error(f'Could not reach node: {node_ip}')
        return(f'Could not reach node: {node_ip}')
    if "MORPHEUS PING" in str(resp.text):
        out = resp.text
        logger.info(f'Looks like the Morpehus UI is up: {out}')
    elif "Morpheus is Loading..." in str(resp.text):
        out = "Morpheus is Loading..."
    else:
        out = resp
    return(out)

def get_morpheus_api_token(url,user_name,password):
    """
    The get_morpheus_api_token function is used to get a Morpheus API token.
    It takes three arguments: the URL of the Morpheus appliance, a username and password.
    The function returns an access_token which can be used in subsequent requests.
    
    :param url: Specify the morpheus api instance that is being used
    :param user_name: Specify the username of the user that is used to authenticate with the morpheus api
    :param password: Pass the password to get_morpheus_api_token function
    :return: A token for the user
    :doc-author: Trelent
    """
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/oauth/token?grant_type=password&scope=write&client_id=morph-api"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {"username": user_name, "password": password}
    try:
        logger.info(f'Attempting to get API token')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=body)
    except Exception as e:
        logger.info(f'Something went wrong')
    if "200" in str(resp):
        logger.info("Token acquired")
        token = resp.json()["access_token"]
        return(token)
    elif "400" in str(resp):
        logger.error('Bad credentials')
        return(resp)
    else:
        return(resp)
    
def _apply_morpheus_license(url,token,license):
    """
    The _apply_morpheus_license function is used to apply a license to the Morpheus instance.
    It takes three arguments: url, token, and license. The url argument is the URL of your Morpheus instance (e.g., https://morpheus-instance). 
    The token argument is an API key generated in the UI for that particular instance (e.g., 1234567890abcde1234567890abcde1234567890). 
    The license argument should be a string containing your desired morpheus license.
    
    :param url: Specify the morpheus instance
    :param token: Pass the token generated by the _get_token function
    :param license: Pass in the license key that you want to apply
    :return: A response object
    :doc-author: Trelent
    """
    headers={'Content-Type': 'application/json',"Accept":"application/json", "Authorization": "BEARER " + token}
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/api/license"
    body = {"license": license}
    try:
        logger.info(f'Attempting to apply the license')
        resp = requests.post(f'{url}{endpoint}',headers=headers,verify=False,data=json.dumps(body))
    except Exception as e:
        logger.error(f'Something went wrong')
    if "200" in str(resp):
        logger.info("License successfully applied")
        return(resp)
    elif "\"success\":false," in str(resp.text):
        logger.error(resp.json()["msg"])
    elif "\"error\":" in str(resp.text):
        logger.error(resp.json()["error_description"])
    return(resp)

def _get_morpheus_setup_status(url):
    """
    The _get_morpheus_setup_status function checks to see if the Morpheus platform is setup.
    It returns True if the platform is setup, and False otherwise.
    
    :param url: Specify the url of the node to check
    :return: A boolean value
    :doc-author: Trelent
    """
    """
    The _get_morpheus_setup_status function checks to see if the Morpheus platform is setup.
    It returns True if the platform is setup, and False otherwise.
    
    :param url: Specify the url of the node to check
    :return: A boolean value
    :doc-author: Trelent
    """
    # Returns True if the platform is setup. Otherwise returns False.
    if 'https://' not in url:
        url = f'https://{url}'
    endpoint = "/api/ping"
    headers = {'Content-Type': 'application/json'}
    try:
        logger.info(f'Checking the setup status of node: {url}')
        resp = requests.get(f'{url}{endpoint}',headers=headers, verify=False)
    except Exception as e:
        logger.error(f'Could not reach node: {url}')
    if "\'setupNeeded\': True," in resp:
        return(False)
    else:
        return(True)
    
def get_aio_external_ips(url,headers,ids:list):
    """
    The get_aio_external_ips function will return a list of IP addresses for all AIO nodes in the cluster.
    This function is used to determine which node should be used as the primary node for license assignment.
    
    :param url: Specify the url of the target cluster
    :param headers: Pass the api key to the get_aio_external_ips function
    :param ids:list: Pass in a list of ids to check for
    :return: The ip addresses of the aio nodes
    :doc-author: Trelent
    """
    session = FuturesSession()
    endpoint = "/api/instances"
    ips = []
    futures=[session.get(f'{url}{endpoint}/{i}',headers=headers,verify=False) for i in ids]
    logger.info(f'Checking for AIO nodes')
    for future in as_completed(futures):
        resp = future.result()
        if "404" in str(resp):
            logger.error(f'Returned 404')
            return(resp)  
        elif "400" in str(resp):
            logger.error(f'Returned 400')
            return(resp) 
        elif "200" in str(resp):
            for node in resp.json()["instance"]["containerDetails"]:
                if "single-node" in node["externalHostname"]:
                    logger.info(f'Found AIO node IP of : {node["ip"]}')
                    ips.append(node["ip"])
    return(ips)

def get_lab_info(url,headers,ids:list):
    """
    The get_lab_info function accepts a URL, headers and instance ids as arguments.
    It then makes an API call to the Morpheus API to get information about each instance in the lab.
    The function returns a list of lists containing all of the data for each instance.
    
    :param url: Specify the endpoint of the api
    :param headers: Pass the api key to the get_lab_info function
    :param ids:list: Pass in the list of instance ids to be parsed
    :return: A list of lists that can be used to create a table
    :doc-author: Trelent
    """
    session = FuturesSession()
    endpoint = "/api/instances"
    data = [['Lab Name','Region','AIO External IP','AIO Internal IP','AMI ID','Access Key','Secret Key']]
    futures=[session.get(f'{url}{endpoint}/{i}/state',headers=headers,verify=False) for i in ids]
    lb_endpoint = []
    rds_endpoint = []
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            # logger.info(f'Parsing instance state for instance id: {resp.json()["workloads"][0]["refId"]}')
            # logger.info(f'Parsing the terraform resources')
            instance_data = []
            lab_name = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "lab_name"]
            region = [i["value"] for i in resp.json()["input"]["variables"] if i["name"] == "region"]
            eip = [i["value"]["value"][0][0]["public_ip"] for i in resp.json()["output"]["outputs"] if i["name"] == "elastic_ips"]
            private_ip = [i["value"]["value"][0][0]["private_ip"] for i in resp.json()["output"]["outputs"] if i["name"] == "elastic_ips"]
            ami_id = [i["value"]["value"][0][0]["ami"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
            state_data = json.loads(resp.json()["stateData"])
            access_key = [i["values"]["id"] for i in state_data["values"]["root_module"]["child_modules"][0]["resources"] if i["type"] == "aws_iam_access_key"]
            secret_key = [i["values"]["secret"] for i in state_data["values"]["root_module"]["child_modules"][0]["resources"] if i["type"] == "aws_iam_access_key"]
            instance_data.extend([lab_name[0],region[0],eip[0],private_ip[0],ami_id[0],access_key[0],secret_key[0]])
            try: 
                lb_endpoint = [i["value"]["value"][0]["dns_name"] for i in resp.json()["output"]["outputs"] if i["name"] == "load_balancer"]
                data[0].append('LB Endpoint')
                instance_data.append(lb_endpoint[0])
            except:
                pass
            try:
                rds_endpoint = [i["value"]["value"][0][0]["endpoint"] for i in resp.json()["output"]["outputs"] if i["name"] == "rds"]
                data[0].append('RDS Endpoint')
                instance_data.append(rds_endpoint[0])
            except:
                pass
            try:
                instances = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
                app_nodes = instances[0][1]
                app_1_pub = [i["public_ip"] for i in app_nodes if "APP-01" in i["tags_all"]["Name"]]
                data[0].append('App-01 Public IP')
                instance_data.append(app_1_pub[0])
                app_1_priv = [i["private_ip"] for i in app_nodes if "APP-01" in i["tags_all"]["Name"]]
                data[0].append('App-01 Private IP')
                instance_data.append(app_1_priv[0])
                app_2_pub = [i["public_ip"] for i in app_nodes if "APP-02" in i["tags_all"]["Name"]]
                data[0].append('App-02 Public IP')
                instance_data.append(app_2_pub[0])
                app_2_priv = [i["private_ip"] for i in app_nodes if "APP-02" in i["tags_all"]["Name"]]
                data[0].append('App-02 Private IP')
                instance_data.append(app_2_priv[0])
                app_3_pub = [i["public_ip"] for i in app_nodes if "APP-03" in i["tags_all"]["Name"]]
                data[0].append('App-03 Public IP')
                instance_data.append(app_3_pub[0])
                app_3_priv = [i["private_ip"] for i in app_nodes if "APP-03" in i["tags_all"]["Name"]]
                data[0].append('App-03 Private IP')
                instance_data.append(app_3_priv[0])
            except:
                pass
            try:
                instances = [i["value"]["value"] for i in resp.json()["output"]["outputs"] if i["name"] == "instances"]
                perc_nodes = instances[0][2]
                perc_1_pub = [i["public_ip"] for i in perc_nodes if "PERC-01" in i["tags_all"]["Name"]]
                data[0].append('Perc-01 Public IP')
                instance_data.append(perc_1_pub[0])
                perc_1_priv = [i["private_ip"] for i in perc_nodes if "PERC-01" in i["tags_all"]["Name"]]
                data[0].append('Perc-01 Private IP')
                instance_data.append(perc_1_priv[0])
                perc_2_pub = [i["public_ip"] for i in perc_nodes if "PERC-02" in i["tags_all"]["Name"]]
                data[0].append('Perc-02 Public IP')
                instance_data.append(perc_2_pub[0])
                perc_2_priv = [i["private_ip"] for i in perc_nodes if "PERC-02" in i["tags_all"]["Name"]]
                data[0].append('Perc-02 Private IP')
                instance_data.append(perc_2_priv[0])
                perc_3_pub = [i["public_ip"] for i in perc_nodes if "PERC-03" in i["tags_all"]["Name"]]
                data[0].append('Perc-03 Public IP')
                instance_data.append(perc_3_pub[0])
                perc_3_priv = [i["private_ip"] for i in perc_nodes if "PERC-03" in i["tags_all"]["Name"]]
                data[0].append('Perc-03 Private IP')
                instance_data.append(perc_3_priv[0])
            except:
                pass
            data.append(instance_data)
    return(data)

def get_lab_instance_ids_from_tag(url,headers,controller_id,tag_name):
    """
    The get_lab_instance_ids_from_tag function accepts a Morpheus API URL,
    a dictionary of HTTP headers containing the user's bearer token,
    the ID of the controller instance to query for lab instances, and 
    the name of the tag that contains all lab instance IDs. The function returns a list 
    of all lab instance IDs.
    
    :param url: Specify the controller url
    :param headers: Pass the api key to the get_lab_instance_ids function
    :param controller_id: Identify the controller to which the api call will be made
    :param tag_name: Specify the tag that you want to search for
    :return: A list of instance ids that are tagged with the specified tag name
    :doc-author: Trelent
    """
    endpoint = "/api/instances"
    resp = requests.get(f'{url}{endpoint}/{controller_id}',headers=headers,verify=False)
    tags = resp.json()["instance"]["tags"]
    for tag in tags:
        if tag["name"] == tag_name:
            ids = tag["value"]
    return(json.loads(ids))



