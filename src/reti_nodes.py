from ast_node import ASTNode


class NT:
    class Program(ASTNode):
        def update_match_args(self):
            self.programname = self.children[0]
            self.instructions = self.children[1:]
            for instr in self.instructions:
                instr.update_match_args()

        __match_args__ = (
            "programname",
            "instructions",
        )

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

    class Jump(ASTNode):
        def update_match_args(self):
            self.relation = self.children[0]
            self.jumplength = self.children[1]

        __match_args__ = ("relation", "jumplength")

        def __repr__(self):
            return self.to_string_show_node()

    class Lt(ASTNode):
        pass

    class Lte(ASTNode):
        pass

    class Gt(ASTNode):
        pass

    class Gte(ASTNode):
        pass

    class Eq(ASTNode):
        pass

    class Neq(ASTNode):
        pass

    class Always(ASTNode):
        pass

    class Nop(ASTNode):
        pass

    class Int(ASTNode):
        def update_match_args(self):
            self.isr = self.children[0]

        __match_args__ = ("isr",)

        def __repr__(self):
            return self.to_string_show_node()

    class Rti(ASTNode):
        pass

    class Call(ASTNode):
        def update_match_args(self):
            self.functionname = self.children[0]

        __match_args__ = ("functionname",)

        def __repr__(self):
            return self.to_string_show_node()

    class Identifier(ASTNode):
        pass

    class Reg(ASTNode):
        pass

    class Immediate(ASTNode):
        pass
