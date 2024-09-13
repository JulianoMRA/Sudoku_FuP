import sys
import fun

# Função para ler o arquivo de jogadas do modo batch e armazenar as jogadas(já padronizadas) em uma lista
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
    
    
    
        
# Função para ler o arquivo de dicas no formato "<coluna>,<linha>: <numero>":
def ler_dicas(arquivo, tabuleiro):
    contador = 0
    flag3 = False
    try:
        with open(arquivo, "r") as file:
            for linha in file:
                
                # Vamos remover as quebras de linhas e espaços inúteis:
                linha = linha.strip()

                # Vamos verificar se a linha está vazia e se contém ":":
                if ':' in linha:

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
                            flag3 = True
                    except ValueError:
                        flag3 = True
            if contador > 80:
                flag3 = True
            return flag3
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
    except Exception as erro:
        print(f"Erro ao ler o arquivo: {erro}")

# Função que cria a mensagem:
def mensagem_inicial():
    print("\n")
    fun.sleep(0.3)
    print("+" + "-="*24 + "-+")
    fun.sleep(0.3)
    print("|" + " "*49 + "|")
    fun.sleep(0.3)
    print("|" + " "*12 + "ARQUIVO DE DICAS INSERIDO" + " "*12 + "|")
    fun.sleep(0.3)
    print("|" + " "*18 + "JOGO INICIADO" + " "*18 + "|")
    fun.sleep(0.3)
    print("|" + " "*19 + "BOM JOGO!!!" + " "*19 + "|")
    fun.sleep(0.3)
    print("|" + " "*49 + "|")
    fun.sleep(0.3)
    print("+" + "-="*24 + "-+")
    print("\n")
    fun.sleep(1)

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
                # Jogadas fornecidas pelo arquivo (dicas) em vermelho com fundo branco
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

# Função básica pra limpar o terminal, funciona pra windows e pra linux
def limpar_terminal():
    if fun.platform.system() == "Windows":
        fun.os.system('cls')
    else:
        fun.os.system('clear')


    

#### INICIO DO CODIGO ####


# Condição que verifica a quantidade de argumentos fornecidos no comando inicial: 
if not 2 <= len(sys.argv) <= 3:
    print("""A quantidade de arquivos não condiz com nenhum modo de jogo!
            Modo Interativo:
                Um arquivo .txt.
            Modo Batch:
                Dois arquivos .txt.""")
    
# Inicializando o tabuleiro e tabuleiroBool
else:
    tabuleiro = [[0 for _ in range(9)] for _ in range(9)]
    tabuleiroBool = [[True for _ in range(9)] for _ in range(9)]

    # Capturando o nome do arquivo da linha de comando
    arquivo = sys.argv[1]

    flag2 = True

    # Ler o arquivo de dicas e preencher o tabuleiro
    flag3 = ler_dicas(arquivo, tabuleiro)
    if flag3:
        flag2 = False
        print("Arquivo de dicas inválido!")
    # Exibe a mensagem
    else:
        mensagem_inicial() 
    # Atualizando o tabuleiroBool para marcar as dicas como imutáveis
    for i in range(9):
        for j in range(9):
            if tabuleiro[i][j] != 0:
                tabuleiroBool[i][j] = False


