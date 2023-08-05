from enum import IntEnum
class JobActionTriggerOn(IntEnum):
    Always = 1
    OnSuccess = 2       
    OnError = 3
    Custom = 4