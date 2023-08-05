from enum import IntEnum

class JobType(IntEnum):
    RunFlowsheet = 1
    AnalyzeFlowsheet = 2       
    RunFlowsheetStepByStep = 3
