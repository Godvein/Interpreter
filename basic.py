#Constants
DIGITS = "0123456789"
# Tokens
# Parentheses
LEFT_PAR = "LEFT_PAR"         # (
RIGHT_PAR = "RIGHT_PAR"       # )

# Operators
PLUS = "PLUS"                 # +
MINUS = "MINUS"               # -
MULTIPLY = "MULTIPLY"         # *
DIVIDE = "DIVIDE"             # /
MODULUS = "MODULUS"           # %
POWER = "POWER"               # ^

# Comparison Operators
EQUAL = "EQUAL"               # ==
NOT_EQUAL = "NOT_EQUAL"       # !=
LESS_THAN = "LESS_THAN"       # <
GREATER_THAN = "GREATER_THAN" # >
LESS_EQUAL = "LESS_EQUAL"     # <=
GREATER_EQUAL = "GREATER_EQUAL" # >=

# Assignment
ASSIGN = "ASSIGN"             # =

# Logical Operators
AND = "AND"                   # &&
OR = "OR"                     # ||
NOT = "NOT"                   # !

# Delimiters
COMMA = "COMMA"               # ,
SEMICOLON = "SEMICOLON"       # ;

# Literals
INTEGER = "INTEGER"           # Integer values
FLOAT = "FLOAT"               # Floating point values
STRING = "STRING"             # String values
IDENTIFIER = "IDENTIFIER"     # Variable names or identifiers

# Keywords (you might add more specific ones based on your language)
LET = "LET"                   # for variable declarations
IF = "IF"
ELSE = "ELSE"
WHILE = "WHILE"
FOR = "FOR"
FUNCTION = "FUNCTION"
RETURN = "RETURN"
TRUE = "TRUE"                 # Boolean true
FALSE = "FALSE"               # Boolean false
NULL = "NULL"                 # Null or none

EOF = "EOF"

from string_with_arrows import *
#Error class
class Error():
    def __init__(self,pos_start, pos_end, error_name, error_details):
        self.pos_start = pos_start 
        self.pos_end = pos_end
        self.error_name = error_name
        self.error_details = error_details

    def return_errror(self):
        result =  f'{self.error_name}: {self.error_details}\n'
        result += f'File{self.pos_start.fn}, line {self.pos_end.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end,details):
        super().__init__(pos_start, pos_end, "Illegal Character Error", details)

class SyntaxError(Error):
    def __init__(self, pos_start, pos_end,details):
        super().__init__(pos_start, pos_end, "Syntax Error", details)

class RunTimeError(Error):
    def __init__(self, pos_start, pos_end,details):
        super().__init__(pos_start, pos_end, "Run-Time Error", details)

#position class 
class Position():
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    #advance to next position
    def advance(self, curr_char = None):
        self.idx += 1
        self.col += 1
        #new line
        if curr_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
        

# the token class when called returns a representation of type and text
class Token():
    def __init__(self, type, value = None, pos_start = None, pos_end = None):
        self.type = type 
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.type: return f'{self.type} : {self.value}'
        return self.value

