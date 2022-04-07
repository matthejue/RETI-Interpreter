from abstract_syntax_tree import ASTNode


class NT:
    class Program(ASTNode):
        __match_args__ = ("children",)

    class Instr(ASTNode):
        __match_args__ = (
            "children[0]",
            "children[1]",
            "children[2]",
            "children[3]",
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

    class Acc(ASTNode):
        pass

    class In1(ASTNode):
        pass

    class In2(ASTNode):
        pass

    class Pc(ASTNode):
        pass

    class Sp(ASTNode):
        pass

    class Baf(ASTNode):
        pass

    class Cs(ASTNode):
        pass

    class Ds(ASTNode):
        pass

    class Print(ASTNode):
        pass

    class Input(ASTNode):
        pass

    class Jump(ASTNode):
        __match_args__ = ("children[0]", "children[1]")

    class Int(ASTNode):

        __match_args__ = ("children[0]",)

    class Rti(ASTNode):
        pass

    class Call(ASTNode):

        __match_args__ = (
            "children[0]",
            "children[1]",
        )

    class Reg(ASTNode):
        pass

    class Immediate(ASTNode):
        pass
