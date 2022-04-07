#  from code_generator import CodeGenerator
import global_vars


class ASTNode:
    """Node of a Normalized Heterogeneous Abstract Syntax Tree (AST), partially
    also has some different Normalized Heterogeneous AST Nodes. A AST holds the
    relevant Tokens and represents grammatical relationships the parser came
    across.  Homogeneous AST means having only one node type and all childs
    normalized in a list. Normalized Heterogeneous means different Node types
    and all childs normalized in a list"""

    def __init__(self, value=None, position=None):
        """
        :tokentype: list of TT's, first entry will be the TT of the Node
        """
        self.children = []
        self.value = value
        self.position = position

    def update_match_args(self):
        pass

    __match_args__ = ("value", "position")

    def add_child(self, node):
        """
        :returns: None
        """
        self.children += [node]

    def __repr__(self):
        #  global_vars.show_node = True
        return self.to_string()

    def to_string(self):
        if not self.children:
            if not self.value and global_vars.args.verbose:
                return self.__class__.__name__
            return f"{self.value}"

        acc = ""

        #  if global_vars.args.verbose and global_vars.show_node:
        #      acc += self.__class__.__name__

        acc += f"({self.children[0]}"

        for child in self.children[1:]:
            acc += f" {child}"

        return acc + ")"

    def alternative_to_string(self):
        #  global_vars.show_node = False
        tmp = self.to_string()
        #  global_vars.show_node = True
        return tmp


def strip_multiline_string(mutline_string):
    """helper function to make mutlineline string usable on different
    indent levels

    :grammar: grammar specification
    :returns: None
    """
    mutline_string = "".join(
        [i.lstrip() + "\n" for i in mutline_string.split("\n")[:-1]]
    )
    # every code piece ends with \n, so the last element can always be poped
    return mutline_string
