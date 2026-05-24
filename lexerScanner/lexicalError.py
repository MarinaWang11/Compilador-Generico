'''    
    Launches a error in case of a lexical error, indicating the unexpected character and its position (line and column) in the source code.
'''
class LexicalError(Exception):
    def __init__(self, char, line, column):
        self.message = f"Erro Léxico: Caractere inesperado '{char}' na linha {line}, coluna {column}."
        
        super().__init__(self.message)