#lexer class lexes through each character and add it to the tokens by calling the token class which returns its type and text value
class Lexer():
    def __init__(self, text, fn):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.curr_char = None
        self.advance()

    def advance(self): 
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def tokenize(self):
        tokens = []

        while self.curr_char is not None:
            if self.curr_char in ' \t':  # Skip whitespace
                self.advance()
            # If it's a number (integer or float), process it
            elif self.curr_char in DIGITS:
                tokens.append(self.make_numbers())
            # If it's an operator, add it as a token
            elif self.curr_char == "+":
                tokens.append(Token(PLUS,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == "-":
                tokens.append(Token(MINUS,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == "*":
                tokens.append(Token(MULTIPLY,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == "/":
                tokens.append(Token(DIVIDE,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == "%":
                tokens.append(Token(MODULUS,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == "^":
                tokens.append(Token(POWER,None, pos_start= self.pos))
                self.advance()
            # Handle parentheses as tokens
            elif self.curr_char == "(":
                tokens.append(Token(LEFT_PAR,None, pos_start= self.pos))
                self.advance()
            elif self.curr_char == ")":
                tokens.append(Token(RIGHT_PAR,None, pos_start= self.pos))
                self.advance()
            else:
                # If an invalid character is found, raise an error
                pos_start = self.pos.copy()
                char = self.curr_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos, char)

        tokens.append(Token(EOF, None, self.pos))
        return tokens, None

    # Method to handle numbers, including floating-point numbers
    def make_numbers(self):
        dot_count = 0
        num = ''
        start_pos = self.pos.copy()

        while self.curr_char is not None and self.curr_char in DIGITS + '.':
            if self.curr_char == '.':
                if dot_count == 1: break  # Ensure there's only one dot for decimal
                dot_count += 1
                num += '.'
            else:
                num += self.curr_char
            self.advance()

        if dot_count == 0:
            return Token(INTEGER, int(num), start_pos, self.pos)
        else:
            return Token(FLOAT, float(num), start_pos, self.pos)
 

#nodes for numbers and binary expression   
#      plus 
#     /   \
#    3    mul
#         /  \   
#        1    2              (3 + (1 * 2))

class NumberNode():
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
    
class BinaryOpNode():
    def __init__(self, leftnode, optok, rightnode):
        self.leftnode = leftnode
        self.optok = optok
        self.rightnode = rightnode

        self.pos_start = self.leftnode.pos_start
        self.pos_end = self.rightnode.pos_start

    def __repr__(self):
        return f'({self.leftnode}, {self.optok}, {self.rightnode})'

class UnaryOperation():
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'{self.op_tok}, {self.node}'
    
#Parse Result class to check for any error during parsing
class ParseResult():
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
#Parser
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokidx = -1
        self.advance()

    def advance(self):
        self.tokidx += 1
        if self.tokidx < len(self.tokens):
            self.curr_tok = self.tokens[self.tokidx] 
        return self.curr_tok
        
    def parse(self):
        res = self.exp()
        if self.curr_tok.type != EOF and not res.error:
            return res.failure(SyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end,
            "Expected '+', '-', '*' or '/'"))
        return res
    
    def factor(self):
        tok = self.curr_tok
        res = ParseResult()


        if tok.type in (PLUS,MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOperation(tok, factor))

        elif tok.type in (INTEGER, FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.type == LEFT_PAR:
            res.register(self.advance())
            expr = res.register(self.exp())
            if res.error: return res
            if self.curr_tok.type == RIGHT_PAR:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(SyntaxError(self.curr_tok.pos_start, self.curr_tok.pos_end, "Expected ')'"))
        return res.failure(SyntaxError(tok.pos_start, tok.pos_end, "Expected int or float"))

    def term(self):
        return self.binaryOp(self.factor, (MULTIPLY, DIVIDE)) 
                                                                  
    def exp(self):
        return self.binaryOp(self.term, (PLUS, MINUS)) 

    def binaryOp(self, func, ops):
        res = ParseResult()
        left = res.register(func())

        while self.curr_tok.type in ops:
            optok = self.curr_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinaryOpNode(left, optok, right)
            
        return res.success(left)
#Numeric Operation
class Number():
    def __init__(self, value):
        self.value = value
        self.setposition()
    
    def setposition(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    #Addition
    def addvalue(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    #Subtracton
    def subtractvalue(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None
    
    #Multiplication
    def multiplyvalue(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    #Division
    def dividevalue(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(self.pos_start, self.pos_end, "not divisible by 0")
            return Number(self.value / other.value), None

#Interpreter Error Check
class InterpreterResult():
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res

    def success(self,value):
        self.value = value 
        return self

    def failure(self, error):
        self.error = error
        return self

#Interpreter
class Interpreter():
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.novisitmethod)
        return method(node)

    def novisitmethod(self, node):
        raise Exception(f'no visit method found {node.type.__name__}')
    
    def visit_NumberNode(self, node):
        return InterpreterResult().success(
            Number(node.tok.value).setposition(node.tok.pos_start, node.tok.pos_end))

    def visit_BinaryOpNode(self, node):
        res = InterpreterResult()
        left = res.register(self.visit(node.leftnode))
        if res.error: return res

        right = res.register(self.visit(node.rightnode))
        if res.error: return res

        left_value = left.value
        right_value = right.value

        if node.optok.type == PLUS:
            result,error = left_value.addvalue(right_value)
        elif node.optok.type == MINUS:
            result,error = left_value.subtractvalue(right_value)
        elif node.optok.type == MULTIPLY:
            result,error = left_value.multiplyvalue(right_value)
        elif node.optok.type == DIVIDE:
            result,error = left_value.dividevalue(right_value)

        if error: 
            return res.failure(error)

        else: return res.success(result.setposition(node.pos_start, node.pos_end))

    def visit_UnaryOperation(self, node):
        res = InterpreterResult()
        number = res.register(self.visit(node.node))
        if res.error: return res

        error = None

        if node.op_tok.type == MINUS:
            number,error = number.multiplyvalue(Number(-1))

        if error: return res.failure(error)

        return res.success(number.setposition(node.pos_start, node.pos_end))
        
    #run function to run the lexer
def run(text, fn):
    lexer = Lexer(text, fn)
    token, error = lexer.tokenize()
    if error: return None, error

    #generate Abstract Syntax Tree(AST)
    parser = Parser(token)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)
   
    return result.value, result.error
   
