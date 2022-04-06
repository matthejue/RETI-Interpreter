class Instr:

    __match_args__ = ("self.instruction_name", "self.arguments[0]", "self.arguments[1]")

    def __init__(self, instruction_name, *args):
        self.instruction_name = instruction_name
        self.arguments = args


class Jump:

    __match_args__ = ("self.relation", "self.argument")

    def __init__(self, relation, argument):
        self.relation = relation
        self.argument = argument


class Reg:

    __match_args__ = ("register_name",)

    def __init__(self, register_name):
        self.register_name = register_name


class Immediate:

    __match_args__ = ("immediate_value",)

    def __init__(self, immediate_value):
        self.immediate_value = immediate_value
