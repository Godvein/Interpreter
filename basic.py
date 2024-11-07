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


#Error class
class Error():
    def __init__(self,pos_start, pos_end, error_name, error_details):
        self.pos_start = pos_start 
        self.pos_end = pos_end
        self.error_name = error_name
        self.error_details = error_details

    def return_errror(self):
        return f'{self.error_name}: {self.error_details}, File{self.pos_start.fn}, line {self.pos_end.ln + 1}'
    
class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end,details):
        super().__init__(pos_start, pos_end, "Illegal Character Error", details)

#position class 
class Position():
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    #advance to next position
    def advance(self, curr_char):
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
    def __init__(self, type, value = None):
        self.type = type 
        self.value = value

    def __repr__(self):
        if self.type: return f'{self.type} : {self.value}'
        return self.value

#lexer class lexes through each character and add it to the tokens by calling the token class which returns its type and text value
class Lexer():
    def __init__(self,text,fn):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.curr_char = None
        self.advance()

    def advance(self): # advance function advances one character at a time
        self.pos.advance(self.curr_char)
        self.curr_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def tokenize(self):
        tokens = []

        while self.curr_char is not None:
            if self.curr_char in ' \t': #check if current character is space or tab and ignore it to advance to next
                self.advance()
            #setting numbers in the token it can be either fload or integer
            elif self.curr_char in DIGITS:
                tokens.append(self.make_numbers())
                self.advance()
            #setting the operators in the token
            elif self.curr_char == "+":
                tokens.append(Token(PLUS))
                self.advance()
            elif self.curr_char == "-":
                tokens.append(Token(MINUS))
                self.advance()
            elif self.curr_char == "*":
                tokens.append(Token( MULTIPLY))
                self.advance()
            elif self.curr_char == "/":
                tokens.append(Token(DIVIDE))
                self.advance()
            elif self.curr_char == "%":
                tokens.append(Token(MODULUS))
                self.advance()
            elif self.curr_char == "^":
                tokens.append(Token(POWER))
                self.advance()
            
            #setting the parentheses in the token
            elif self.curr_char == "(":
                tokens.append(Token(LEFT_PAR))
                self.advance()
            elif self.curr_char == ")":
                tokens.append(Token(RIGHT_PAR))
                self.advance()
            else:
                #return error
                pos_start = self.pos.copy()
                char = self.curr_char
                self.advance()
                return [], IllegalCharacterError(pos_start, self.pos,char)
            
        return tokens, None

#check if number is float or integer
    def make_numbers(self):
        dot_count = 0
        num = ''

        while self.curr_char is not None and self.curr_char in DIGITS + '.':
            if self.curr_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num += '.'
            else:
                num+= self.curr_char
            self.advance()
        if dot_count == 0:
            return Token(INTEGER, int(num))
        else:
            return Token(FLOAT, float(num))   

#nodes for numbers and binary expression   
#      plus 
#     /   \
#    3    mul
#         /  \   
#        1    2              (3 + (1 * 2))

class NumberNode():
    def __init__(self, tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'
    
class BinaryOpNode():
    def __init__(self, leftnode, optok, rightnode):
        self.leftnode = leftnode
        self.optok = optok
        self.rightnode = rightnode

    def __repr__(self):
        return f'({self.leftnode}, {self.optok}, {self.rightnode})'
    
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
        return res
    
    def factor(self):
        tok = self.curr_tok

        if tok.type in (INTEGER, FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        return self.binaryOp(self.factor, (MULTIPLY, DIVIDE)) 
                                                                  
    def exp(self):
        return self.binaryOp(self.term, (PLUS, MINUS)) 

    def binaryOp(self, func, ops):
        left = func()

        while self.curr_tok.type in ops:
            optok = self.curr_tok
            self.advance()
            right = func()
            left = BinaryOpNode(left, optok, right)
            
        return left

    #run function to run the lexer
def run(text, fn):
    lexer = Lexer(text, fn)
    token, error = lexer.tokenize()
    if error: return None, error

    #generate Abstract Syntax Tree(AST)
    parser = Parser(token)
    ast = parser.parse()
    return ast,error
