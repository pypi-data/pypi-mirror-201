from simulate365py.dispatcher.models import InputParameterModel

class NewJobFromFilterPostModel:
    def __init__(self,  filterUniqueIdentifier: str, input_parameters: dict[str, int]):
       
        self.FilterUniqueIdentifier = filterUniqueIdentifier
        self.InputParameters = input_parameters
       

    ApiKey=""
    FilterUniqueIdentifier=""
    InputParameters: dict[str, float] = []
    Actions=None
    Settings=None
    Tags: list[str] = []

    def to_json(self):
       

        mapped_input_params = []
        for k,v in self.InputParameters.items():
            mapped_input_params.append(InputParameterModel(k,v))

        return {           
            
            "FilterUniqueIdentifier": self.FilterUniqueIdentifier,           
            "InputParameters": list(map(lambda p: p.to_json(), mapped_input_params)),         
           
            "Tags": self.Tags
        }