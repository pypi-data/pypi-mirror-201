
import requests
from files.Input import APIConfigFile


import datetime


class DataRequester:
    def __init__(self, api_endpoint=None, api_key=None, config_file=None) -> None:
        '''
        The `DataRequester` class must be initialized with an API endpoint and API
        key. These properties can be supplied explicitly to the class's constructor 
        method via the `api_endpoint` and `api_key` parameters, respectively, or they
        can be passed in through the name of a separate configuration file containing
        these attributes.

        The constructor method expects only one of these two methods to be utilized in
        the initializaton process. If arguments are passed to all three paramters, the
        `api_endpoint` and `api_key` arguments will take priority over the `config_file`
        argument. 
        
        :param api_endpoint: URI-formatted string that the `DataRequester` will
        submit all API requests to.

        :param api_key: Secure key used by the API endpoint to authorize
        requests sent by the `DataRequester`.

        :param config_file: Input file containing an API endpoint and API
        key that will be read and used by this instance of the `DataRequester`.
        '''
        if not all(api_endpoint, api_key, config_file):
            raise ValueError('''
                A valid URI endpoint and API key must be supplied to this
                class's constructor method, either explicitly or in a configuration
                file.
            ''')
        elif not config_file and (api_endpoint or api_key):
            raise ValueError('''
                A valid URI endpoint and API key must be supplied to this
                class's constructor method, either explicitly or in a configuration
                file.
            ''')
        elif all(api_endpoint, api_key):
            self.api_endpoint = api_endpoint
            self.api_key = api_key
        else:
            file = APIConfigFile(config_file)
            api_details = file.read_file_contents()
            
            self.api_endpoint = api_details[0]
            self.api_key = api_details[1]
    

    def authorize_request(self):
        return

    @authorize_request
    def send_api_request(self, api_request: str, request_method: str):
        return