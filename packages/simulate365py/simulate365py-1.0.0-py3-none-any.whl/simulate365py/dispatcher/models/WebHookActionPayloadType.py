from enum import IntEnum
class WebHookActionPayloadType(IntEnum):
    DefaultJson = 1
    CustomJson = 2     
    CustomFormdata = 3
