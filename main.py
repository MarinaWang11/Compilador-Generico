''' Funcionamento:

    1) Entrada: Função open() lê o conteúdo do arquivo. Caso o arquivo não exista, ele captura a exceção e avisa o usuário.

    2) Análise: O código-fonte em formato de string é passado para a classe Lexer. O método analyze() é invocado e retorna duas listas:
                uma contendo os tokens válidos e outra contendo possíveis erros léxicos encontrados.

    3) Saída e Validação: Se o código estiver correto, ele itera sobre a lista de tokens e cria uma tabela, a qual é impressa no terminal
                          e gravada em um arquivo. Caso haja erros léxicos, o programa exibe apenas os erros no terminal com a indicação
                          de linha e coluna, e bloqueia a geração do arquivo de saída. 
''' 

from lexerScanner.lexer import Lexer

if __name__ == "__main__":
    arquivo_entrada = "input.c" 

    try:
        with open(arquivo_entrada, "r", encoding="utf-8") as arquivo:
            codigo_c = arquivo.read()

    except FileNotFoundError:
        print(f"\n[ERRO CRÍTICO] O arquivo '{arquivo_entrada}' não foi encontrado na pasta.")

        print("Certifique-se de criar o arquivo e tentar novamente.")

        sys.exit(1) #Interrompe o programa se o arquivo não existir

    analisador = Lexer(codigo_c)

    try:
        lista_tokens, lista_erros = analisador.analyze()
            

        if lista_erros:
            print("\n")
            print(f"FORAM ENCONTRADOS {len(lista_erros)} ERROS LÉXICOS:")

            for e in lista_erros:
                print(f" -> {e}")
            
            print("\n[AVISO] Arquivo de tokens não gerado devido a erros no código fonte.")
        
        else:
            print(f"--- {len(lista_tokens)} TOKENS ENCONTRADOS ---")

            header = f"{'ID':<5} | {'LEXEMA':<15} | {'CLASSE':<15} | {'LINHA':<7} | {'COLUNA':<7}"
            separator = "-" * len(header)

            with open("output/lexer_output.txt", "w", encoding="utf-8") as arquivo:
                print(header)
                print(separator)
                
                arquivo.write(header + "\n")
                arquivo.write(separator + "\n")

                for t in lista_tokens:
                    linha_token = f"{t['id']:<5} | {t['lexeme']:<15} | {t['class']:<15} | {t['line']:<7} | {t['column']:<7}"
                    
                    print(linha_token)          
                    arquivo.write(linha_token + "\n") 

    
            print(f"\n[SUCESSO] {len(lista_tokens)} tokens processados e salvos em 'output/lexer_output.txt'.")

        
    except Exception as e:
        print(f"Erro inesperado no sistema: {e}")
