class Args:
    def __init__(self):
        self.infile = "stdin"
        self.concrete_syntax = True
        self.tokens = True
        self.abstract_syntax = True
        self.print_output = True
        self.reti_state = True
        self.print = True
        self.process_begin = 8
        self.datasegment_size = 32
        self.distance = 20
        self.sight = 2
        self.eprom_size = 8
        self.uart_size = 4
        self.sram_size = 0
        self.color = True
        self.verbose = False
        self.debug = False
        self.show_error_message = False


# options from command-line arguments
args = Args()

# for turning the "writing the nodetype in front of the parenthesis" for
# __repr__ temporarily on and off
show_node = True

# Name and path for the basename of all output files. If it stays empty this
# means one is in shell mode
outbase = ""

# each line from the <outbase>.in file ist taken as input for 'call input'
test_input = []

# constants to determine whether a number is in the right range for a certain
# dataype etc.
RANGE_OF_CHAR = (-128, 127)
RANGE_OF_PARAMETER = (-2097152, 2097151)
RANGE_OF_INT = (-2147483648, 2147483647)
