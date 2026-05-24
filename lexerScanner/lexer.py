''' 
    In each iteration of the while loop, the code tries to match the text at the current position with some rule (Regular Expression):

        1) If finds an match, it extracts the lexeme, calculates the size, creates a Token object, and advances the 
           pointer according to the length of the read lexeme. 

        2) If the pointer stops at a character that doesn't match any rule (mismatch), or identifies an unclosed comment  
           of block/string/char, the error is formatted with its exact location, added to a list of 
           errors, and the pointer is forced to advance to continue the analysis of the rest of the code.
'''

import re

from lexerScanner.tokenClass import Token
from lexerScanner.lexicalError import LexicalError

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code 
        self.tokens = []
        self.errors = []
        self.current_id = 1
        self.position = 0  #pointer to current position in source code
        self.line = 1
        self.column = 1
        
        #Compiles each regex individually, the order matters (e.g., comments before operators to avoid conflicts)

        rules = [
            (r'/\*[\s\S]*?\*/', 'COMMENT_MULTI'),
            (r'/\*[\s\S]*', 'UNCLOSED_COMMENT'), 
            (r'//.*', 'COMMENT_SINGLE'),
            (r'\b(if|for|int|bool|string|float|char|return)\b', 'RESERVED_WORD'),
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
            (r'\b\d+\.\d+\b', 'FLOAT_LIT'),
            (r'\b\d+\b', 'INT_LIT'),
            (r'".*?"', 'STRING_LIT'),
            (r"'.'", 'CHAR_LIT'),
            (r'\+\+|--|==|<=|>=|&&|\|\||[+\-*/<>=!]', 'OPERATOR'),
            (r'[{}();]', 'DELIMITER'),
            (r'\n', 'NEWLINE'),
            (r'[ \t]+', 'WHITESPACE'),
            (r'.', 'MISMATCH') #invalid
        ]
        
        self.rules_compiled = [(re.compile(pattern), tag) for pattern, tag in rules] 

    def analyze(self):
        while self.position < len(self.source_code): 
            match_found = False
            
            for regex, token_class in self.rules_compiled:
                match = regex.match(self.source_code, self.position) #try to match the regex at the current position
                
                if match: 
                    lexeme = match.group(0) #text matched by the regex

                    if token_class == 'NEWLINE':
                        self.line += 1
                        self.column = 1

                    elif token_class in ['WHITESPACE', 'COMMENT_SINGLE']:
                        self.column += len(lexeme)

                    elif token_class == 'COMMENT_MULTI':
                        newlines = lexeme.count('\n')

                        if newlines > 0:
                            self.line += newlines

                            #calculate column position after the last newline in the comment
                            last_newline_idx = lexeme.rfind('\n') 
                            self.column = len(lexeme) - last_newline_idx

                        else:
                            self.column += len(lexeme)

                    elif token_class == 'UNCLOSED_COMMENT':
                        self.errors.append(f"Erro: Comentário não fechado na linha {self.line}, col {self.column}")
                    
                    elif token_class == 'MISMATCH':
                        self.errors.append(f"Erro: Caractere inválido '{lexeme}' na linha {self.line}, col {self.column}")
                    
                    else:                        
                        token = {
                            "id": self.current_id,
                            "lexeme": lexeme,
                            "class": token_class,
                            "line": self.line,
                            "column": self.column
                        }

                        self.tokens.append(token)
                        self.current_id += 1
                        self.column += len(lexeme)
                    
                    #Advance the position pointer to the end of the matched lexeme
                    self.position = match.end() 
                    match_found = True 

                    break #new position
            
            #Security lock if none of the rules match
            if not match_found:
                char_problem = self.source_code[self.position]

                raise Exception(f"Erro Crítico: Falha ao processar '{char_problem}' na linha {self.line}")

        return self.tokens, self.errors