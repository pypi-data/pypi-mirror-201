class OutputParameterModel:
    Parameter=""
    def __init__(self, parameter):
      self.Parameter = parameter

    def to_json(self):
      return {
        "Parameter": self.Parameter
      }
     