''' 
    A cada iteração do while, o código tenta casar o texto na posição atual com alguma regra (Expressão Regular):

        1) Se encontrar um padrão válido, ele extrai o lexema, calcula o tamanho, cria um objeto Token, e avança o 
           ponteiro de acordo com o comprimentodo lexema lido. 

        2) Se o ponteiro parar em um caractere que não bate com nenhuma regra (mismatch), ou identificar um comentário  
           de bloco/string/char não fechado, o erro é formatado com sua localização exata, adicionado a uma lista de 
           erros, e o ponteiro é forçado a avançar para fazer a análise do restante do código.
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
        self.position = 0  
        self.line = 1
        self.column = 1
        
        
        #Compila cada regex individualmente, a ordem importa
        
        rules = [
            (r'/\*[\s\S]*?\*/', 'COMMENT_MULTI'),
            (r'/\*[\s\S]*', 'UNCLOSED_COMMENT'), 
            (r'//.*', 'COMMENT_SINGLE'),
            (r'\b(if|for|int|bool|string|float|char)\b', 'RESERVED_WORD'),
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
            (r'\b\d+\.\d+\b', 'FLOAT_LIT'),
            (r'\b\d+\b', 'INT_LIT'),
            (r'".*?"', 'STRING_LIT'),
            (r"'.'", 'CHAR_LIT'),
            (r'\+\+|--|==|<=|>=|&&|\|\||[+\-*/<>=!]', 'OPERATOR'),
            (r'[{}();]', 'DELIMITER'),
            (r'\n', 'NEWLINE'),
            (r'[ \t]+', 'WHITESPACE'),
            (r'.', 'MISMATCH') #Caractere inválido
        ]
        
        self.rules_compiled = [(re.compile(pattern), tag) for pattern, tag in rules]

    def analyze(self):
        while self.position < len(self.source_code):
            match_found = False
            
            for regex, token_class in self.rules_compiled:
                match = regex.match(self.source_code, self.position)
                
                if match:
                    lexeme = match.group(0)

                    if token_class == 'NEWLINE':
                        self.line += 1
                        self.column = 1

                    elif token_class in ['WHITESPACE', 'COMMENT_SINGLE']:
                        self.column += len(lexeme)

                    elif token_class == 'COMMENT_MULTI':
                        newlines = lexeme.count('\n')

                        if newlines > 0:
                            self.line += newlines

                            #Calcula a col da última linha do comentário
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
                    
                    # Avança o ponteiro
                    self.position = match.end()
                    match_found = True

                    break #nova posicao
            
            #Trava de segurança caso o regex falhe 
            if not match_found:
                char_problem = self.source_code[self.position]

                raise Exception(f"Erro Crítico: Falha ao processar '{char_problem}' na linha {self.line}")

        return self.tokens, self.errors