class InputParameterModel:
    
    def __init__(self, parameter: str, value: float):
      self.Parameter = parameter
      self.Value=value

    def to_json(self):
      return {
        "Parameter": self.Parameter,
        "Value": self.Value
      }