# Verifica se é o modo interativo:
if len(sys.argv) == 2:

    # Modo Interativo (Início):
    contador = 0
    flag4 = False

    while flag2:

        if contador == 0:
            # Exibir o tabuleiro inicial
            print_tabuleiro(tabuleiro, tabuleiroBool)
            entrada = input("Entre com uma jogada: ")
        elif flag4:
            entrada = input("Tente novamente. ")
            flag4 = False
        else:
            entrada = input("Próxima jogada! ")

        # Padronizando entrada:
        entrada = entrada.replace(":", "")
        entrada = entrada.replace(";", "")
        entrada = entrada.replace(".", "")
        entrada = entrada.replace(",", "")
        entrada = entrada.replace(" ", "")
        entrada = entrada.strip()

        # Verificando se a entrada é válida
        if len(entrada) == 3:

            # Condições que implementam o comando de apagar uma célula [!]:
            if entrada[0] == "!" and entrada[1].isalpha() and entrada[2].isnumeric():
                coluna, linha = entrada[1], entrada[2]
                colunaNum = str.lower(coluna)
                colunaNum = ord(colunaNum) - ord("a")
                linha = int(linha) - 1

                if linha > 9 or linha < 0 or colunaNum > 9 or colunaNum < 0:
                    print("Jogada no formato inválido!")

                elif tabuleiroBool[linha][colunaNum] and tabuleiro[linha][colunaNum] != 0:
                    simNao = certeza("\nVocê tem certeza que deseja apagar essa célula? ")
                    if simNao == "s":
                        print("\nApagando linha", linha, "coluna", coluna + ".")
                        tabuleiro[linha][colunaNum] = 0
                        print_tabuleiro(tabuleiro, tabuleiroBool)
                    else:
                        print("A célula não foi alterada.")
                elif not tabuleiroBool[linha][colunaNum]:
                    print("Não é possível apagar uma célula-dica!")
                    
                else:
                    print("A célula escolhida já é vazia...")

            # Condições que implementam o comando de saber quais números podem ser colocados em uma célula [?]:
            elif entrada[0] == "?" and entrada[1].isalpha() and entrada[2].isnumeric():
                coluna, linha = entrada[1], entrada[2]
                colunaNum = str.lower(coluna)
                colunaNum = ord(colunaNum) - ord("a")
                linha = int(linha) - 1

                resposta = []
                numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                if not tabuleiroBool[linha][colunaNum]:
                    print("Essa célula é uma dica\n")
                else:
                    for i in range(9):
                        if check(tabuleiro, colunaNum, linha, numeros[i]):
                            resposta.append(numeros[i])

                    print("\nOs números possíveis para esta célula são:\n")
                    print(resposta)
                    print("\n")
            
            # Jogada no formato "<coluna>, <linha> : <numero>":
            elif entrada[0].isalpha() and entrada[1].isnumeric() and entrada[2].isnumeric():
                coluna, linha, numero = entrada[0], entrada[1], entrada[2]
                linha = int(linha) - 1
                numero = int(numero)

                coluna = str.lower(coluna)
                coluna = ord(coluna) - ord("a")

                if numero > 9 or numero < 1 or linha > 8 or \
                linha < 0 or coluna > 8 or coluna < 0 or entrada == " ":
                    print("\nJogada no formato inválido!")
                
                elif not tabuleiroBool[linha][coluna]:
                    print("\nA jogada é inválida!\nNão se pode substituir um número-dica.")

                elif tabuleiro[linha][coluna] == numero:
                    print("\nA jogada não mudará o tabuleiro...\n")
                
                elif not check(tabuleiro, coluna, linha, numero):
                    print("\nA jogada é inválida!\nA jogada fere as regras do jogo.")
                
                elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] == 0:
                    print("\nJogada válida!\n")
                    tabuleiro[linha][coluna] = numero
                    fun.sleep(1)
                    limpar_terminal()
                    print_tabuleiro(tabuleiro, tabuleiroBool)
                
                elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] != 0:
                    simNao = certeza("\nA jogada é válida, mas a célula escolhida já está preenchida, "
                                "deseja substituí-la? (s/n)\n")
                    if simNao == "s":
                        tabuleiro[linha][coluna] = numero
                        print("\nSubstituindo...\n")
                        fun.sleep(1)
                        limpar_terminal()
                        print_tabuleiro(tabuleiro, tabuleiroBool)
                    else:
                        print("A célula foi mantida!\n")
            
            else:
                print("\nJogada no formato inválido!")
                flag4 = True
                
        else:
            print("\nJogada no formato inválido!")
            flag4 = True

        i = 0
        flag2 = False
        while i < 9 and not flag2:
            j = 0
            while j < 9 and not flag2:
                if tabuleiro[i][j] == 0:    
                    flag2 = True
                j += 1
            i += 1
        contador += 1

    print("JOGO CONCLUIDO")
    print("PARABENS!!")
    
    # Modo Interativo (Fim).
        
elif len(sys.argv) == 3:
    # Modo Batch (Inicio)

    # Ler o arquivo de dicas e validá-lo e montar o tabuleiro com as dicas lidas (Já feito fora dessa condicional na linha 184)

    # Ler o arquivo de jogadas e armazenar as jogadas em uma lista
    arquivo2 = sys.argv[2]
    lista_de_jogadas = []
    lista_de_jogadas = ler_jogadas(arquivo2, lista_de_jogadas)


    # Percorrer a lista de jogadas validando cada jogada uma a uma, e salvando as inválidas em uma lista separada
    lista_de_jogadas_erradas = []

    for jogada in lista_de_jogadas:

        entrada = jogada

        if entrada[0].isalpha() and entrada[1].isnumeric() and entrada[2].isnumeric():
            coluna, linha, numero = entrada[0], entrada[1], entrada[2]
            linha = int(linha) - 1
            numero = int(numero)

            coluna = str.lower(coluna)
            coluna = ord(coluna) - ord("a")

            if numero > 9 or numero < 1 or linha > 8 or \
            linha < 0 or coluna > 8 or coluna < 0 or entrada == " ":
                lista_de_jogadas_erradas.append(entrada)
            
            elif not tabuleiroBool[linha][coluna]:
                lista_de_jogadas_erradas.append(entrada)
            
            elif not check(tabuleiro, coluna, linha, numero):
                lista_de_jogadas_erradas.append(entrada)
            
            elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] == 0:
                tabuleiro[linha][coluna] = numero
                
            
            elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] != 0:
                tabuleiro[linha][coluna] = numero
            
            else:
                lista_de_jogadas_erradas.append(entrada)

    # Checando se a grade foi preenchida ou não
    nao_terminou = False
    i = 0
    while i < 9 and not nao_terminou:
        j = 0
        while j < 9 and not nao_terminou:
            if tabuleiro[i][j] == 0:
                nao_terminou = True
            j += 1
        i += 1
        


    # Printando as jogadas erradas
    for jogada in lista_de_jogadas_erradas:

        entrada = jogada

        coluna, linha, numero = entrada[0], entrada[1], entrada[2]

        print(f"A jogada ({coluna}, {linha}) = {numero} eh invalida!")

    # Printando se a grade foi preenchida ou não
    if True:
        print("A grade foi preenchida com sucesso!")
    else:
        print("A grade nao foi preenchida!")

    #Modo Batch (Fim)

#### FIM DO CODIGO ####