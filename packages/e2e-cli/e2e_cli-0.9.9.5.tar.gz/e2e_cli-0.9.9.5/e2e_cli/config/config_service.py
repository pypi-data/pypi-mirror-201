from e2e_cli.core.request_service import Request
from e2e_cli.core.constants import BASE_URL

def is_valid(API_key, Auth_Token):
    url= BASE_URL+"myaccount/api/v1/customer/details/?apikey="+ API_key+"&contact_person_id=null"
    response= Request(url, Auth_Token, {}, 'GET').response.json()
    if ('code' in response):
        return True
    else:
        return False