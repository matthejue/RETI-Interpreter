from colormanager import ColorManager as CM


class Errors:
    class InvalidCharacterError(Exception):
        """If there're Token sequences generated from the input that are not
        permitted by the grammar rules"""

        def __init__(self, found, found_pos):
            self.description = (
                f"{CM().YELLOW}InvalidCharacterError{CM().RESET}: '{found}' is not a "
                "permitted character"
            )
            self.found = found
            self.found_pos = found_pos

    class UnclosedCharacterError(Exception):
        """If a character has a opening apostrophe but not a closing one"""

        def __init__(self, expected, found, found_pos):
            self.description = (
                f"{CM().YELLOW}UnclosedCharacterError{CM().RESET}: Expected {expected},"
                f" found {found}"
            )
            self.expected = expected
            self.found = found
            self.found_pos = found_pos

    class InvalidWordError(Exception):
        """If there's a word that is neither a instruction, nor a register name"""

        def __init__(self, found, found_pos):
            self.description = (
                f"{CM().YELLOW}InvalidWordError{CM().RESET}: '{found}' is neither "
                f"a instruction name, nor a register name"
            )
            self.found = found
            self.found_pos = found_pos

    class InvalidInstructionError(Exception):
        """If there's a word that is neither a instruction, nor a register name"""

        def __init__(self, found, found_pos):
            self.description = (
                f"{CM().YELLOW}InvalidWordError{CM().RESET}: '{found}' is a "
                f"not currectly composed instruction"
            )
            self.found = found
            self.found_pos = found_pos

    class InvalidNumberError(Exception):
        """If a character has a opening apostrophe but not a closing one"""

        def __init__(self, expected, found, found_pos):
            self.description = (
                f"{CM().YELLOW}InvalidNumberError{CM().RESET}: Expected {expected},"
                f" found {found}"
            )
            self.expected = expected
            self.found = found
            self.found_pos = found_pos

    class NoApplicableRuleError(Exception):
        """If no rule is applicable in a situation where several undistinguishable
        alternatives are possible"""

        def __init__(self, expected, found, found_pos):
            self.description = (
                f"{CM().YELLOW}NoApplicableRuleError{CM().RESET}: Expected '{expected}'"
                f", found '{found}'"
            )
            self.expected = expected
            self.found = found
            self.found_pos = found_pos

    class MismatchedTokenError(Exception):
        """If Token shouldn't syntactically appear at this position"""

        def __init__(self, expected, found, found_pos):
            # there can be several expected and these already have single quotes
            self.description = (
                f"{CM().YELLOW}MismatchedTokenError{CM().RESET}: Expected '{expected}'"
                f", found '{found}'"
            )
            self.expected = expected
            self.found = found
            self.found_pos = found_pos

    class TooLargeLiteralError(Exception):
        """If the literal assigned to a variable is too large for the datatype of
        the variable"""

        def __init__(self, found, found_pos, found_symbol_type, found_from, found_to):
            self.description = f"{CM().YELLOW}TooLargeLiteralError{CM().RESET}: Literal '{found}' is too large"
            self.found = found
            self.found_pos = found_pos
            self.found_symbol_type = found_symbol_type
            self.found_from = found_from
            self.found_to = found_to

    class JumpedOutOfProgramError(Exception):
        """If the PC Register points outside of any instruction of the program,
        probably because a 'JUMP 0' was forgotten to terminate execution"""

        def __init__(self, found, found_pos, found_symbol_type, found_from, found_to):
            self.description = f"{CM().YELLOW}JumpedOutOfProgramError{CM().RESET}: Literal '{found}' is too large"
            self.found = found
            self.found_pos = found_pos
            self.found_symbol_type = found_symbol_type
            self.found_from = found_from
            self.found_to = found_to
