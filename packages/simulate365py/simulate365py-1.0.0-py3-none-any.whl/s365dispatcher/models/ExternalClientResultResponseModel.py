import string
from typing import List
from s365dispatcher.models.JobProcessingStatus import JobProcessingStatus

class ExternalClientResultResponseModel_OutputParameter:
    parameter: string = None
    alias: string = None
    value: float = None
    unit: string = None

class ExternalClientResultResponseModel:
    processing_status: JobProcessingStatus = None
    error: string = None
    output_parameters: List[ExternalClientResultResponseModel_OutputParameter] = None