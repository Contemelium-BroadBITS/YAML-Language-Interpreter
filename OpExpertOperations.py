from hashlib import md5
from io import BytesIO
from json import dumps, loads
from requests import Session





class Interactions:
    
    def __init__(self, username, password, CRMURL):
        
        self.username = username
        self.password = password
        self.CRMURL = CRMURL
        self.sessionID = False
    
    
    
    # This functions returns a Session ID by logging in
    def login(self):
        
        data = {
            'user_auth': {
                'user_name': self.username, 
                'password': md5(self.password.encode()).hexdigest()
            }
        }
        
        response = self.__call('login', data)
        self.sessionID = response.get('id')
    
    
    
    # This function performs API calls as per request
    def __call(self, method, data, URL = False):
        
        curlRequest = Session()
        
        payload = {
            'method': method, 
            'input_type': 'JSON', 
            'response_type': 'JSON', 
            'rest_data': dumps(data), 
            'script_command': True
        }
        
        response = curlRequest.post(URL if URL else self.CRMURL, data = payload)
        curlRequest.close()
        
        result = loads(response.text)
        
        return result
    
    
    
    # This function gets the data from an integration using the integration ID
    def getIntegrationWithID(self, reportID = '', params = ''):
        
        if self.sessionID:
            
            data = {
                'session': self.sessionID, 
                'report_id': reportID, 
                'UserInputParam': []
            }
            
            try:
                return self.__call('getAPIReportResponse', data)
            except:
                return "An error occurred. Please try again after verifying your session ID and report ID."
            
        else:
            return "You cannot proceed with this action without initializing a session."