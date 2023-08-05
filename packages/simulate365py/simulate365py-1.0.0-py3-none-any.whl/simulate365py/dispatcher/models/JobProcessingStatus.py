from enum import IntEnum

class JobProcessingStatus(IntEnum):
    NotCalculated = 0
    Finished = 1
    Failed = 2
    Cancelled = 3