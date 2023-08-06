from ..morphclass import RequestsApi
import morphqs.logging.loghandler as loghandler
import json
import sys

def create_task(branch, integration_id,task_name, hchighered_contentPath):
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    task = cl.get(f"/api/tasks?name={task_name}").json()
    try: 
        taskid = task["tasks"][0]["id"]
    except IndexError as e:
        taskid = None
    if taskid is not None:
        logger.info(f"Task {task_name} already exists with id {taskid}")
        return taskid
    else: 
        logger.info(f"Task {task_name} does not exist. Creating.")
        setup_payload = {"task": {
                                "name": task_name,
                                "taskType": {
                                    "code": "jythonTask"
                                },
                                "visibility": "private",
                                "labels": [
                                    "higher_ed_msp", "setup", "demo", "poc", "example"
                                ],
                                "taskOptions": {
                                    "pythonAdditionalPackages": "requests morphcp click",
                                    "username": None,
                                    "password": None,
                                    "passwordHash": None,
                                    "pythonBinary": None,
                                    "host": None,
                                    "localScriptGitId": None,
                                    "port": None,
                                    "pythonArgs": "highered",
                                    "localScriptGitRef": None
                                },
                                "file": {
                                    "sourceType": "repository",
                                    "contentRef": branch,
                                    "contentPath": hchighered_contentPath,
                                    "repository": {
                                        "id": integration_id,
                                    },
                                    "content": None
                                },
                                "resultType": None,
                                "executeTarget": "local",
                                "retryable": False,
                                "retryCount": 5,
                                "retryDelaySeconds": 10,
                                "allowCustomConfig": False
                            }
                        }
        logger.debug(f"Creating task {task_name} with payload {setup_payload}")
        resp = cl.post("/api/tasks", data = json.dumps(setup_payload)).json()
        logger.debug(resp)
        if resp["success"] == True:
            logger.info(f"Successfully created task {task_name}")
        if resp["success"] == False:
            logger.error(f"Failed to create task {task_name}")
            logger.error(resp["errors"])
        return resp

def create_workflow(task_name,workflow_name):
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    task = cl.get(f"/api/tasks?name={task_name}").json()
    try: 
        taskid = task["tasks"][0]["id"]
    except IndexError as e:
        taskid = None
        logger.error('Task is not created')
        if taskid is None: 
            sys.exit(1)
    workflow = cl.get(f"/api/task-sets?name={workflow_name}").json()
    try:
        workflowid = workflow["taskSets"][0]["id"]
    except IndexError as e:
        workflowid = None

    if workflowid is not None:
        logger.info(f"Workflow {workflow_name} already exists with id {workflowid}")
        return workflowid
    else:
        logger.info(f"Workflow {workflow_name} does not exist. Creating.")
        setup_payload = {"taskSet": {
                            "labels": ["higher_ed_msp", "setup", "demo", "poc", "example"],
                            "type": "operation",
                            "visibility": "private",
                            "tasks": [{
                                "taskId": taskid,
                                "taskPhase": "operation"
                            }],
                            "name": workflow_name,
                            "description": "Higher Education MSP Setup - utilized by the Higher Education MSP Content Pack"
                        }}
        resp = cl.post("/api/task-sets", data = json.dumps(setup_payload)).json()
        logger.debug(resp)
        if resp["success"] == True:
            logger.info(f"Successfully created workflow {workflow_name}")
        if resp["success"] == False:
            logger.error(f"Failed to create workflow {workflow_name}")
            logger.error(resp["errors"])
        return resp['taskSet']['id']

def catalog_items(workflow_id):
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    setup_payload = {"catalogItemType": {
                        "labels": ["higher_ed_msp", "setup", "demo", "poc", "example"],
                        "type": "workflow",
                        "visibility": "private",
                        "enabled": True,
                        "featured": False,
                        "allowQuantity": False,
                        "workflow": {"id": workflow_id},
                        "name": "Higher Education MSP Setup",
                        "category": "demo",
                        "description": "Utilized by the Higher Education MSP Content Pack. Primarily used to setup demo constructs.",
                        "context": "appliance"
                    }}
    resp = cl.post("/api/catalog-item-types", data = json.dumps(setup_payload)).json()
    if resp["success"] == True:
        logger.info("Successfully created catalog item")
    if resp["success"] == False:
        logger.error("Failed to create catalog item")
        logger.error(resp["errors"])



def inject_wiki_article():
    # Future Use Case.
    pass


def deploy_higher_ed_msp(branch, integration_id, hchighered_contentPath):
    task_name = "Higher Education MSP Setup"
    workflow_name = "Higher Education MSP Setup"
    create_task(branch, integration_id,task_name, hchighered_contentPath)
    workflow_id = create_workflow(task_name,workflow_name)
    catalog_items(workflow_id)
