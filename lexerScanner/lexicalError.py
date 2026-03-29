'''    
    Lançar erros específicos quando um caractere inválido é encontrado, fornecendo informações detalhadas sobre a localização do erro no código-fonte.
'''
class LexicalError(Exception):
    def __init__(self, char, line, column):
        self.message = f"Erro Léxico: Caractere inesperado '{char}' na linha {line}, coluna {column}."
        
        super().__init__(self.message)