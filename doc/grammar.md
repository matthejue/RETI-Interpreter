# L_x86
## Concrete Syntax
### L_RETI
```
dig_no_0 := 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
dig_with_0 := 0 | <dig_no_0>
num := 0 | <dig_no_0><dig_with_0>* | -<dig_with_0>*
letter := a | b | ... | y | z | A | B | ... | Y | Z
name := <letter>[<letter> | <dig_with_0> | _]*
---------------------------------------------------------------------------
reg := ACC | IN1 | IN2 | PC | SP | BAF | CS | DS
arg := <reg> | <num>
rel := == | = | != | <> | < | <= | > | >= | _NOP
instr := ADD <reg> <arg> | ADDI <reg> <num> | SUB <reg> <arg> | SUBI <reg> <num> | MULT <reg> <arg> | MULTI <reg> <num> | DIV <reg> <arg> | DIVI <reg <num>> | MOD <reg <arg>> | MODI <reg> <num> | OPLUS <reg> <arg> | OPLUSI <reg> <num> | OR <reg> <arg> | ORI <reg> <num> | AND <reg> <arg> | ANDI <reg> <num>
instr := LOAD <reg> <num> | LOADIN <arg> <arg> <num> | LOADI <reg> <num>
instr := STORE <reg> <num> | STOREIN <arg> <arg> <num> | MOVE <reg> <reg>
instr := JUMP<rel> <num> | INT <num> | RTI
instr := CALL INPUT <reg> | CALL PRINT <reg>
L\_RETI := <name> [<instr>;]*
```
## Abstract Syntax
### L_RETI
```
reg := Reg('ACC') | Reg('IN1') | Reg('IN2') | Reg('PC') | Reg('SP') | Reg('BAF') | Reg('CS') | Reg('DS')
arg := <reg> | Num(val)
rel := Eq() | NEq() | Lt() | LtE() | Gt() | GtE() | Always() | NOp()
op := Add() | Addi() | Sub() | Subi() | Mult() | Multi() | Div() | Divi() | Mod() | Modi() | Oplus() | Oplusi() | Or() | Ori() | And() | Andi()
op := Load() | Loadin() | Loadi()
op := Store() | Storein() | Move()
instr := Instr(<op>, <arg>+), Jump(<rel>, Num(val)), Int(Num(val)), RTI(), Call(Name('print'), <reg>), Call(Name('input'), <reg>)
L\_RETI := Program(Name(str), <instr>*)
```
