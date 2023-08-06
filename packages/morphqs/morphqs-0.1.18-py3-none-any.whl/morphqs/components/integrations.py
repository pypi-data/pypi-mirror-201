from ..morphclass import RequestsApi
import morphqs.logging.loghandler as loghandler
import json
import urllib
import sys

def add_integration(default_branch, repo_url, integration_name):
    """
    The add_integration function is used to create a new integration in Morpheus.
        It takes three arguments: 
            1) default_branch - the branch that will be checked out by default when cloning the repo (defaults to master)
            2) repo_url - The URL of the repository you want to integrate with Morpheus. This can be any valid git url, including SSH and HTTP(S). 
                For example: https://gitlab.com/jaredlutgen/morpheus_quickshots.git or git@github.com:jaredlutgen/morpheus-qu
            3) integration_name - the name of the integration. 
    
    :param default_branch: Set the default branch for the integration
    :param repo_url: Specify the url of the repository to be integrated
    :param integration_name: Find the integration id
    :return: An integration id
    :doc-author: Trelent
    """    
    
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    integrationname = urllib.parse.quote(integration_name)
    intid = cl.get(f"/api/integrations?name={integrationname}").json()
    try: 
        intid = intid["integrations"][0]["id"]
    except IndexError as e:
        intid = None
    if intid is not None: 
        logger.info(f"Integration {integration_name} already exists. Skipping.")
        logger.info(f"Integration ID: {intid}")
        logger.debug(intid)
        coderepoId = cl.get(f"/api/options/codeRepositories?integrationId={intid}").json()
        logger.debug(coderepoId)
        logger.debug(f"integration id: {intid}")
        logger.debug(f"code repo response: {coderepoId}")
        if coderepoId["data"] != []:
            repoid = coderepoId["data"][0]["value"]
            logger.debug(f"repo id {repoid}")
            return repoid
    else:
        logger.info(f"Integration {integration_name} does not exist. Creating.")
        root_int_payload = {"integration": {
                                "refresh": True,
                                "credential": {"type": "local"},
                                "type": "git",
                                "config": {
                                    "defaultBranch": default_branch, #"highered",
                                    "cacheEnabled": False
                                },
                                "name": integration_name, #"Morpheus Quickshots Base Repo",
                                "serviceUrl": repo_url #"https://gitlab.com/jaredlutgen/morpheus_quickshots.git"
                            }}
        logger.debug(f"Creating integration {integration_name} with payload {root_int_payload}")
        cl.post("/api/integrations", data = json.dumps(root_int_payload)).json()
        intid = cl.get(f"/api/integrations?name={integrationname}").json()
        try: 
            intid = intid["integrations"][0]["id"]
        except IndexError as e:
            intid = None
        coderepoId = cl.get(f"/api/options/codeRepositories?integrationId={intid}").json()
        logger.debug(coderepoId)
        logger.debug(f"integration id: {intid}")
        logger.debug(f"code repo response: {coderepoId}")
        if coderepoId["data"] != []:
            repoid = coderepoId["data"][0]["value"]
            logger.debug(f"repo id {repoid}")
            return repoid
        # logger.debug(coderepoId)
        # logger.debug(f"integration id: {intid}")
        # logger.debug(f"code repo response: {coderepoId}")
        # if coderepoId["data"] != []:
        #     repoid = coderepoId["data"][0]["value"]
        #     logger.debug(f"repo id {repoid}")
        #     return repoid
        # else: 
        #     logger.error("Failed to create integration")
        #     logger.error(coderepoId)
        #     sys.exit(1)
       



def add_integration_ansible(default_branch, repo_url, integration_name, ansibleplaybooks, ansibleroles, ansiblegroupvars, ansiblehostvars):
    """
    The add_integration_ansible function creates an Ansible integration in Morpheus.
    
    :param default_branch: Set the default branch for the integration
    :param repo_url: Specify the git repo url
    :param integration_name: Search for the integration
    :param ansibleplaybooks: Define the path to the playbooks directory in your repo
    :param ansibleroles: Specify the path to your ansible roles
    :param ansiblegroupvars: Specify the path to group_vars in your repository
    :param ansiblehostvars: Specify the location of host_vars files in your repo
    :return: The id of the integration
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    integrationname = urllib.parse.quote(integration_name)
    intid = cl.get(f"/api/integrations?name={integrationname}").json()
    try: 
        intid = intid["integrations"][0]["id"]
    except IndexError as e:
        intid = None
    if intid is not None: 
        logger.info(f"Integration {integration_name} already exists. Skipping.")
        logger.info(f"Integration ID: {intid}")
        logger.debug(intid)
        return intid
    else:
        logger.info(f"Integration {integration_name} does not exist. Creating.")
        root_int_payload = {"integration": {
                                "type": "ansible",
                                "name": integration_name,
                                "enabled": True,
                                "serviceUrl": repo_url,
                                "config": {
                                    "defaultBranch": default_branch,
                                    "ansiblePlaybooks": ansibleplaybooks,
                                    "ansibleRoles": ansibleroles,
                                    "ansibleGroupVars": ansiblegroupvars,
                                    "ansibleHostVars": ansiblehostvars,
                                    "ansibleGalaxyEnabled": False,
                                    "ansibleVerbose": False,
                                    "ansibleCommandBus": True,
                                    "cacheEnabled": False
                                    }
                                }
                            }
        logger.debug(f"Creating integration {integration_name} with payload {root_int_payload}")
        resp = cl.post("/api/integrations", data = json.dumps(root_int_payload)).json()
        logger.debug(resp)
        intid = resp["integration"]["id"]
        if resp["success"] == True:
            logger.info(f"Successfully created integration {integration_name}")
        if resp["success"] == False:
            logger.error(f"Failed to create integration {integration_name}")
            logger.error(resp["errors"])
        logger.debug(intid)
        logger.debug(resp)
        return intid