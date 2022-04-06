from errors import Errors
from enum import Enum
import string
import global_vars


class Token:
    """Identifies what a certiain string slice is"""

    __match_args__ = ("type", "value")

    def __init__(self, tokentype, value, position):
        """
        :type: TT
        :value: string
        :position: (row, column) in the file where the token starts
        """
        self.type = tokentype
        self.value = value
        self.position = position

    def __repr__(self):
        if global_vars.args.verbose:
            return f"<{self.type},'{self.value}',{self.position}>"
        return f"'{self.value}'"


class TT(Enum):
    """Tokentypes that are part of the grammar. Their strings are used for
    differentiation and for error messages"""

    ADD = "ADD"
    ADDI = "ADDI"
    SUB = "SUB"
    SUBI = "SUBI"
    MULT = "MULT"
    MULTI = "MULTI"
    DIV = "DIV"
    DIVI = "DIVI"
    MOD = "MOD"
    MODI = "MODI"
    OPLUS = "OPLUS"
    OPLUSI = "OPLUSI"
    OR = "OR"
    ORI = "ORI"
    AND = "AND"
    ANDI = "ANDI"
    LOAD = "LOAD"
    LOADIN = "LOADIN"
    LOADI = "LOADI"
    STORE = "STORE"
    STOREIN = "STOREIN"
    MOVE = "MOVE"
    JUMP = "JUMP"
    INT = "INT"
    RTI = "RETI"
    ACC = "ACC"
    IN1 = "IN1"
    IN2 = "IN2"
    PC = "PC"
    SP = "SP"
    BAF = "BAF"
    CS = "CS"
    DS = "DS"
    IMMEDIATE = "immediate"
    MINUS = "-"
    SEMICOLON = ";"


class Lexer:
    """Identifies tokens in the picoC code

    :Info: The Lexer doesn't check if the token is also at the right position
    to follow the grammar rules (that's the task of the parser). That's why
    12ab will be split into a number an identifier Token and it's the task of
    the Parser to raise an error. That's also the reason why self.next_char()
    is used instead of self.match()
    """

    EOF_CHAR = "EOF"
    DIGIT_WITHOUT_ZERO = "123456789"
    DIGIT_WITH_ZERO = "0123456789"
    LETTER = string.ascii_letters

    NOT_TO_MAP = ("immediate", )
    REGISTERS = ("ACC", "IN1", "IN2", "SP", "BAF", "CS", "DS")

    STRING_TO_TT_REGISTER = {
        value.value: value
        for value in (
            value
            for key, value in TT.__dict__.items()
            if not key.startswith("_")
            and value.value[0] in REGISTERS
    }

    STRING_TO_TT_INSTRUCTIONS = {
        value.value: value
        for value in (
            value
            for key, value in TT.__dict__.items()
            if not key.startswith("_")
            and value.value[0] not in REGISTERS + NOT_TO_MAP
        )
    }

    def __init__(self, finput):
        """
        :lc: lookahead character
        :c: character
        """
        self.finput = finput
        self.lc_col = 0
        self.lc_row = 0
        self.lc = finput[self.lc_row][self.lc_col]
        self.c = ""
        # position variable to be available between methods
        self.position = (0, 0)

    def next_token(self):
        """identifies the next Token in the picoC code

        :returns: Token
        """
        while self.lc != self.EOF_CHAR:
            self.position = (self.lc_row, self.lc_col)
            if self.lc in " \t":
                self.next_char()
            elif self.lc in self.LETTER:
                # identifier or special keyword symbol
                # :grammar: <identifier>|if|else|while|do|int|char
                # |void|const|main
                # :identifier: <letter> <letter_digit>*
                self.next_char()
                symbol = self.c
                while self.lc in self.LETTER:
                    self.next_char()
                    symbol += self.c
                if self.STRING_TO_TT_REGISTER.get(symbol):
                    return Token(
                        self.STRING_TO_TT_REGISTER[symbol], symbol, self.position
                    )
                return Token(TT.IDENTIFIER, symbol, self.position)
            elif self.lc in self.DIGIT_WITH_ZERO:
                # number
                # :grammar: 0|(<digit_without_zero><digit_with_zero>*)
                if self.lc == 0:
                    self.next_char()
                    return Token(TT.IMMEDIATE, self.c, self.position)
                # else: self.lc in self.DIGIT_WITHOUT_ZERO:
                self.next_char()
                symbol = self.c
                while self.lc in self.DIGIT_WITH_ZERO:
                    self.next_char()
                    symbol += self.c
                return Token(TT.IMMEDIATE, symbol, self.position)
            else:
                raise Errors.InvalidCharacterError(self.lc, self.position)
        return Token(TT.EOF, self.lc, self.position)

    def next_char(self):
        """go to the next character, detect if "end of file" is reached

        :returns: None
        """
        # next column or next row
        if self.lc_col < len(self.finput[self.lc_row]) - 1:
            self.lc_col += 1
        elif (
            self.lc_col == len(self.finput[self.lc_row]) - 1
            and self.lc_row < len(self.finput) - 1
        ):
            self.lc_row += 1
            self.lc_col = 0
        elif (
            self.lc_col == len(self.finput[self.lc_row]) - 1
            and self.lc_row == len(self.finput)
        ) - 1:
            self.lc_col += 1

        # next character
        self.c = self.lc
        if (
            self.lc_col == len(self.finput[self.lc_row])
            and self.lc_row == len(self.finput) - 1
        ):
            self.lc = self.EOF_CHAR
        else:
            self.lc = self.finput[self.lc_row][self.lc_col]

    def __repr__(
        self,
    ):
        return str(self.finput)
