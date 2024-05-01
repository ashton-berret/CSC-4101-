import re

# Define token categories using regex
KEYWORDS = r'\b(program|end_program|if|end_if|loop|end_loop)\b' #match language keywords. same idea with \b to make sure end_... is matched as a keyword and not as an identifier followed by a keyword
IDENTIFIERS = r'[a-zA-Z][a-zA-Z0-9]*' #match letters and digits as identifiers regardless of case
NUMBERS = r'[0-9]+' #match digits 
OPERATORS = r'[+\\-\\*/%=]' #match operators
LOGIC_OPERATORS = r'\b(==|>=|<=|>|<)\b' #match logic operators. Use the \b in order to ensure that each operator is matched as a sequence and not as individual logic operators or regular operators
DELIMITERS = r'[();:]' #match delimiter
WHITESPACE = r'\\s+' #match space(s)

# Create a dictionary storing token types as integers mostly for personal debugging but also to potentially help with changing tokens later if needed
TokenType = {
    'KEYWORD': 0,
    'IDENTIFIER': 1,
    'NUMBER': 2,
    'OPERATOR': 3,
    'LOGIC_OPERATOR': 4,
    'DELIMITER': 5,
    'WHITESPACE': 6
}

# Token class to initialize token type and value
class Token:
    def __init__(self, type, value): 
        self.type = type
        self.value = value

# function that turns an input string into a token that matches the structure of the program/type of valid program inputs
def tokenize(input):
    tokens = [] 
    #re module is used to compile a regular expression into an object so you can match that object against input strings
    pattern = re.compile(f'{KEYWORDS}|{IDENTIFIERS}|{NUMBERS}|{OPERATORS}|{LOGIC_OPERATORS}|{DELIMITERS}|{WHITESPACE}')
    for match in re.finditer(pattern, input): #iterates over tokens matched and checks if the type matches one of the defined token categories
        token_type = None
        if re.match(KEYWORDS, match.group()):
            token_type = TokenType['KEYWORD']
        elif re.match(IDENTIFIERS, match.group()):
            token_type = TokenType['IDENTIFIER']
        elif re.match(NUMBERS, match.group()):
            token_type = TokenType['NUMBER']
        elif re.match(OPERATORS, match.group()):
            token_type = TokenType['OPERATOR']
        elif re.match(LOGIC_OPERATORS, match.group()):
            token_type = TokenType['LOGIC_OPERATOR']
        elif re.match(DELIMITERS, match.group()):
            token_type = TokenType['DELIMITER']
        else:
            continue  # Ignore whitespace
        #print(f'Token: {match.group()}, Type: {list(TokenType.keys())[list(TokenType.values()).index(token_type)]}')
        tokens.append(Token(token_type, match.group())) #for all the matches, append that to the list of tokens

    return tokens

# Test with provided code input
input = 'program value = 32; mod1 = 45; z = mod1 / value * (value % 7) + mod1;  loop (i = 0 : value) z = z + mod1; end_loop if (z >= 50) newValue = 50 / mod1; x = mod1; end_if end_program'
tokens = tokenize(input)

