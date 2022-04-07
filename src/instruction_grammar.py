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

    OTHER_INSTRUCTION = [
        TT.LOAD,
        TT.LOADIN,
        TT.LOADI,
        TT.STORE,
        TT.STOREIN,
        TT.MOVE,
    ]

    def code_instr(self):
        savestate_node = self.ast_builder.down(NT.Program)

        self._instr()

        self.ast_builder.up(savestate_node)

    def _instr(self):
        """instruction

        :concrete:
        :abstract: abstract grammar specification
        """
        while self.LTT(1) in chain(
            self.COMPUTE_INSTRUCTION.keys(),
            self.COMPUTE_IMMEDIATE_INSTRUCTION.keys(),
            self.OTHER_INSTRUCTION,
        ):
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
            elif self.LTT(1) == TT.JUMP:
                savestate_node = self.ast_builder.down(NT.Jump)

                self.add_and_match([TT.IMMEDIATE], classname=NT.Immediate)

                self.ast_builder.up(savestate_node)
