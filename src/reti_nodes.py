from ast_node import ASTNode


class N:
    """Nodes"""

    # -------------------------------------------------------------------------
    # -                            Container Nodes                            -
    # -------------------------------------------------------------------------
    # -------------------------------- Program --------------------------------
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

    # ------------------------- Load / Store / Compute ------------------------
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

    # --------------------------- Jump Instructions ---------------------------
    class Jump(ASTNode):
        def update_match_args(self):
            self.relation = self.children[0]
            self.offset = self.children[1]

        __match_args__ = ("relation", "offset")

        def __repr__(self):
            return self.to_string_show_node()

    class Int(ASTNode):
        def update_match_args(self):
            self.isr = self.children[0]

        __match_args__ = ("isr",)

        def __repr__(self):
            return self.to_string_show_node()

    # ---------------------------- Input and Print ----------------------------
    class Call(ASTNode):
        def update_match_args(self):
            self.procedurename = self.children[0]
            self.reg = self.children[1]

        __match_args__ = ("procedurename", "reg")

        def __repr__(self):
            return self.to_string_show_node()

    # -------------------------------------------------------------------------
    # -                              Token Nodes                              -
    # -------------------------------------------------------------------------
    # ------------------------- Location and Immediate ------------------------
    class Name(ASTNode):
        # shorter then 'Identifier'
        pass

    class Reg(ASTNode):
        pass

    class Num(ASTNode):
        # shorter then 'Immediate'
        pass

    # ----------------------- Compute Memory / Register -----------------------
    class Add(ASTNode):
        pass

    class Sub(ASTNode):
        pass

    class Mult(ASTNode):
        pass

    class Div(ASTNode):
        pass

    class Mod(ASTNode):
        pass

    class Oplus(ASTNode):
        pass

    class Or(ASTNode):
        pass

    class And(ASTNode):
        pass

    # --------------------- Compute Immediate Instructions --------------------
    class Addi(ASTNode):
        pass

    class Subi(ASTNode):
        pass

    class Multi(ASTNode):
        pass

    class Divi(ASTNode):
        pass

    class Modi(ASTNode):
        pass

    class Oplusi(ASTNode):
        pass

    class Ori(ASTNode):
        pass

    class Andi(ASTNode):
        pass

    # --------------------------- Load Instructions ---------------------------
    class Load(ASTNode):
        pass

    class Loadin(ASTNode):
        pass

    class Loadi(ASTNode):
        pass

    # --------------------------- Store Instructions --------------------------
    class Store(ASTNode):
        pass

    class Storein(ASTNode):
        pass

    class Move(ASTNode):
        pass

    # ------------------------------- Relations -------------------------------
    class Lt(ASTNode):
        pass

    class LtE(ASTNode):
        pass

    class Gt(ASTNode):
        pass

    class GtE(ASTNode):
        pass

    class Eq(ASTNode):
        pass

    class NEq(ASTNode):
        pass

    class Always(ASTNode):
        pass

    class NOp(ASTNode):
        pass

    # --------------------------- Jump Instructions ---------------------------
    class Rti(ASTNode):
        pass
