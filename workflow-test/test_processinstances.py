# -*- coding: utf-8 -*-
"""
workflow processes tests
"""

# set certificate password using
# keyring set .certs my.p12

import ssl_context
import unittest
import base64
import os
from workflow import ApiClient as WorkflowApiClient
from workflow.configuration import Configuration as WorkflowConfiguration
from workflow.api.process_instances_api import ProcessInstancesApi
from filedossier import ApiClient as FiledossierApiClient
from filedossier.configuration import Configuration as FiledossierConfiguration
from filedossier.api.dossiers_api import DossiersApi



class TestProcessInstances(unittest.TestCase):

    def setUp(self):
        self.workflowUrl="https://devel.net.ilb.ru/workflow-web/web/v2"
        self.setUpWorkflow()
        self.setUpFiledossier()
    def setUpWorkflow(self):
        configuration = WorkflowConfiguration()
        configuration.host=self.workflowUrl
        configuration.username =  os.environ.get('USER')
        configuration.password = "123"
        configuration.debug=True
        auth_header='Basic ' + base64.b64encode(bytes(configuration.username+':'+configuration.password, 'utf-8')).decode("utf-8")
        self.process_api = ProcessInstancesApi(WorkflowApiClient(configuration=configuration,header_name="Authorization",header_value=auth_header))
    def setUpFiledossier(self):
        configuration = FiledossierConfiguration()
        configuration.host=self.workflowUrl
        configuration.username =  os.environ.get('USER')
        configuration.password = "123"
        configuration.debug=True
        auth_header='Basic ' + base64.b64encode(bytes(configuration.username+':'+configuration.password, 'utf-8')).decode("utf-8")
        self.filedossier_api = DossiersApi(FiledossierApiClient(configuration=configuration,header_name="Authorization",header_value=auth_header))
    def test_createProcessInstanceAndNext(self):
        self.nextActivity = self.process_api.create_process_instance_and_next(process_definition_id="stockvaluation_fairpricecalc",body={})
        print('nextActivity', self.nextActivity)
        body={'ticker':'ОФЗ 26223'}
        self.nextActivity=self.process_api.complete_and_next(self.nextActivity.id,self.nextActivity.process_instance_id,body=body)
        print('nextActivity', self.nextActivity)
        self.activityForm=self.process_api.get_activity_form1(self.nextActivity.id,self.nextActivity.process_instance_id)
        print('activityForm!!!', self.activityForm)
        activityDossier=self.activityForm['activityDossier']
        print('activityDossier', activityDossier)
        dossier = self.filedossier_api.get_dossier(activityDossier['dossierKey'],activityDossier['dossierPackage'],activityDossier['dossierCode'])
        print('dossier', dossier)
        response=self.filedossier_api.download('fairpricecalc',activityDossier['dossierKey'],activityDossier['dossierPackage'],activityDossier['dossierCode'],_preload_content=False)
        f= open("/tmp/content.ods","wb")
        f.write(response.data)
        print('content url',self.workflowUrl + '/dossiers/' + activityDossier['dossierKey'] + '/stockvaluation/stockvaluation_fairpricecalc/dossierfiles/fairpricecalc')
        print('done')
if __name__ == '__main__':
    unittest.main()
