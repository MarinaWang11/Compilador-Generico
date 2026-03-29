'''
    Um token é a menor unidade de significado em um código-fonte, possuindo 5 características de cada símbolo validado.
'''

class Token:
    def __init__(self, token_id, lexeme, token_class, line, column):
        self.id = token_id            
        self.lexeme = lexeme          #String exata 
        self.token_class = token_class
        self.line = line              
        self.column = column          

    def __repr__(self):
        #Formatação da lista 
        return f"[ID: {self.id:03d} | Token: {self.lexeme:<10} | Classe: {self.token_class:<15} | Linha: {self.line:02d} | Coluna: {self.column:02d}]"