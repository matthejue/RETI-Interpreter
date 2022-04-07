import global_vars


class RETI:
    _instance = None

    def __init__(self):
        self.registers = {
            "ACC": 0,
            "IN1": 0,
            "IN2": 0,
            "PC": 0,
            "SP": 0,
            "BAF": 0,
            "CS": 0,
            "DS": 0,
        }
        self.memory = {i: 0 for i in range(global_vars.args.end_data_segment)}

    def __repr__(self):
        return f"{self.registers}\n{self.memory}"


#  def RETI():
#      if _RETI._instance is None:
#          _RETI._instance = _RETI()
#      return _RETI._instance
