import requests

class Request:
    def __init__(self, url, Auth_Token, payload, req, user_agent='cli-e2e', query={}):
        self.headers= {
                        'Authorization': 'Bearer ' + Auth_Token,
                        'Content-Type': 'application/json',
                        'User-Agent' : user_agent
                        }
        self.response = requests.request(req, url, headers=self.headers, data=payload, params=query)

