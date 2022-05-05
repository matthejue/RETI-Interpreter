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
            self.instrs = self.children[1:]
            for instr in self.instrs:
                instr.update_match_args()

        __match_args__ = (
            "programname",
            "instrs",
        )

    # ------------------------- Load / Store / Compute ------------------------
    class Instr(ASTNode):
        def update_match_args(self):
            self.instr = self.children[0]
            self.arg1 = self.children[1]
            self.arg2 = self.children[2]
            if len(self.children) == 4:
                self.arg3 = self.children[3]
            self.arg1.update_match_args()
            self.arg2.update_match_args()

        __match_args__ = (
            "instr",
            "arg1",
            "arg2",
            "arg3",
        )

    # --------------------------- Jump Instructions ---------------------------
    class Jump(ASTNode):
        def update_match_args(self):
            self.rel = self.children[0]
            self.offset = self.children[1]

        def __repr__(self):
            return self.to_string_show_node()

        __match_args__ = ("rel", "offset")

    class Int(ASTNode):
        def update_match_args(self):
            self.isr = self.children[0]

        def __repr__(self):
            return self.to_string_show_node()

        __match_args__ = ("isr",)

    # ---------------------------- Input and Print ----------------------------
    class Call(ASTNode):
        def update_match_args(self):
            self.procedurename = self.children[0]
            self.reg = self.children[1]
            self.reg.update_match_args()

        def __repr__(self):
            return self.to_string_show_node()

        __match_args__ = ("procedurename", "reg")

    # ------------------------- Location and Immediate ------------------------
    class Reg(ASTNode):
        def update_match_args(self):
            self.reg = self.children[0]

        def __repr__(self):
            return self.to_string_show_node()

        __match_args__ = ("reg",)

    # -------------------------------------------------------------------------
    # -                              Token Nodes                              -
    # -------------------------------------------------------------------------
    # ------------------------- Location and Immediate ------------------------
    class Name(ASTNode):
        # shorter then 'Identifier'
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

    # ------------------------------- Registers -------------------------------
    class Acc(ASTNode):
        pass

    class In1(ASTNode):
        pass

    class In2(ASTNode):
        pass

    class Sp(ASTNode):
        pass

    class Baf(ASTNode):
        pass

    class Cs(ASTNode):
        pass

    class Ds(ASTNode):
        pass
