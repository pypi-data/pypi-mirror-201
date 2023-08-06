import json
from e2e_client.request_service import Request
from e2e_client.constants import BASE_URL, E2E_NAME_SERVERS
from e2e_client.exceptions import DomainException
import whois
class payload:
    def __init__(self, **kwargs):
        self.zone_name = kwargs['zone_name']
        self.record_name = kwargs['record_name']
        self.content = kwargs['content']
        self.record_ttl = kwargs['record_ttl']
        self.record_type = kwargs['record_type']

    def my_payload(self):
        payload_dict = {
                        "zone_name":self.zone_name, 
                        "record_name":self.record_name, 
                        "content":self.content, 
                        "record_ttl":self.record_ttl, 
                        "record_type":self.record_type
                        }
        return payload_dict  

    def delete_payload(self):
        payload_dict = {
                        "zone_name":self.zone_name, 
                        "record_name":self.record_name, 
                        "content":self.content,
                        "record_type":self.record_type
                        }
        return payload_dict      

class Domain:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.api_key = kwargs['api_key']
        self.api_token = kwargs['api_token']
        self.zone_name = kwargs['zone_name']
        self.record_name = kwargs['record_name']
        self.content = kwargs['content']
        self.record_ttl = kwargs['record_ttl']
        self.record_type = kwargs['record_type']

    def get_all_domain(self):
        my_payload = {}
        API_key=self.api_key
        Auth_Token=self.api_token
        url = BASE_URL+"myaccount/api/v1/e2e_dns/forward/?apikey="+API_key+"&contact_person_id=null&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        return status['data']

    def add_record(self):
        domain_name = self.kwargs['domain_name']
        my_payload = payload(zone_name=self.zone_name, record_ttl=self.record_ttl, content=self.content, record_name=self.record_name, record_type=self.record_type).my_payload()
        API_key=self.api_key
        Auth_Token=self.api_token
        url = BASE_URL+"myaccount/api/v1/e2e_dns/forward/"+domain_name+"/?apikey="+API_key+"&contact_person_id=null&location=Delhi"
        req="POST"
        user_agent='cli_python'
        status=Request(url, Auth_Token, json.dumps(my_payload, indent=4), req, user_agent).response.json()
        if status['code'] != 200:
            raise Exception(status['errors']['message'])
        return status['data']

    def delete_record(self):
        domain_name = self.kwargs['domain_name']
        my_payload = payload(zone_name=self.zone_name, record_ttl=None, content=self.content, record_name=self.record_name, record_type=self.record_type).delete_payload()
        API_key=self.api_key
        Auth_Token=self.api_token
        url = BASE_URL+"myaccount/api/v1/e2e_dns/forward/"+domain_name+"/?apikey="+API_key+"&contact_person_id=null&location=Delhi"
        req="DELETE"
        user_agent='cli_python'
        status=Request(url, Auth_Token, json.dumps(my_payload, indent=4), req, user_agent).response.json()
        return status['data']

    def check_domain_valid(self):
        domain_name = self.kwargs['domain_name']
        domain = domain_name.strip('.')
        domian_info = whois.whois(domain)
        if E2E_NAME_SERVERS in domian_info.name_servers:
            raise DomainException('Domain not registered on e2e_networks')
        my_payload={}
        API_key=self.api_key
        Auth_Token=self.api_token
        url = BASE_URL+"myaccount/api/v1/e2e_dns/forward/"+domain_name+"/?apikey="+API_key+"&contact_person_id=null&location=Delhi"
        req="GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()
        if status['code'] != 200:
            raise DomainException('Domain not found')
        return status['data']
    