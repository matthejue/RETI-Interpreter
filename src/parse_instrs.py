from reti_nodes import NT
from lexer import TT
from errors import Errors
from parser import LL_Recursive_Decent_Parser
from itertools import chain


COMPUTE_INSTRUCTION = {
    TT.ADD: NT.Add,
    TT.SUB: NT.Sub,
    TT.MULT: NT.Mult,
    TT.DIV: NT.Div,
    TT.MOD: NT.Mod,
    TT.OPLUS: NT.Oplus,
    TT.OR: NT.Or,
    TT.AND: NT.And,
}

COMPUTE_IMMEDIATE_INSTRUCTION = {
    TT.ADDI: NT.Addi,
    TT.SUBI: NT.Subi,
    TT.MULTI: NT.Multi,
    TT.DIVI: NT.Divi,
    TT.MODI: NT.Modi,
    TT.OPLUSI: NT.Oplusi,
    TT.ORI: NT.Ori,
    TT.ANDI: NT.Andi,
}

RELATION = {
    TT.LT: NT.Lt,
    TT.LTE: NT.Lte,
    TT.GT: NT.Gt,
    TT.GTE: NT.Gte,
    TT.EQ: NT.Eq,
    TT.EQ2: NT.Eq,
    TT.NEQ: NT.Neq,
    TT.NEQ2: NT.Neq,
    TT.NOP: NT.Nop,
}

OTHER_INSTRUCTION = {
    TT.LOAD,
    TT.LOADIN,
    TT.LOADI,
    TT.STORE,
    TT.STOREIN,
    TT.MOVE,
    TT.JUMP,
    TT.INT,
    TT.RTI,
    TT.CALL,
}


class InstrsParser(LL_Recursive_Decent_Parser):
    def _instr(self):
        """instruction"""
        if self.LTT(1) in COMPUTE_INSTRUCTION.keys():
            # concrete_syntax: <COMPUTE_INSTRUCTION> <REGISTER> (<REGISTER>|<Immediate>)
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(mapping=COMPUTE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=NT.Reg)

            if self.LTT(1) == TT.REG:
                self.add_and_consume(classname=NT.Reg)
            elif self.LTT(1) == TT.IMMEDIATE:
                self.add_and_consume(classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) in COMPUTE_IMMEDIATE_INSTRUCTION.keys():
            # concrete_syntax: <COMPUTE_IMMEDIATE_INSTRUCTION> <REGISTER> <Immediate>
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(mapping=COMPUTE_IMMEDIATE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOAD:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Load)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADIN:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Loadin)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADI:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Loadi)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STORE:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Store)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STOREIN:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Storein)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.MOVE:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Move)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.JUMP:
            savestate_node = self.ast_builder.down(NT.Jump)

            self.consume_next_token()

            if self.LTT(1) in RELATION.keys():
                self.add_and_consume(mapping=RELATION)
            else:
                savestate_node = self.ast_builder.down(NT.Always)
                self.ast_builder.up(savestate_node)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.INT:
            savestate_node = self.ast_builder.down(NT.Int)

            self.consume_next_token()

            self.add_and_match([TT.IMMEDIATE], classname=NT.Num)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.RTI:
            self.add_and_consume(classname=NT.Rti)

            self.match([TT.SEMICOLON])
        elif self.LTT(1) == TT.CALL:
            savestate_node = self.ast_builder.down(NT.Call)

            self.consume_next_token()

            self.add_and_match([TT.NAME], classname=NT.Name)

            self.match([TT.SEMICOLON])

            self.ast_builder.up(savestate_node)
        else:
            # error
            pass

    def _instrs(self):
        savestate_node = self.ast_builder.down(NT.Program)

        self.add_and_match([TT.NAME], classname=NT.Name)

        while self.LTT(1) in chain(
            COMPUTE_INSTRUCTION.keys(),
            COMPUTE_IMMEDIATE_INSTRUCTION.keys(),
            OTHER_INSTRUCTION,
        ):
            self._instr()

        self.ast_builder.up(savestate_node)

    def parse_instrs(self):
        self._instrs()
