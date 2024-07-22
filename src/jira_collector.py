import requests
from requests.auth import HTTPBasicAuth
import json
from config import API_KEY, HOST


def get_json(names: dict, project_name: str, filter_name: str) -> dict:
    url = f"https://{HOST}/rest/api/2/search?expand=names"
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(f"https://{HOST}", API_KEY)
    query = {"jql": f"project = {project_name} and {filter_name}"}
    response = requests.request("GET", url, headers=headers, params=query, auth=auth)
    jira_load = json.loads(response.text)
    issues = jira_load["issues"]
    results = {}

    for i in range(len(issues)):
        issue = issues[i]
        result = {}
        for key in names:
            if type(key) is tuple:
                if len(key) == 2:
                    result[names[key]] = issue[key[0]][key[1]]
                else:
                    result[names[key]] = issue[key[0]][key[1]][key[2]]
            else:
                result[names[key]] = issue[key]

        results[result["ключ"]] = result

    return results
