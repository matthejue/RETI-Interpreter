from reti_ast import NT
from reti import RETI


class Interp_RETI:
    def interp_memory(self, arg, reti, deref=0):
        match arg:
            case NT.Immediate(val):
                memory_type = reti.registers["DS"] >> 30
                if memory_type == 0b00:
                    return reti.eprom[val + deref]
                elif memory_type == 0b01:
                    return reti.uart[val + deref]
                else:
                    return reti.sram[val + deref]
            case NT.Reg(reg):
                return reti.registers[reg]
            # immediate is always a memory address here, because all
            # 'immediate' instructions are always unambiguous

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
                reti.registers[reg] = reti.registers[reg] & int(val)
            case NT.Instr(NT.Load(), NT.Reg(reg), arg):  # arg=M(i)
                reti.registers[reg] = self.interp_memory(arg, reti)
            #  case NT.Instr(NT.Loadin(), reg_base, NT.Reg(reg), deref):
            #      reti.registers[reg] = self.interp_memory(reg_base, reti, self.interp_memory(deref, reti))
            # TODO: continue here
            #  case NT.Instr(NT.Loadi(), NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Instr(NT.Store(), NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Instr(NT.Storein(), NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Instr(NT.Move(), NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Jump(NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Int(NT.Reg(reg), NT.Immediate(val)):
            #  case NT.Rti(NT.Reg(reg), NT.Immediate(val)):
        return reti

    def interp_program(self, p):
        p.update_match_args()
        match p:
            case NT.Program(instructions):
                reti = RETI()
                for instr in instructions:
                    self.interp_instruction(instr, reti)
                return reti
