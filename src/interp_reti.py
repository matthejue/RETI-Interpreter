from reti_ast import NT
from reti import RETI


class Interp_RETI:
    def interp_jump_condition(self, condition, jumplength, reti):
        if condition:
            reti.registers["PC"] += jumplength
        else:
            reti.registers["PC"] += 1

    def interp_operation(self, operand1, operation, operand2):
        match operation:
            case (NT.Add() | NT.Addi()):
                # sigextension
                return operand1 + operand2
            case (NT.Sub() | NT.Subi()):
                return operand1 - operand2
            case (NT.Mult() | NT.Multi()):
                return operand1 * operand2
            case (NT.Div() | NT.Divi()):
                return operand1 // operand2
            case (NT.Mod() | NT.Modi()):
                return operand1 % operand2
            case (NT.Oplus() | NT.Oplusi()):
                # signextension mit 0en
                return operand1 ^ operand2
            case (NT.Or() | NT.Ori()):
                return operand1 | operand2
            case (NT.And() | NT.Andi()):
                return operand1 & operand2

    def interp_memory_store(self, destination, source, reti) -> int:
        match destination:
            # addressbus
            case NT.Immediate(val):
                higher_bits = (reti.registers["DS"] >> 22) % 0b100000000 << 22
                memory_type = reti.registers["DS"] >> 30
                match memory_type:
                    case 0b00:
                        reti.eprom[abs(int(val)) + higher_bits] = source
                    case 0b01:
                        reti.uart[abs(int(val)) + higher_bits] = source
                    case _:
                        reti.sram[abs(int(val)) + higher_bits] = source
            case NT.Reg(reg):
                reti.registers[reg] = source
            # right_databus
            case int():
                # TODO: signextension
                memory_type = destination >> 30
                match memory_type:
                    case 0b00:
                        reti.eprom[destination << 2 >> 2] = source
                    case 0b01:
                        reti.uart[destination << 2 >> 2] = source
                    case _:
                        reti.sram[destination << 2 >> 2] = source

    def interp_memory_load(self, source, reti) -> int:
        match source:
            # addressbus
            case NT.Immediate(val):
                higher_bits = (reti.registers["DS"] >> 22) % 0b100000000 << 22
                memory_type = reti.registers["DS"] >> 30
                match memory_type:
                    case 0b00:
                        return reti.eprom[abs(int(val)) + higher_bits]
                    case 0b01:
                        return reti.uart[abs(int(val)) + higher_bits]
                    case _:
                        return reti.sram[abs(int(val)) + higher_bits]
            case NT.Reg(reg):
                return reti.registers[reg]
            # right databus
            case int():
                memory_type = source >> 30
                match memory_type:
                    case 0b00:
                        return reti.eprom[source << 2 >> 2]
                    case 0b01:
                        return reti.uart[source << 2 >> 2]
                    case _:
                        return reti.sram[source << 2 >> 2]
            case _:
                #  raise TODO: sich hier was überlegen
                ...

    def interp_instruction(self, instr, reti):
        match instr:
            case NT.Instr(
                operation,
                NT.Reg() as destination,
                (NT.Immediate() | NT.Reg()) as source,
            ):
                self.interp_memory_store(
                    destination,
                    self.interp_operation(
                        self.interp_memory_load(destination, reti),
                        operation,
                        self.interp_memory_load(source, reti),
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(operation, NT.Reg() as destination, NT.Immediate(val)):
                # TODO: Signextension? Bei Oplusi, Ori, Andi wird immer mit 0en signextendet
                self.interp_memory_store(
                    destination,
                    self.interp_operation(
                        self.interp_memory_load(destination, reti), operation, int(val)
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Load(), NT.Reg() as destination, NT.Immediate() as source):
                self.interp_memory_store(
                    destination, self.interp_memory_load(source, reti), reti
                )
                reti.registers["PC"] += 1
            case NT.Instr(
                NT.Loadin(),
                NT.Reg() as reg_source,
                NT.Reg() as destination,
                NT.Immediate(val),
            ):
                self.interp_memory_store(
                    destination,
                    self.interp_memory_load(
                        abs(self.interp_memory_load(reg_source, reti)) + int(val), reti
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Loadi(), NT.Reg() as destination, NT.Immediate(val)):
                # TODO: Signextension?
                self.interp_memory_store(
                    destination,
                    int(val),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(
                NT.Store(), NT.Reg() as source, NT.Immediate() as destination
            ):
                self.interp_memory_store(
                    destination, self.interp_memory_load(source, reti), reti
                )
                reti.registers["PC"] += 1
            case NT.Instr(
                NT.Storein(),
                NT.Reg() as destination,
                NT.Reg() as reg_source,
                NT.Immediate(val),
            ):
                self.interp_memory_store(
                    abs(self.interp_memory_load(destination, reti)) + int(val),
                    self.interp_memory_load(
                        self.interp_memory_load(reg_source, reti), reti
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Move(), NT.Reg() as source, NT.Reg() as destination):
                self.interp_memory_store(
                    destination, self.interp_memory_load(source, reti), reti
                )
                reti.registers["PC"] += 1
            case NT.Jump(relation, NT.Immediate(val)):
                match relation:
                    case NT.LT():
                        self.interp_jump_condition(
                            0 < reti.registers["ACC"], int(val), reti
                        )
                    case NT.LTE():
                        self.interp_jump_condition(
                            0 <= reti.registers["ACC"], int(val), reti
                        )
                    case NT.GT():
                        self.interp_jump_condition(
                            0 > reti.registers["ACC"], int(val), reti
                        )
                    case NT.GTE():
                        self.interp_jump_condition(
                            0 >= reti.registers["ACC"], int(val), reti
                        )
                    case (NT.EQ() | NT.EQ2()):
                        self.interp_jump_condition(
                            0 == reti.registers["ACC"], int(val), reti
                        )
                    case (NT.NEQ() | NT.NEQ2()):
                        self.interp_jump_condition(
                            0 != reti.registers["ACC"], int(val), reti
                        )
            case NT.Int(NT.Immediate(val)):
                # save PC
                # jump to start address of isr
                self.interp_memory_store(
                    NT.Reg("PC"), self.interp_memory_load(abs(int(val)), reti), reti
                )
            case NT.Rti():
                ...

    def interp_program(self, p):
        p.update_match_args()
        match p:
            case NT.Program(instructions):
                reti = RETI()
                next_instr = reti.registers["PC"]
                while next_instr < len(instructions):
                    self.interp_instruction(instructions[next_instr], reti)
                    next_instr = reti.registers["PC"]
                return reti
