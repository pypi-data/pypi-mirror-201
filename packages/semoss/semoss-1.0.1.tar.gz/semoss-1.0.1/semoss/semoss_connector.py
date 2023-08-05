import pandas as pd
import getpass
import os
import requests

class semoss_connector:
    def __init__(self, apiUrl):
        self.apiUrl = apiUrl
        self._pySemossSession = None
        self.insightId = ''

    def establishSession(self,username=None, password=None):
        while(username == None or username ==''):
            # check if its in the sys env
            username = os.getenv("SEMOSS_USERNAME")
            if (username == None):
                username = getpass.getpass('Username:')

        while(password == None or password ==''):
            # check if its in the sys env
            password = os.getenv("SEMOSS_PASSWORD")
            if (password == None):
                password = getpass.getpass('Password:')
        
        pySemossSession = requests.Session()
        login = pySemossSession.post(self.apiUrl + '/api/auth/login',  {'username': username, 'password':password})

        if (login.status_code == 200):
            self._pySemossSession = pySemossSession
            return True

    def endSession(self):
        self._pySemossSession.post(self.apiUrl + '/api/auth/logout/all')
        self._pySemossSession = None

    def importFrameFromSemossApi(self,project_id = None, insight_id = None, sql = None):
        if project_id == None:
            project_id = input('Please enter the Project ID: ')
        if insight_id == None:
            insight_id = input('Please enter the Insight ID: ')

        base_url = self.apiUrl + '/api/project-' + project_id + '/jdbc_json?insightId=' + insight_id + '&open=true&sql='
        
        if sql == None:
            sql = input('Please enter the SQL: ')

        
        queryColumns = sql[sql.find(' '):sql.lower().find('from')].strip().split(',')

        apiUrl = base_url+sql
        response = self._pySemossSession.get(apiUrl).json()

        try:
            return pd.DataFrame(response['dataArray'], columns=response['columns'])
        except:
            try:
                return pd.DataFrame(response['data'], columns=response['columns'])
            except:
                return None
    



    
    def runPixel(self,expression):
        if (self.insightId==''):
            response = self._pySemossSession.post(url = self.apiUrl + '/api/engine/runPixel', headers = {'Content-Type':'application/x-www-form-urlencoded; charset=utf-8'}, data = 'expression=META%7Ctrue&insightId=new')
            self.insightId = response.json()['insightID']
        
        data = 'expression=' + requests.utils.quote(expression)
        data += '&insightId=' + requests.utils.quote(self.insightId)

        response = self._pySemossSession.post(url = self.apiUrl + '/api/engine/runPixel', headers = {'Content-Type':'application/x-www-form-urlencoded; charset=utf-8'}, data = data)
        return response.json()


    def getDataFrameFromTaskData(self,expression):
        response = self.runPixel(expression)
        if (response['pixelReturn'][0]['operationType'][0] == 'TASK_DATA'):
            return pd.DataFrame(response['pixelReturn'][0]['output']['data']['values'], columns=response['pixelReturn'][0]['output']['data']['headers'])
        else:
            return None