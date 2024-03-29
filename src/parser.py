from errors import Errors
from ast_builder import ASTBuilder


class LL_Recursive_Decent_Parser:
    """Analyzes the syntactic structure of a token sequence generated by the
    Lexer using  k>1 lookahead tokens
    """

    def __init__(self, lexer, num_lts):
        """
        :lts: lookahead tokens
        :num_lts: number of lookahead tokens
        :lt_idx: lookahead token index

        """
        self.lexer = lexer
        self.num_lts = num_lts
        self.lts = [0] * self.num_lts
        self.lt_idx = 0
        for _ in range(self.num_lts):
            self.consume_next_token()
        self.ast_builder = ASTBuilder()

    def consume_next_token(self):
        """fills next position in the lookahead tokenlist with token

        :returns: None
        """
        self.lts[self.lt_idx] = self.lexer.next_token()
        self.lt_idx = (self.lt_idx + 1) % self.num_lts

    def LT(self, i):
        """Lookahead Token

        :returns: find out token looking ahead i tokens
        """
        return self.lts[(self.lt_idx + i - 1) % self.num_lts]

    def LTT(self, i):
        """Lookahead tokentype

        :returns: find out type locking ahead i tokens
        """
        return self.LT(i).type

    def match(self, tokentypes):
        """Check if one of the token are the next token in the lexer to match. In
        general checks if non-terminal symbols are at the right syntactial
        position

        :tokentypes: list of tokentypes
        """
        if self.LTT(1) in tokentypes:
            self.consume_next_token()
        else:
            token = self.LT(1)
            raise Errors.MismatchedTokenError(
                " or ".join(tokentype.value for tokentype in tokentypes),
                token.value,
                token.position,
            )

    def add_and_match(self, tokentypes, classname=None, mapping=None):
        """Same as add, but also check for match

        :tokentypes: list of tokentypes
        :classname: what kind of nodetype should be added
        :mapping: dictionray from which the right nodetype gets determined by
        the LTT
        """
        self._add(classname, mapping)
        self.match(tokentypes)

    def add_and_consume(self, classname=None, mapping=None):
        self._add(classname, mapping)
        self.consume_next_token()

    def _add(self, classname=None, mapping=None):
        """Add the node with the given classname if given or else right
        nodetype matching the tokentype of the current token and with the right
        tokenvalue to the ast

        :classname: nodetype
        :mapping: see docstring of add_and_match
        """
        if not classname:
            classname = mapping.get(self.LTT(1))
            # leave it to the match function to throw the error
            if not classname:
                return
        self.ast_builder.CN().add_child(
            classname(self.LT(1).value, self.LT(1).position)
        )
