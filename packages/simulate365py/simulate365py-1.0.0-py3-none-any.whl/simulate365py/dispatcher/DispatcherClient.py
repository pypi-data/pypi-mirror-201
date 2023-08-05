from pprint import pprint
import requests
import json

from simulate365py.dispatcher.models.Environment import Environment
from simulate365py.dispatcher.models.NewJobPostModel import NewJobPostModel
from simulate365py.dispatcher.models.ExternalClientResultResponseModel import ExternalClientResultResponseModel, ExternalClientResultResponseModel_OutputParameter
from simulate365py.dispatcher.models.NewJobFromFilterPostModel import NewJobFromFilterPostModel

class DispatcherClient:

    def __init__(self, apiKey: str, environment: Environment = Environment.Production):
      self.apiKey = apiKey
      self.environment = environment

    def __get_url(self, path):
      base_url = "https://unknown-environment"
      if (self.environment == Environment.Production):
        base_url = "https://dispatcher-service.azurewebsites.net"
      elif (self.environment == Environment.Staging):
        base_url = "https://dispatcher-service-staging.azurewebsites.net"
      elif (self.environment == Environment.Localhost):
        base_url = "http://localhost:7470"
      else:
        raise Exception("Unknown environment.")

      return base_url + path;

    ##
    # Submit job to Dispatcher
    ##
    def submit_job(self, job: NewJobPostModel) -> int:
            
      api_url = self.__get_url("/api/jobs")    

      dictModel = job.to_json()
      dictModel['ApiKey'] = self.apiKey

      postData= json.dumps(dictModel)       
      #print("Json data:" + postData)
      headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
      response = requests.post(api_url, data=postData, headers=headers, verify=True)
      #print("response:" +str(response))
      if response.status_code==200:
         responseModel=json.loads(response.content)
         return responseModel["jobId"]
      else:
        error= str(response.content)
        print("An error occured while submitting jobs to API. Error:"+error)

    def submit_job_from_filter(self, model:NewJobFromFilterPostModel) -> int:
      api_url = self.__get_url("/api/jobs/from-filter")    

      dictModel = model.to_json()
      dictModel['ApiKey'] = self.apiKey

      postData= json.dumps(dictModel)       
      #print("Json data:" + postData)
      headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
      response = requests.post(api_url, data=postData, headers=headers, verify=True)
      #print("response:" +str(response))
      if response.status_code==200:
         responseModel=json.loads(response.content)
         return responseModel["jobId"]
      else:
        error= str(response.content)
        print("An error occured while submitting jobs to API. Error:"+error)  


     
    
    def get_job_results(self, jobId: int) -> ExternalClientResultResponseModel:
      api_url =  self.__get_url("/api/external-clients/jobs/"+ str(jobId))
      #print(api_url)

      headers = {'Authorization': 'ApiKey ' + self.apiKey}
      response = requests.get(api_url, headers=headers, verify=True)
      if response.status_code == 200:
         responseModel = self._map_results_respones_to_model(response.content)
         return responseModel
      else:
        error= str(response.content)
        #print("An error occured while getting results. Response status code is " + str(response.status_code) + ". Error: " + error)

    def _map_results_respones_to_model(self, response: bytes):
      obj = json.loads(response);
      model = ExternalClientResultResponseModel()
      model.processing_status = obj["processingStatus"]
      model.error = obj["error"]
      if obj["outputParameters"] is not None:
        model.output_parameters = map(self._map_output_parameter_to_model, obj["outputParameters"])

      return model

    def _map_output_parameter_to_model(self, p):
      model = ExternalClientResultResponseModel_OutputParameter()
      model.parameter = p["parameter"]
      model.alias = p["alias"]
      model.value = p["value"]
      model.unit = p["unit"]
      return model
   
   