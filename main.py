''' Funcionamento:

    1) Entrada: Função open() lê o conteúdo do arquivo. Caso o arquivo não exista, ele captura a exceção e avisa o usuário.

    2) Análise Léxica: O código-fonte em formato de string é passado para a classe Lexer. O método analyze() é invocado e retorna duas listas:
                       uma contendo os tokens válidos e outra contendo possíveis erros léxicos encontrados.
    
    3) Análise Sintática: A lista de tokens é passada para a classe Parser, onde o método parse() é chamado. Ele verifica a estrutura do código 
                          de acordo com as regras gramaticais definidas, e retorna uma lista de erros sintáticos, caso existam.
    
    4) Análise Semântica: Durante a análise sintática, o Parser também realiza verificações semânticas, como checagem de tipos e uso de variáveis. 
                          Ele mantém uma tabela de símbolos para rastrear declarações e usos de variáveis, e gera relat

    5) Saída e Validação: Se o código fonte contiver erros léxicos, o programa exibe o relatório de erro detalhados no terminal
                          e bloqueia a geração do arquivo de saída. Caso todo o código esteja correto, a tabela de tokens estruturada é 
                          exibida no terminal e gravada permanentemente no arquivo "output/lexer_output.txt", ademais da tabela de símbolos 
                          do semântico que é gerada durante a análise e gravada no arquivo "output/symbol_table.txt". Já se contiver erros 
                          sintáticos e semânticos, o programa exibe o relatório de erro detalhados no terminal e gera o arquivo de saída 
                          "output/parser.txt".
'''

import sys
from lexerScanner.lexer import Lexer
from semanticAnalyzer.semantic import Parser, SymbolTable


if __name__ == "__main__":
    arquivo_entrada = "input.c" 

    try:
        with open(arquivo_entrada, "r", encoding="utf-8") as arquivo:
            codigo_c = arquivo.read()

    except FileNotFoundError:
        print(f"\n[ERRO CRÍTICO] O arquivo '{arquivo_entrada}' não foi encontrado na pasta.")

        print("Certifique-se de criar o arquivo e tentar novamente.")

        sys.exit(1) 

    analisador = Lexer(codigo_c)

    try:
        lista_tokens, lista_erros = analisador.analyze()
            

        if lista_erros:
            print("\n")
            print(f"FORAM ENCONTRADOS {len(lista_erros)} ERROS LÉXICOS:")

            for e in lista_erros:
                print(f" -> {e}")
            
            print("\n[AVISO] Arquivo de tokens não gerado devido a erros no código fonte.")
            sys.exit(1)

        else:
            print(f"[LEXER]")

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
        resultado_analise = analisador_sintatico.parse()
        
        erros_sintaticos = resultado_analise['syntax_errors']
        erros_semanticos = resultado_analise['semantic_errors']
        avisos_semanticos = resultado_analise['semantic_warnings']
        tabela_simbolos = resultado_analise['symbol_table']

        tem_erros_fatais = len(erros_sintaticos) > 0 or len(erros_semanticos) > 0

        if tem_erros_fatais:
            print("\n[ERRO] Compilação falhou!")
            
            with open("output/parser.txt", "w", encoding="utf-8") as arquivo_parser:
                if erros_sintaticos:
                    titulo = f"\n--- ERROS SINTÁTICOS ({len(erros_sintaticos)}) ---"
                    print(titulo)
                    arquivo_parser.write(titulo + "\n")
                    for e in erros_sintaticos: 
                        print(f" -> {e}")
                        arquivo_parser.write(f" -> {e}\n")
                        
                if erros_semanticos:
                    titulo = f"\n--- ERROS SEMÂNTICOS ({len(erros_semanticos)}) ---"
                    print(titulo)
                    arquivo_parser.write(titulo + "\n")
                    for e in erros_semanticos: 
                        print(f" -> {e}")
                        arquivo_parser.write(f" -> {e}\n")

            print("\n[AVISO] Arquivo 'output/parser.txt' gerado com os erros.")

        
        else:
            print("\n[SUCESSO]")
            with open("output/parser.txt", "w", encoding="utf-8") as arquivo_parser:
                arquivo_parser.write("[SUCESSO] COMPILAÇÃO BEM-SUCEDIDA!\n\n")
            
        if avisos_semanticos:
            print(f"\n[WARNINGS] ")
            for aviso in avisos_semanticos:
                print(f" -> {aviso}")

        print("\n--- TABELA DE SÍMBOLOS GERADA ---")
        
        header_sym = f"{'ID':<12} | {'TIPO':<9} | {'DECLARAÇÃO':<12} | {'INICIALIZADA':<13} | {'VALOR':<10} | {'USADA':<5}"
        sep_sym = "-" * len(header_sym)
        
        with open("output/symbol_table.txt", "w", encoding="utf-8") as arq_sym:
            print(header_sym)
            print(sep_sym)
            arq_sym.write(header_sym + "\n" + sep_sym + "\n")
            
            for sym in tabela_simbolos:
                decl = f"{sym['decl_line']} x {sym['decl_col']}"
                inic = sym['init_pos'] if sym['init_pos'] != ' ' else ("True" if sym['initialized'] else "False")
                usada = "True" if sym['used'] else "False"
                
                valor = sym['value']
                
                linha = f"{sym['name']:<12} | {sym['type']:<9} | {decl:<12} | {inic:<13} | {valor:<10} | {usada:<5}"
                
                print(linha)
                arq_sym.write(linha + "\n")
                
        print("\n[INFO] Tabela de Símbolos salva em 'output/symbol_table.txt'.")

    except Exception as e:
        print(f"Erro inesperado durante a análise semântica: {e}")
    
