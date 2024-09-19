### ESTE É O ARQUIVO QUE CONTÉM TODAS AS FUNÇÕES UTILIZADAS NO ARQUIVO sudoku.py ###

from time import sleep
import os
import platform

# Função para ler o arquivo de jogadas do modo batch e armazenar as jogadas(já padronizadas) em uma lista:
def ler_jogadas(arquivo, lista_jogadas):

    with open(arquivo, "r") as file:
        for line in file:
            entrada = line
            # Padronizando entrada:
            entrada = entrada.replace(":", "")
            entrada = entrada.replace(";", "")
            entrada = entrada.replace(".", "")
            entrada = entrada.replace(",", "")
            entrada = entrada.replace(" ", "")
            entrada = entrada.strip()

            lista_jogadas.append(entrada)

        return lista_jogadas

# Função para ler o arquivo de pistas:
def ler_pistas(arquivo, tabuleiro):
    contador = 0
    pistas_invalidas = False
    try:
        with open(arquivo, "r") as file:
            for linha in file:
                
                # Vamos remover as quebras de linhas e espaços inúteis:
                linha = linha.strip()

                # Vamos verificar se contém ":":
                if linha:

                    # Vamos separar a jogada em coluna + linha e número:
                    celula, numero = linha.split(':')

                    # Vamos remover os espaços inúteis:
                    celula = celula.strip()
                    numero = numero.strip()

                    # Separando as colunas e linhas (Ex: "F,1"):
                    try:
                        coluna, linha_tabuleiro = celula.split(',')
                        coluna = coluna.strip()
                        linha_tabuleiro = linha_tabuleiro.strip()

                        # Convertendo as letras das colunas para números:
                        coluna = ord(coluna.lower()) - ord('a')

                        # Convertendo as linhas para índices do tabuleiro:
                        linha_tabuleiro = int(linha_tabuleiro) - 1

                        # Verificando se os índices estão nos limites:
                        if 0 <= linha_tabuleiro < 9 and 0 <= coluna < 9 and check(tabuleiro, coluna, linha_tabuleiro, int(numero)):
                            contador += 1

                            # Atribuindo o número ao tabuleiro:
                            tabuleiro[linha_tabuleiro][coluna] = int(numero)
                        else:
                            pistas_invalidas = True
                    except ValueError:
                        pistas_invalidas = True
            if contador > 80:
                pistas_invalidas = True
            return pistas_invalidas
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
    except Exception as erro:
        print(f"Erro ao ler o arquivo: {erro}")

# Função referente a mensagem inicial:
def mensagem_inicial():
    print("\n")
    sleep(0.3)
    print("+" + "-="*24 + "-+")
    sleep(0.3)
    print("|" + " "*49 + "|")
    sleep(0.3)
    print("|" + " "*12 + "ARQUIVO DE PISTAS INSERIDO" + " "*11 + "|")
    sleep(0.3)
    print("|" + " "*18 + "JOGO INICIADO" + " "*18 + "|")
    sleep(0.3)
    print("|" + " "*19 + "BOM JOGO!!!" + " "*19 + "|")
    sleep(0.3)
    print("|" + " "*49 + "|")
    sleep(0.3)
    print("+" + "-="*24 + "-+")
    print("\n")
    sleep(1)

# Função referente a mensagem final:
def mensagem_final():
    print("\n")
    sleep(0.2)
    print("+" + "-="*24 + "-+")
    sleep(0.2)
    print("|" + " "*49 + "|")
    sleep(0.2)
    print("|" + " "*6 + "A GRADE FOI PREENCHIDA COM SUCESSO!!!" + " "*6 + "|")
    sleep(0.2)
    print("|" + " "*16 + "JOGO CONCLUÍDO!!!" + " "*16 + "|")
    sleep(0.2)
    print("|" + " "*19 + "PARABÉNS!!!" + " "*19 + "|")
    sleep(0.2)
    print("|" + " "*49 + "|")
    sleep(0.2)
    print("+" + "-="*24 + "-+")
    print("\n")

# Códigos ANSI de cores:
vermelho = "\033[31m"
normal = "\033[0m"

# Função para gerar e imprimir o tabuleiro (onde tem 0, fica vazio):
def print_tabuleiro(tabuleiro, tabuleiroBool):
    print("     A   B   C    D   E   F    G   H   I")
    for i in range(9):
        if i == 3 or i == 6:
            print("  ++===+===+===++===+===+===++===+===+===++")
        else:
            print("  ++---+---+---++---+---+---++---+---+---++")
        print(i + 1, "||", end=" ")

        for j in range(9):
            if tabuleiro[i][j] != 0:
                # Jogadas fornecidas pelo arquivo (pistas) em vermelho com fundo branco
                if not tabuleiroBool[i][j]:
                    print(f"{vermelho}{tabuleiro[i][j]}{normal}", end=" ")
                # Jogadas do jogador (futuras) sem formatação
                else:
                    print(str(tabuleiro[i][j]), end=" ")
            else:
                print(" ", end=" ")

            if j < 8:
                if j == 2 or j == 5:
                    print("||", end=" ")
                else:
                    print("|", end=" ")
        print("||", end=" ")
        print(end="\n")
    print("  ++---+---+---++---+---+---++---+---+---++")

# Função que será usada como validação extra para o usuário:
def certeza(pergunta):
    while True:
        simNao = input(pergunta)
        simNao = str.lower(simNao).strip()
        if simNao[0] == "s":
            return "s"
        elif simNao[0] == "n":
            return "n"
        else:
            print("Resposta inválida, a célula não foi alterada...")

# Função que verifica se um número pode ser colocado em um determinado quadrante:
def check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
    for i in range(3):
        for j in range(3):
            if tabuleiro[i_inicial + i][j_inicial + j] == numero:
                return True
    return False

# Função que verifica se um número pode ser colocado em uma célula[linha][coluna]:
def check(tabuleiro, coluna, linha, numero):
    i_inicial = linha // 3 * 3
    j_inicial = coluna // 3 * 3

    for i in range(9):
        if tabuleiro[i][coluna] == numero or tabuleiro[linha][i] == numero:
            return False
    if check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
        return False
    return True

# Função básica pra limpar o terminal, funciona pra windows e pra linux:
def limpar_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
