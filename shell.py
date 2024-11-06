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


#error class
class Error():
    def __init__(self, error_name, error_details):
        self.error_name = error_name
        self.error_details = error_details

    def return_errror(self):
        return f'{self.error_name}: {self.error_details}'
    
class IllegalCharacterError(Error):
    def __init__(self, details):
        super().__init__("Illegal Character Error", details)


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
    def __init__(self,text):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.advance()

    def advance(self): # advance function advances one character at a time
        self.pos+=1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None
        
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
                char = self.curr_char
                self.advance()
                return [], IllegalCharacterError(char)
            
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
        
    #run function to run the lexer
def run(text):
    lexer = Lexer(text)
    token, error = lexer.tokenize()

    return token,error
