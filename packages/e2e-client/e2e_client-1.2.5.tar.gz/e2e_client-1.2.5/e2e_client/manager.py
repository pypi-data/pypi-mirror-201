from e2e_client.request_service import Request
from e2e_client.constants import BASE_URL
from e2e_client.exceptions import TokenException

class Manager:
    def __init__(self, **kwargs):
        self.api_key = kwargs['api_key']
        self.api_token = kwargs['api_token']

    def check_token(self):
        try:
            my_payload = {}
            API_key=self.api_key
            Auth_Token=self.api_token
            url = BASE_URL+"myaccount/api/v1/e2e_dns/forward/?apikey="+API_key+"&contact_person_id=null&location=Delhi"
            req="GET"
            status=Request(url, Auth_Token, my_payload, req).response.json()
            return True
        except:    
            if status['responseCode']:
                raise TokenException("Token or key is invalid")
            