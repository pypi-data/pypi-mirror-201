from s365dispatcher.models import InputParameterModel, OutputParameterModel, JobType

class NewJobPostModel:

    def __init__(self, job_type: JobType, flowsheet_identifier: str, input_parameters: dict[str, int], output_parameters):
        self.JobType = job_type
        self.FlowsheetIdentifier = flowsheet_identifier
        self.InputParameters = input_parameters
        self.OutputParameters = output_parameters

    JobType = None
    FlowsheetIdentifier: str = None
    #FlowsheetFromJobId = None
    StepEvaluationFunction: str = ""
    InputParameters: dict[str, float] = []
    OutputParameters: list[str] = []
    #Actions=None
    #Settings=None
    Tags: list[str] = []

    def to_json(self):
        flowsheetIdSplit = self.FlowsheetIdentifier.split("/")

        mapped_input_params = []
        for k,v in self.InputParameters.items():
            mapped_input_params.append(InputParameterModel(k,v))

        return {
            #"apiKey":self.apiKey,
            "JobType": self.JobType,
            "FlowsheetDriveId": flowsheetIdSplit[0],
            "FlowsheetItemId": flowsheetIdSplit[1],
            "FlowsheetVersion": flowsheetIdSplit[2],
            #"FlowsheetFromJobId":job.FlowsheetFromJobId,
            "StepEvaluationFunction": self.StepEvaluationFunction,
            "InputParameters": list(map(lambda p: p.to_json(), mapped_input_params)),
            "outputParameters": list(map(lambda p: OutputParameterModel(p).to_json(), self.OutputParameters)),
            #"Actions": None if isinstance(job.Actions,type(None)) else job.Actions.__dict__,
            #"Settings":None if isinstance(job.Settings,type(None)) else job.Settings.__dict__,
            "Tags": self.Tags
        }

