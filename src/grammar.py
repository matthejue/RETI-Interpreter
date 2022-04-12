from parse_reti import InstructionGrammar
from lexer import TT


class Grammar(InstructionGrammar):
    def __init__(self, lexer):
        super().__init__(lexer, 1)

        # to check for the MoreThanOneMainFunctionError
        self.mains = []

    def start_parse(self):
        """start parsing the grammar

        :returns: None
        """
        self.parse_program()
        self.match([TT.EOF])

    def reveal_ast(self):
        """makes the abstract syntax tree of the grammar available

        :returns: rootnode of the abstract syntax tree
        """
        return self.ast_builder.root

    def __repr__(self):
        return str(self.ast_builder)
