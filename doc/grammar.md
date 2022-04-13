# L_X86
## Concrete Syntax
###
## Abstract Syntax
### L_RETI
```
reg := Reg() |
arg := reg | Num(val)
rel := Eq() | NEq() | Lt() | LtE() | Gt() | GtE() | Always() | NOp()
op := Add() | Addi() | Sub() | Subi() | Mult() | Multi() | Div() | Divi() | Mod() | Modi() | Oplus() | Oplusi() | And() | Andi() | Or() | Ori()
op := Load() | Loadin() | Loadi() | Store() | Storein() | Move()
instr := Instr(op, arg+), Jump(rel, Num(val)), Int(Num(val)), RTI(), Call(Name('print'), reg), Call(Name('input'), reg)
L\_RETI := Program(Name(str), instr*)
```
