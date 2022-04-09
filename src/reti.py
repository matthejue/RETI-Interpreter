import global_vars


class RETI:
    _instance = None

    def __init__(self, instructions):
        min_sram_size = (
            global_vars.args.process_begin
            + len(instructions)
            + global_vars.args.datasegment_size
        )
        self.instructions = instructions
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
        self.eprom = {i: 0 for i in range(global_vars.args.eprom_size)}
        self.uart = {i: 0 for i in range(global_vars.args.uart_size)}
        self.sram = {
            i: 0 for i in range(max(global_vars.args.sram_size, min_sram_size))
        }

    def __repr__(self):
        start = global_vars.args.process_begin
        end = global_vars.args.process_begin + len(self.instructions) - 1
        new_sram = {
            i: (
                str(self.instructions[i - global_vars.args.process_begin])
                if i >= start and i <= end
                else "0"
            )
            for i in range(len(self.sram))
        }
        return f"Registers:\n\t{self.registers}\nEPROM:\n\t{self.eprom}\nUART:\n\t{self.uart}\nSRAM:\n\t{new_sram}"


#  def RETI():
#      if _RETI._instance is None:
#          _RETI._instance = _RETI()
#      return _RETI._instance
