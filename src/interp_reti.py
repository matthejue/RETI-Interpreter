from reti_nodes import N
from reti import RETI
import global_vars
import os
from parse_instrs import COMPUTE_IMMEDIATE_INSTRUCTION, COMPUTE_INSTRUCTION
from errors import Errors


class RETIInterpreter:
    # when the <outabse>.out file gets written for the first time it should
    # overwrite everything else
    first_write_out = True
    first_write_reti_state = True

    def _jump_condition(self, condition, offset, reti):
        if condition:
            reti.registers["PC"] += offset
        else:
            reti.registers["PC"] += 1

    def _op(self, operand1, operation, operand2):
        match operation:
            case (N.Add() | N.Addi()):
                # sigextension
                return (operand1 + operand2) % 2**32
            case (N.Sub() | N.Subi()):
                return (operand1 - operand2) % 2**32
            case (N.Mult() | N.Multi()):
                return (operand1 * operand2) % 2**32
            case (N.Div() | N.Divi()):
                return (operand1 // operand2) % 2**32
            case (N.Mod() | N.Modi()):
                return (operand1 % operand2) % 2**32
            case (N.Oplus() | N.Oplusi()):
                # signextension mit 0en
                return (operand1 ^ operand2) % 2**32
            case (N.Or() | N.Ori()):
                return (operand1 | operand2) % 2**32
            case (N.And() | N.Andi()):
                return (operand1 & operand2) % 2**32

    def _memory_store(self, destination, source, reti) -> int:
        match destination:
            # addressbus
            case N.Num(val):
                higher_bits = (reti.registers["DS"] >> 22) % 0b100000000 << 22
                memory_type = reti.registers["DS"] >> 30
                match memory_type:
                    case 0b00:
                        reti.eprom[abs(int(val)) + higher_bits] = source
                    case 0b01:
                        reti.uart[abs(int(val)) + higher_bits] = source
                    case _:
                        reti.sram[abs(int(val)) + higher_bits] = source
            case N.Reg(reg):
                reti.registers[reg.value] = source
            # right_databus
            case int():
                # TODO: signextension
                memory_type = destination >> 30
                match memory_type:
                    case 0b00:
                        reti.eprom[((destination << 2) % 2**32) >> 2] = source
                    case 0b01:
                        reti.uart[((destination << 2) % 2**32) >> 2] = source
                    case _:
                        reti.sram[((destination << 2) % 2**32) >> 2] = source

    def _memory_load(self, source, reti) -> int:
        match source:
            # addressbus
            case N.Num(val):
                higher_bits = (reti.registers["DS"] >> 22) % 0b100000000 << 22
                memory_type = reti.registers["DS"] >> 30
                match memory_type:
                    case 0b00:
                        return reti.eprom[abs(int(val)) + higher_bits]
                    case 0b01:
                        return reti.uart[abs(int(val)) + higher_bits]
                    case _:
                        return reti.sram[abs(int(val)) + higher_bits]
            case N.Reg(reg):
                return reti.registers[reg.value]
            # right databus
            case int():
                memory_type = source >> 30
                match memory_type:
                    case 0b00:
                        return reti.eprom[((source << 2) % 2**32) >> 2]
                    case 0b01:
                        return reti.uart[((source << 2) % 2**32) >> 2]
                    case _:
                        return reti.sram[((source << 2) % 2**32) >> 2]
            case _:
                #  raise TODO: sich hier was überlegen
                ...

    def _instr(self, instr, reti):
        match instr:
            case N.Instr(
                operation,
                [N.Reg() as destination, (N.Num() | N.Reg()) as source],
            ) if type(operation) in COMPUTE_INSTRUCTION.values():
                self._memory_store(
                    destination,
                    self._op(
                        self._memory_load(destination, reti),
                        operation,
                        self._memory_load(source, reti),
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case N.Instr(operation, [N.Reg() as destination, N.Num(val)]) if type(
                operation
            ) in COMPUTE_IMMEDIATE_INSTRUCTION.values():
                # TODO: Signextension? Bei Oplusi, Ori, Andi wird immer mit 0en signextendet
                self._memory_store(
                    destination,
                    self._op(self._memory_load(destination, reti), operation, int(val)),
                    reti,
                )
                reti.registers["PC"] += 1
            case N.Instr(N.Load(), [N.Reg() as destination, N.Num() as source]):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case N.Instr(
                N.Loadin(),
                [N.Reg() as reg_source, N.Reg() as destination, N.Num(val)],
            ):
                self._memory_store(
                    destination,
                    self._memory_load(
                        (abs(self._memory_load(reg_source, reti)) + int(val)) % 2**32,
                        reti,
                    ),
                    reti,
                )
                reti.registers["PC"] += 1
            case N.Instr(N.Loadi(), [N.Reg() as destination, N.Num(val)]):
                # TODO: Signextension?
                self._memory_store(
                    destination,
                    int(val),
                    reti,
                )
                reti.registers["PC"] += 1
            case N.Instr(N.Store(), [N.Reg() as source, N.Num() as destination]):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case N.Instr(
                N.Storein(),
                [N.Reg() as destination, N.Reg() as reg_source, N.Num(val)],
            ):
                self._memory_store(
                    (abs(self._memory_load(destination, reti)) + int(val)) % 2**32,
                    self._memory_load(reg_source, reti),
                    reti,
                )
                reti.registers["PC"] += 1
            case N.Instr(N.Move(), [N.Reg() as source, N.Reg() as destination]):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case N.Jump(relation, N.Num(val)):
                match relation:
                    case N.Lt():
                        self._jump_condition(0 < reti.registers["ACC"], int(val), reti)
                    case N.LtE():
                        self._jump_condition(0 <= reti.registers["ACC"], int(val), reti)
                    case N.Gt():
                        self._jump_condition(0 > reti.registers["ACC"], int(val), reti)
                    case N.GtE():
                        self._jump_condition(0 >= reti.registers["ACC"], int(val), reti)
                    case (N.Eq()):
                        self._jump_condition(0 == reti.registers["ACC"], int(val), reti)
                    case (N.NEq()):
                        self._jump_condition(0 != reti.registers["ACC"], int(val), reti)
                    case (N.Always()):
                        self._jump_condition(True, int(val), reti)
                    case (N.NOp()):
                        self._jump_condition(False, int(val), reti)
            case N.Int(N.Num(val)):
                # save PC to stack
                reti.sram[reti.registers["SP"]] = reti.registers["PC"]
                reti.registers["SP"] = reti.registers["SP"] - 1
                # jump to start address of isr
                reti.registers["PC"] = reti.sram[abs(int(val))]
            case N.Rti():
                # restore PC
                reti.registers["PC"] = reti.sram[reti.registers["SP"] + 1]
                # delete PC from stack
                reti.registers["SP"] = reti.registers["SP"] + 1
            case N.Call(N.Name("PRINT"), N.Reg(reg)):
                if global_vars.args.print_output:
                    if global_vars.args.print:
                        print("\nOutput:\n\t" + str(reti.registers[reg.value]))
                    if global_vars.outbase:
                        if self.first_write_out:
                            with open(
                                global_vars.outbase + ".out", "w", encoding="utf-8"
                            ) as fout:
                                fout.write(str(reti.registers[reg.value]))
                            self.first_write_out = False
                        else:
                            with open(
                                global_vars.outbase + ".out", "a", encoding="utf-8"
                            ) as fout:
                                fout.write(" " + str(reti.registers[reg.value]))
                reti.registers["PC"] += 1
            case N.Call(N.Name("INPUT"), N.Reg(reg)):
                if global_vars.test_input:
                    reti.registers[reg.value] = global_vars.test_input.pop()
                else:
                    reti.registers[reg.value] = int(input())
                reti.registers["PC"] += 1

    def _preconfigs(self, p, reti):
        # set the CS, PC, DS and SP Register properly
        reti.registers["CS"] = global_vars.args.process_begin + 2**31
        reti.registers["PC"] = global_vars.args.process_begin + 2**31
        reti.registers["DS"] = (
            global_vars.args.process_begin + len(p.children) + 2**31
        )
        reti.registers["SP"] = (
            global_vars.args.process_begin
            + len(p.instrs)
            + global_vars.args.datasegment_size
            + 2**31
            - 1
        )
        if os.path.isfile(global_vars.outbase + ".in"):
            with open(global_vars.outbase + ".in", "r", encoding="utf-8") as fin:
                global_vars.test_input = list(
                    reversed([int(line) for line in fin.readline().split(" ")])
                )

    def _reti_state_option(self, reti_state):
        if global_vars.args.print:
            #  code = (
            #      Colorizer(
            #          str(ast_node.show_generated_code())
            #      ).colorize_reti_code()
            #      if global_vars.args.color
            #      else str(ast_node.show_generated_code())
            #  )
            print("\n" + str(reti_state))
        if global_vars.outbase:
            if self.first_write_reti_state:
                with open(
                    global_vars.outbase + ".reti_state",
                    "w",
                    encoding="utf-8",
                ) as fout:
                    fout.write(str(reti_state))
                self.first_write_reti_state = False
            else:
                with open(
                    global_vars.outbase + ".reti_state",
                    "a",
                    encoding="utf-8",
                ) as fout:
                    fout.write("\n\n" + str(reti_state))

    def _instrs(self, p: N.Program, reti):
        match p:
            case N.Program(_, instructions):
                while True:
                    i = reti.registers["PC"] - global_vars.args.process_begin - 2**31
                    next_instruction = (
                        instructions[i] if i < len(instructions) and i >= 0 else None
                    )
                    if not next_instruction:
                        break
                        # raise Errors.JumpedOutOfProgrammError()
                    match next_instruction:
                        case N.Jump(N.Always(), N.Num("0")):
                            if (
                                global_vars.args.reti_state
                                and not global_vars.args.verbose
                            ):
                                self._reti_state_option(reti)
                            # needs a newline at the end, else it differs from .out_except
                            with open(
                                global_vars.outbase + ".out", "a", encoding="utf-8"
                            ) as fout:
                                fout.write("\n")
                            break

                        case _:
                            self._instr(next_instruction, reti)
                    if global_vars.args.reti_state and global_vars.args.verbose:
                        self._reti_state_option(reti)

    def interp_reti(self, p: N.Program):
        # necessary for the __match_case__ of the nodes to work
        p.update_match_args()
        reti = RETI(p.instrs)
        self._preconfigs(p, reti)
        self._instrs(p, reti)
