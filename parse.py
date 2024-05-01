import lexer
from lexer import *

#class that takes in the tokens created in the lexer.py file
class Parser: 
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr_index = 0

    #returns boolean if the index is less than number of tokens 
    def has_more_tokens(self):
        #print(f'Current token index: {self.curr_index}, Tokens length: {len(self.tokens)}')
        #print(f'Current token value: {self.get_curr_token().value}')
        return self.curr_index < len(self.tokens) 
        

    def get_curr_token(self):
        return self.tokens[self.curr_index]

    def get_next_token(self):
        self.curr_index += 1

    #tries to match the expected type, raises error if not
    #the expected value is only needed if encountering a delimiter, operator, or keyword. otherwise the parser doesn't need to know the exact val
    def match(self, expected_type, expected_value):
        #print(f'Expected type: {expected_type}, Expected value: {expected_value}')
        if not self.has_more_tokens():
            self.error('Error: End of Input Sequence')
        curr_token = self.get_curr_token()
        #print(f'Current token type: {curr_token.type}, Current token value: {curr_token.value}')

        #For the below code, None is only an acceptable expected value when it is examining a token's category where the exact token value (a specific logic operator, in example) doesn't matter
        if expected_type is not None and curr_token.type != expected_type:
            self.error(f'Expected token type: {expected_type}, found: {curr_token.type}')
        if expected_value is not None and curr_token.value != expected_value:
            self.error(f'Expected token value: {expected_value}, found: {curr_token.value}')

        self.get_next_token()

    #Matches identifier and returns that token
    def identifier(self): 
        token = self.get_curr_token()
        self.match(TokenType['IDENTIFIER'], None)
        return token
    
    #parses arithmetic operators
    def expression(self):
        self.term() #parse the first term
        while self.get_curr_token().type in [TokenType['OPERATOR']]: #loop to see if token is any operator, doesn't matter which
            self.match(TokenType['OPERATOR'], None)
            self.term() #recalls term to match next token

    #parses multiplication/division and modulo 
    def term(self):
        self.factor()
        while self.has_more_tokens() and (self.get_curr_token().value in ['*', '/', '%']):
            self.get_next_token()
            self.factor()

    #since factor is the lowest/base level token, it now calls the match function on the current token to check the token is expected type and value (if applicable)
    def factor(self):
        token = self.get_curr_token()
        if token.type == TokenType['IDENTIFIER']:
            self.match(TokenType['IDENTIFIER'], None)
        elif token.type == TokenType['NUMBER']:
            self.match(TokenType['NUMBER'], None)
        elif token.type == TokenType['DELIMITER'] and token.value == '(':
            self.match(TokenType['DELIMITER'], '(')
            self.expression() #if the token is following a '(', it calls the expression function to handle those tokens before moving on
            self.match(TokenType['DELIMITER'], ')')
        elif token.type == TokenType['OPERATOR']:
            self.match(TokenType['OPERATOR'], None)
        else:
            print(f'Encountered unknown token: {token.value} ({token.type})')
            raise RuntimeError (f'Syntax error {self(token)}: Factor Not Recognized')

    #starts and stops parsing based on matching the keywords
    def run_parser(self):
        self.match(TokenType['KEYWORD'], 'program') 
        self.parse_statements()
        self.match(TokenType['KEYWORD'], 'end_program')

    def parse_statements(self):
        #print('Entering parse_statements function')
        while self.has_more_tokens() and self.get_curr_token().value not in ['end_program', 'end_if', 'end_loop']: #moves the token to next step of parsing if it is not a ending keyword
            self.statement()

    #begin moving through the statement and call needed function depending on the type of statement indicated by matching strings
    def statement(self):
        if self.get_curr_token().type == TokenType['IDENTIFIER']:
            self.assignment()
        elif self.get_curr_token().type == TokenType['KEYWORD'] and self.get_curr_token().value == 'loop':
            self.loop()
        elif self.get_curr_token().type == TokenType['KEYWORD'] and self.get_curr_token().value == 'if':
            self.if_statement()
        else:
            self.error('Statement Type Not Recognized')

    def assignment(self):
        self.identifier()
        self.match(TokenType['OPERATOR'], '=')
        self.expression()
        self.match(TokenType['DELIMITER'], ';')

    def loop(self):
        #print('Entering loop function')
        self.match(TokenType['KEYWORD'], 'loop')
        #print('Matched loop keyword')
        self.match(TokenType['DELIMITER'], '(')
        #print('Matched left parenthesis')
        self.identifier()
        #print('Matched Identifier')
        self.match(TokenType['OPERATOR'], '=')
        #print('Matched Operator')
        self.expression()
        #print('Parsed expression')
        self.match(TokenType['DELIMITER'], ':')
        #print('Matched colon')
        self.expression()
        #print('Parsed expression')
        self.match(TokenType['DELIMITER'], ')')
        #print('Matched right parenthesis')
        self.parse_statements()
        #print('Parsed statement')
        self.match(TokenType['KEYWORD'], 'end_loop')
        #print('Matched end_loop keyword')

    def logic_expression(self):
        self.expression()
        while self.get_curr_token().type in [TokenType['OPERATOR']]:
            self.match(TokenType['OPERATOR'], None)
            self.expression()
        if self.get_curr_token().type in [TokenType['LOGIC_OPERATOR']]:
            self.match(TokenType['LOGIC_OPERATOR'], None)
            self.expression()


    def if_statement(self):
        #print('Entering if statement function')
        self.match(TokenType['KEYWORD'], 'if')
        #print('Matched if keyword')
        self.match(TokenType['DELIMITER'], '(')
        #print('Matched left parenthesis')
        token = self.get_curr_token()
        #print(f'Current token: {token.value}, {token.type}')
        self.logic_expression()
        #print('Parsed logic expression')
        self.match(TokenType['DELIMITER'], ')')
        #print('Matched right parenthesis')
        self.parse_statements()
        #print('Parsed logic statements')
        self.match(TokenType['KEYWORD'], 'end_if')
        #print('Matched end_if')


    def error(self, message):
        curr_token = self.get_curr_token()
        raise RuntimeError(f'Syntax error:  {message}')
    
    
    
    

# Test with provided code input
input = 'program value = 32; mod1 = 45; z = mod1 / value * (value % 7) + mod1;  loop (i = 0 : value) z = z + mod1; end_loop if (z >= 50) newValue = 50 / mod1; x = mod1; end_if end_program'
tokens = lexer.tokenize(input)
parser = Parser(tokens)
parser.run_parser()
print('Parsing Completed')