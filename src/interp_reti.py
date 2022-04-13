from reti_nodes import NT
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

    def _jump_condition(self, condition, jumplength, reti):
        if condition:
            reti.registers["PC"] += jumplength
        else:
            reti.registers["PC"] += 1

    def _op(self, operand1, operation, operand2):
        match operation:
            case (NT.Add() | NT.Addi()):
                # sigextension
                return (operand1 + operand2) % 2**32
            case (NT.Sub() | NT.Subi()):
                return (operand1 - operand2) % 2**32
            case (NT.Mult() | NT.Multi()):
                return (operand1 * operand2) % 2**32
            case (NT.Div() | NT.Divi()):
                return (operand1 // operand2) % 2**32
            case (NT.Mod() | NT.Modi()):
                return (operand1 % operand2) % 2**32
            case (NT.Oplus() | NT.Oplusi()):
                # signextension mit 0en
                return (operand1 ^ operand2) % 2**32
            case (NT.Or() | NT.Ori()):
                return (operand1 | operand2) % 2**32
            case (NT.And() | NT.Andi()):
                return (operand1 & operand2) % 2**32

    def _memory_store(self, destination, source, reti) -> int:
        match destination:
            # addressbus
            case NT.Num(val):
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
                        reti.eprom[((destination << 2) % 2**32) >> 2] = source
                    case 0b01:
                        reti.uart[((destination << 2) % 2**32) >> 2] = source
                    case _:
                        reti.sram[((destination << 2) % 2**32) >> 2] = source

    def _memory_load(self, source, reti) -> int:
        match source:
            # addressbus
            case NT.Num(val):
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
            case NT.Instr(
                operation,
                NT.Reg() as destination,
                (NT.Num() | NT.Reg()) as source,
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
            case NT.Instr(operation, NT.Reg() as destination, NT.Num(val)) if type(
                operation
            ) in COMPUTE_IMMEDIATE_INSTRUCTION.values():
                # TODO: Signextension? Bei Oplusi, Ori, Andi wird immer mit 0en signextendet
                self._memory_store(
                    destination,
                    self._op(self._memory_load(destination, reti), operation, int(val)),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Load(), NT.Reg() as destination, NT.Num() as source):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case NT.Instr(
                NT.Loadin(),
                NT.Reg() as reg_source,
                NT.Reg() as destination,
                NT.Num(val),
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
            case NT.Instr(NT.Loadi(), NT.Reg() as destination, NT.Num(val)):
                # TODO: Signextension?
                self._memory_store(
                    destination,
                    int(val),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Store(), NT.Reg() as source, NT.Num() as destination):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case NT.Instr(
                NT.Storein(),
                NT.Reg() as destination,
                NT.Reg() as reg_source,
                NT.Num(val),
            ):
                self._memory_store(
                    (abs(self._memory_load(destination, reti)) + int(val)) % 2**32,
                    self._memory_load(reg_source, reti),
                    reti,
                )
                reti.registers["PC"] += 1
            case NT.Instr(NT.Move(), NT.Reg() as source, NT.Reg() as destination):
                self._memory_store(destination, self._memory_load(source, reti), reti)
                reti.registers["PC"] += 1
            case NT.Jump(relation, NT.Num(val)):
                match relation:
                    case NT.Lt():
                        self._jump_condition(0 < reti.registers["ACC"], int(val), reti)
                    case NT.Lte():
                        self._jump_condition(0 <= reti.registers["ACC"], int(val), reti)
                    case NT.Gt():
                        self._jump_condition(0 > reti.registers["ACC"], int(val), reti)
                    case NT.Gte():
                        self._jump_condition(0 >= reti.registers["ACC"], int(val), reti)
                    case (NT.Eq()):
                        self._jump_condition(0 == reti.registers["ACC"], int(val), reti)
                    case (NT.Neq()):
                        self._jump_condition(0 != reti.registers["ACC"], int(val), reti)
                    case (NT.Always()):
                        self._jump_condition(True, int(val), reti)
                    case (NT.Nop()):
                        self._jump_condition(False, int(val), reti)
            case NT.Int(NT.Num(val)):
                # save PC to stack
                reti.sram[reti.registers["SP"]] = reti.registers["PC"]
                reti.registers["SP"] = reti.registers["SP"] - 1
                # jump to start address of isr
                reti.registers["PC"] = reti.sram[abs(int(val))]
            case NT.Rti():
                # restore PC
                reti.registers["PC"] = reti.sram[reti.registers["SP"] + 1]
                # delete PC from stack
                reti.registers["SP"] = reti.registers["SP"] + 1
            case NT.Call(NT.Name("PRINT")):
                if global_vars.args.print_output:
                    if global_vars.args.print:
                        print("\nOutput:\n\t" + str(reti.registers["ACC"]))
                    if global_vars.outbase:
                        if self.first_write_out:
                            with open(
                                global_vars.outbase + ".out", "w", encoding="utf-8"
                            ) as fout:
                                fout.write(str(reti.registers["ACC"]))
                            self.first_write_out = False
                        else:
                            with open(
                                global_vars.outbase + ".out", "a", encoding="utf-8"
                            ) as fout:
                                fout.write(" " + str(reti.registers["ACC"]))
                reti.registers["PC"] += 1
            case NT.Call(NT.Name("INPUT")):
                if global_vars.test_input:
                    reti.registers["ACC"] = global_vars.test_input.pop()
                else:
                    reti.registers["ACC"] = int(input())
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
            + len(p.instructions)
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

    def _instrs(self, p: NT.Program, reti):
        match p:
            case NT.Program(_, instructions):
                while True:
                    i = reti.registers["PC"] - global_vars.args.process_begin - 2**31
                    next_instruction = (
                        instructions[i] if i < len(instructions) and i >= 0 else None
                    )
                    if not next_instruction:
                        break
                        # raise Errors.JumpedOutOfProgrammError()
                    match next_instruction:
                        case NT.Jump(NT.Always(), NT.Num("0")):
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

    def interp_reti(self, p: NT.Program):
        # necessary for the __match_case__ of the nodes to work
        p.update_match_args()
        reti = RETI(p.instructions)
        self._preconfigs(p, reti)
        self._instrs(p, reti)
