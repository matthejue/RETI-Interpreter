from abstract_syntax_tree import ASTNode


class NT:
    class Program(ASTNode):
        def update_match_args(self):
            self.instructions = self.children
            for instr in self.instructions:
                instr.update_match_args()

        __match_args__ = ("instructions",)

        def __repr__(self):
            return self.alternative_to_string()

    class Instr(ASTNode):
        def update_match_args(self):
            self.instruction = self.children[0]
            self.argument1 = self.children[1]
            self.argument2 = self.children[2]
            if len(self.children) == 4:
                self.argument3 = self.children[3]

        __match_args__ = (
            "instruction",
            "argument1",
            "argument2",
            "argument3",
        )

        def __repr__(self):
            return self.alternative_to_string()

    class Add(ASTNode):
        pass

    class Addi(ASTNode):
        pass

    class Sub(ASTNode):
        pass

    class Subi(ASTNode):
        pass

    class Mult(ASTNode):
        pass

    class Multi(ASTNode):
        pass

    class Div(ASTNode):
        pass

    class Divi(ASTNode):
        pass

    class Mod(ASTNode):
        pass

    class Modi(ASTNode):
        pass

    class Oplus(ASTNode):
        pass

    class Oplusi(ASTNode):
        pass

    class Or(ASTNode):
        pass

    class Ori(ASTNode):
        pass

    class And(ASTNode):
        pass

    class Andi(ASTNode):
        pass

    class Load(ASTNode):
        pass

    class Loadin(ASTNode):
        pass

    class Loadi(ASTNode):
        pass

    class Store(ASTNode):
        pass

    class Storein(ASTNode):
        pass

    class Move(ASTNode):
        pass

    class Print(ASTNode):
        pass

    class Input(ASTNode):
        pass

    class Jump(ASTNode):
        def update_match_args(self):
            self.relation = self.children[0]
            self.jumplenght = self.children[1]

        __match_args__ = ("relation", "jumplength")

    class NOP(ASTNode):
        pass

    class LT(ASTNode):
        pass

    class LTE(ASTNode):
        pass

    class GT(ASTNode):
        pass

    class GTE(ASTNode):
        pass

    class EQ(ASTNode):
        pass

    class EQ2(ASTNode):
        pass

    class NEQ(ASTNode):
        pass

    class NEQ2(ASTNode):
        pass

    class Int(ASTNode):
        def update_match_args(self):
            self.isr = self.children[0]

        __match_args__ = ("isr",)

    class Rti(ASTNode):
        pass

    class Call(ASTNode):
        def update_match_args(self):
            self.functionname = self.children[0]
            self.argument = self.children[1]

        __match_args__ = (
            "functionname",
            "argument",
        )

    class Reg(ASTNode):
        pass

    class Immediate(ASTNode):
        pass
