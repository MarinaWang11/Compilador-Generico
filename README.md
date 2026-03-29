# Compilador-Generico

TP1 - Compiladores 

## 📖 Sobre o Projeto
Este projeto é a construção de um compilador genérico para a linguagem C. Foi desenvolvido em Python e utiliza a biblioteca nativa `re` para manipulação das expressões regulares e casamento de padrões.
___

## ⚙️ O Processo de Compilação 
A compilação é o processo de traduzir um código escrito em linguagem de alto nível para linguagem de máquina. 
Esse processo é dividido em várias fases: Analisador Léxico, Analisador Sintático, Analisador Semântico, Gerador de Código e Otimizador.

___

## ⭐ Como Executar

### Pré-requisitos
* Python 3.x instalado e configurado nas variáveis de ambiente.

### Passo a Passo
1.  Clone este repositório ou baixe a pasta do projeto.
2.  Abra o terminal na raiz da pasta `Compilador-Generico`.
3.  Edite o arquivo `input.c` na mesma pasta do `main.py` com o código C que deseja analisar.
4.  Execute o comando:
    ```bash
    python main.py
    ```
    *(Nota para Windows: Caso o comando acima falhe, utilize `py main.py`)*

### Regras de Saída (output)
1.  Analisador Léxico:
    * **Sucesso:** Se o código não contiver erros léxicos, uma tabela formatada com todos os tokens será impressa no terminal e salva em arquivo.
    * **Falha:** Se o código contiver símbolos inválidos, imprimirá no terminal uma lista detalhada com todos os erros léxicos encontrados, apontando a localização exata de cada um.