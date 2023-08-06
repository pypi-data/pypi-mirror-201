{
    "task": {
        "name": "ansible_task_patches_ssh",
        "code": "hs_createdAccounts",
        "taskType": {
            "code": "jythonTask"
        },
        "visibility": "private",
        "labels": [
            "analytics",
            "igt"
        ],
        "taskOptions": {
            "password": null,
            "passwordHash": null,
            "sshKey": null,
            "pythonBinary": null,
            "port": null,
            "pythonArgs": "ansible",
            "pythonAdditionalPackages": "requests morphcp click",
            "localScriptGitId": null,
            "username": null,
            "localScriptGitRef": null,
            "host": null
        },
        "file": {
            "sourceType": "repository",
            "contentRef": "highered",
            "contentPath": "morph_contentpack/main.py",
            "repository": {
                "id": 23,
                "name": "morpheus_quickshots"
            },
            "content": null
        },
        "resultType": null,
        "executeTarget": "local",
        "retryable": false,
        "retryCount": 5,
        "retryDelaySeconds": 10,
        "allowCustomConfig": false,
        "credential": {
            "type": "local"
        }
    }
}