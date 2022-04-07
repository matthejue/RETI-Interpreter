from reti_ast import NT
from lexer import TT
from errors import Errors
from parser import LL_Recursive_Decent_Parser
from itertools import chain


class InstructionGrammar(LL_Recursive_Decent_Parser):

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
        TT.LT: NT.LT,
        TT.LTE: NT.LTE,
        TT.GT: NT.GT,
        TT.GTE: NT.GTE,
        TT.EQ: NT.EQ,
        TT.EQ2: NT.EQ2,
        TT.NEQ: NT.NEQ,
        TT.NEQ2: NT.NEQ2,
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
    }

    def code_instr(self):
        savestate_node = self.ast_builder.down(NT.Program)

        while self.LTT(1) in chain(
            self.COMPUTE_INSTRUCTION.keys(),
            self.COMPUTE_IMMEDIATE_INSTRUCTION.keys(),
            self.OTHER_INSTRUCTION,
        ):
            self._instr()

        self.ast_builder.up(savestate_node)

    def _instr(self):
        """instruction

        :concrete:
        :abstract: abstract grammar specification
        """
        if self.LTT(1) in self.COMPUTE_INSTRUCTION.keys():
            # concrete_syntax: <COMPUTE_INSTRUCTION> <REGISTER> (<REGISTER>|<Immediate>)
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(mapping=self.COMPUTE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=NT.Reg)

            if self.LTT(1) == TT.REG:
                self.add_and_consume(classname=NT.Reg)
            elif self.LTT(1) == TT.IMMEDIATE:
                self.add_and_consume(classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) in self.COMPUTE_IMMEDIATE_INSTRUCTION.keys():
            # concrete_syntax: <COMPUTE_IMMEDIATE_INSTRUCTION> <REGISTER> <Immediate>
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(mapping=self.COMPUTE_IMMEDIATE_INSTRUCTION)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOAD:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Load)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADIN:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Loadin)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.LOADI:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Loadi)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STORE:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Store)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.STOREIN:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Storein)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.MOVE:
            savestate_node = self.ast_builder.down(NT.Instr)

            self.add_and_consume(classname=NT.Move)

            self.add_and_match([TT.REG], classname=NT.Reg)

            self.add_and_match([TT.REG], classname=NT.Reg)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.JUMP:
            savestate_node = self.ast_builder.down(NT.Jump)

            self.consume_next_token()

            if self.LTT(1) in self.RELATION.keys():
                self.add_and_consume(mapping=self.RELATION)
            else:
                self.add(classname=NT.NOP)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            if self.LTT(1) == TT.SEMICOLON:
                self.consume_next_token()

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.INT:
            savestate_node = self.ast_builder.down(NT.Int)

            self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

            self.ast_builder.up(savestate_node)
        elif self.LTT(1) == TT.RTI:
            self.add_and_consume(classname=NT.Rti)
        else:
            # error
            pass
