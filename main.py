''' Funcionamento:

    1) Entrada: Função open() lê o conteúdo do arquivo. Caso o arquivo não exista, ele captura a exceção e avisa o usuário.

    2) Análise Léxica: O código-fonte em formato de string é passado para a classe Lexer. O método analyze() é invocado e retorna duas listas:
                       uma contendo os tokens válidos e outra contendo possíveis erros léxicos encontrados.
    
    3) Análise Sintática: A lista de tokens é passada para a classe Parser, onde o método parse() é chamado. Ele verifica a estrutura do código 
                          de acordo com as regras gramaticais definidas, e retorna uma lista de erros sintáticos, caso existam.

    4) Saída e Validação: Se o código fonte contiver erros léxicos, o programa exibe o relatório de erro detalhados no terminal
                          e bloqueia a geração do arquivo de saída. Caso todo o código esteja correto, a tabela de tokens estruturada é 
                          exibida no terminal e gravada permanentemente no arquivo "output/lexer_output.txt". Já se contiver erros sintáticos,
                          o o programa exibe o relatório de erro detalhados no terminal e gera o arquivo de saída.
'''

import sys
from lexerScanner.lexer import Lexer
from parser.parser import Parser


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
            print(f"[LEXER] FORAM ENCONTRADOS {len(lista_tokens)} TOKENS")

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

    analisador_sintatico = Parser(lista_tokens)
    
    try:
        erros_sintaticos = analisador_sintatico.parse()

        if erros_sintaticos:
            print(f"\n[PARSER] FORAM ENCONTRADOS {len(erros_sintaticos)} ERROS SINTÁTICOS:")

            with open("output/parser.txt", "w", encoding="utf-8") as arquivo_erros:
                arquivo_erros.write(f"RELATÓRIO DE ERROS SINTÁTICOS - TOTAL: {len(erros_sintaticos)} \n\n")
                
                for e in erros_sintaticos:
                    print(f" -> {e}")
                    arquivo_erros.write(f" -> {e}\n")

            print("\n[AVISO] Compilação abortada, os erros foram salvos em 'output/parser_output.txt'")

        else:
            print("\n[SUCESSO] Análise sintática concluída sem erros.")
            
            # Abre o arquivo para registrar o sucesso da compilação sintática
            with open("output/parser_output.txt", "w", encoding="utf-8") as arquivo_sucesso:
                arquivo_sucesso.write("STATUS: COMPILAÇÃO BEM-SUCEDIDA\n")

    except Exception as e:
        print(f"Erro inesperado durante a análise sintática: {e}")

    
