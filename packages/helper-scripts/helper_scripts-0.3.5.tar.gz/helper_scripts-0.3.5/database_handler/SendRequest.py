import requests
from database_handler.logger import logger
from requests.exceptions import HTTPError
import json
import traceback

log = logger()

class SendRequest:
    def __init__(self, URL):
        self.URL = URL
        

    def send_request_func(self, method,request_body):
        error_response = {}
        try:
            the_response = requests.request(method=method,url = self.URL,data = request_body, headers={"Content-Type": "application/json"})

            the_response.raise_for_status()

            json_response = the_response.json()

            return json_response
            
        except Exception as err:
            
            log.log_message(traceback.print_exc())
                #raise ex
            return ({'response_code': 'Err', 'response_message': '%s' % (err)}), 400

    
    