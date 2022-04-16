from reti_nodes import N
from lexer import TT
from errors import Errors
from parser import LL_Recursive_Decent_Parser
from itertools import chain


COMPUTE_INSTRUCTION = {
    TT.ADD: N.Add,
    TT.SUB: N.Sub,
    TT.MULT: N.Mult,
    TT.DIV: N.Div,
    TT.MOD: N.Mod,
    TT.OPLUS: N.Oplus,
    TT.OR: N.Or,
    TT.AND: N.And,
}

COMPUTE_IMMEDIATE_INSTRUCTION = {
    TT.ADDI: N.Addi,
    TT.SUBI: N.Subi,
    TT.MULTI: N.Multi,
    TT.DIVI: N.Divi,
    TT.MODI: N.Modi,
    TT.OPLUSI: N.Oplusi,
    TT.ORI: N.Ori,
    TT.ANDI: N.Andi,
}

RELATION = {
    TT.LT: N.Lt,
    TT.LTE: N.LtE,
    TT.GT: N.Gt,
    TT.GTE: N.GtE,
    TT.EQ: N.Eq,
    TT.EQ2: N.Eq,
    TT.NEQ: N.NEq,
    TT.NEQ2: N.NEq,
    TT.NOP: N.NOp,
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
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(mapping=COMPUTE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=N.Reg)

            if self.LTT(1) == TT.REG:
                self.add_and_consume(classname=N.Reg)
            elif self.LTT(1) == TT.IMMEDIATE:
                self.add_and_consume(classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) in COMPUTE_IMMEDIATE_INSTRUCTION.keys():
            # concrete_syntax: <COMPUTE_IMMEDIATE_INSTRUCTION> <REGISTER> <Immediate>
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(mapping=COMPUTE_IMMEDIATE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOAD:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Load)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADIN:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Loadin)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADI:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Loadi)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STORE:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Store)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STOREIN:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Storein)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.MOVE:
            savestate_node = self.ast_builder.down(N.Instr)

            self.add_and_consume(classname=N.Move)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.JUMP:
            savestate_node = self.ast_builder.down(N.Jump)

            self.consume_next_token()

            if self.LTT(1) in RELATION.keys():
                self.add_and_consume(mapping=RELATION)
            else:
                savestate_node = self.ast_builder.down(N.Always)
                self.ast_builder.up(savestate_node)

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.INT:
            savestate_node = self.ast_builder.down(N.Int)

            self.consume_next_token()

            self.add_and_match([TT.IMMEDIATE], classname=N.Num)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.RTI:
            self.add_and_consume(classname=N.Rti)
        elif self.LTT(1) == TT.CALL:
            savestate_node = self.ast_builder.down(N.Call)

            self.consume_next_token()

            self.add_and_match([TT.NAME], classname=N.Name)

            self.add_and_match([TT.REG], classname=N.Reg)

            self.ast_builder.up(savestate_node)
        else:
            # error
            pass

    def _instrs(self):
        savestate_node = self.ast_builder.down(N.Program)

        self.add_and_match([TT.NAME], classname=N.Name)

        while self.LTT(1) in chain(
            COMPUTE_INSTRUCTION.keys(),
            COMPUTE_IMMEDIATE_INSTRUCTION.keys(),
            OTHER_INSTRUCTION,
        ):
            self._instr()
            self.match([TT.SEMICOLON])

        self.ast_builder.up(savestate_node)

    def parse_instrs(self):
        self._instrs()
