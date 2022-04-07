from reti_ast import NT
from reti import RETI


class Interp_RETI:
    def interp_program(self, p):
        match p:
            case NT.Program(instructions):
                reti = RETI()
                for instr in instructions:
                    self.interp_instruction(instr, reti)
                return reti

    def interp_instruction(self, instr, reti):
        match instr:
            case NT.Instr(NT.Add(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] + reti.memory(val)
            case NT.Instr(NT.Add(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] + reti.registers[reg2]
            case NT.Instr(NT.Addi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] + val
            case NT.Instr(NT.Sub(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] - reti.memory(val)
            case NT.Instr(NT.Sub(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] - reti.registers[reg2]
            case NT.Instr(NT.Subi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] - val
            case NT.Instr(NT.Mult(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] * reti.memory(val)
            case NT.Instr(NT.Mult(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] * reti.registers[reg2]
            case NT.Instr(NT.Multi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] * val
            case NT.Instr(NT.Div(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] // reti.memory(val)
            case NT.Instr(NT.Div(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] // reti.registers[reg2]
            case NT.Instr(NT.Divi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] // val
            case NT.Instr(NT.Mod(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] % reti.memory(val)
            case NT.Instr(NT.Mod(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] % reti.registers[reg2]
            case NT.Instr(NT.Modi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] % val
            case NT.Instr(NT.Oplus(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] ^ reti.memory(val)
            case NT.Instr(NT.Oplus(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] ^ reti.registers[reg2]
            case NT.Instr(NT.Oplusi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] ^ val
            case NT.Instr(NT.Or(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] | reti.memory(val)
            case NT.Instr(NT.Or(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] | reti.registers[reg2]
            case NT.Instr(NT.Ori(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] | val
            case NT.Instr(NT.And(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] & reti.memory(val)
            case NT.Instr(NT.And(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg1] = reti.registers[reg1] & reti.registers[reg2]
            case NT.Instr(NT.Andi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] & val
        return reti
