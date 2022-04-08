from reti_ast import NT
from reti import RETI


class Interp_RETI:
    def interp_memory(self, arg, reti) -> int:
        match arg:
            case NT.Immediate(val):
                higher_bits = (reti.registers["DS"] >> 22) % 0b100000000 << 22
                memory_type = reti.registers["DS"] >> 30
                if memory_type == 0b00:
                    return reti.eprom[val + higher_bits]
                elif memory_type == 0b01:
                    return reti.uart[val + higher_bits]
                else:
                    return reti.sram[val + higher_bits]
            case NT.Reg(reg):
                return reti.registers[reg]
            case int():
                memory_type = arg >> 30
                if memory_type == 0b00:
                    return reti.eprom[arg]
                elif memory_type == 0b01:
                    return reti.uart[arg]
                else:
                    return reti.sram[arg]
            case _:
                #  raise TODO: sich hier was überlegen
                ...

    def interp_instruction(self, instr, reti):
        match instr:
            case NT.Instr(NT.Add(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] + self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Addi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] + int(val)
            case NT.Instr(NT.Sub(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] - self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Subi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] - int(val)
            case NT.Instr(NT.Mult(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] * self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Multi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] * int(val)
            case NT.Instr(NT.Div(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] // self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Divi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] // int(val)
            case NT.Instr(NT.Mod(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] % self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Modi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] % int(val)
            case NT.Instr(NT.Oplus(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] ^ self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Oplusi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] ^ int(val)
            case NT.Instr(NT.Or(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] | self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Ori(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = reti.registers[reg] | int(val)
            case NT.Instr(NT.And(), NT.Reg(reg), arg):
                reti.registers[reg] = reti.registers[reg] & self.interp_memory(
                    arg, reti
                )
            case NT.Instr(NT.Andi(), NT.Reg(reg), NT.Immediate(val)):
                # TODO: wegen Signextension überlegen
                reti.registers[reg] = reti.registers[reg] & int(val)
            case NT.Instr(NT.Load(), NT.Reg(reg), NT.Immediate() as M):  # arg=M(i)
                reti.registers[reg] = self.interp_memory(M, reti)
            case NT.Instr(
                NT.Loadin(), NT.Reg() as reg_base, NT.Reg(reg), NT.Immediate(deref)
            ):  # reg_base=Reg
                reti.registers[reg] = self.interp_memory(
                    self.interp_memory(reg_base, reti) + int(deref), reti
                )
            case NT.Instr(NT.Loadi(), NT.Reg(reg), NT.Immediate(val)):
                reti.registers[reg] = (
                    int(val) + (reti.registers["DS"] >> 22) % 0b100000000 << 22
                )
            case NT.Instr(NT.Store(), NT.Reg(reg), NT.Immediate(val) as M):
                #  reti. = reti.registers[reg]
                ...
            case NT.Instr(NT.Storein(), NT.Reg(reg1), NT.Reg(reg2), NT.Immediate(val)):
                #  reti = reti.registers[reg]
                ...
            case NT.Instr(NT.Move(), NT.Reg(reg1), NT.Reg(reg2)):
                reti.registers[reg2] = reti.registers[reg1]
            #  case NT.Jump(NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Int(NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Rti(NT.Reg(reg), NT.Immediate(val)):

    def interp_program(self, p):
        p.update_match_args()
        match p:
            case NT.Program(instructions):
                reti = RETI()
                for instr in instructions:
                    self.interp_instruction(instr, reti)
                return reti
