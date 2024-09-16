# Edileudo Maciel Moreira Filho | Matrícula: 567234
# Juliano Melo Rodrigues Alencar | Matrícula: 565760
# Gabriel Matias ... | Matrícula:

### ESTE ARQUIVO CONTÉM O PROGRAMA NO MODO INTERATIVO E MODO BATCH ###
import sys
import fun

#### INICIO DO CODIGO ####

# Condição que verifica a quantidade de argumentos fornecidos no comando inicial: 
if not 2 <= len(sys.argv) <= 3:
    print("""A quantidade de arquivos não condiz com nenhum modo de jogo!
          
Para acessar o Modo Interativo insira:
          
    python sudoku.py <arquivo_de_pistas.txt>
          
Para acessar o Modo Batch insira:
          
    python sudoku.py <arquivo_de_pistas.txt> <arquivo_de_jogadas.txt>
          """)


# Inicializando o tabuleiro e tabuleiroBool:
else:
    tabuleiro = [[0 for _ in range(9)] for _ in range(9)]
    tabuleiroBool = [[True for _ in range(9)] for _ in range(9)]

    # Capturando o nome do arquivo da linha de comando:
    arquivo = sys.argv[1]

    flag2 = True

    # Ler o arquivo de pistas e preencher o tabuleiro:
    flag3 = fun.ler_pistas(arquivo, tabuleiro)
    if flag3:
        flag2 = False
        print("Arquivo de pistas inválido!")
    # Exibe a mensagem:
    else:
        fun.mensagem_inicial() 
    # Atualizando o tabuleiroBool para marcar as pistas como imutáveis:
    for i in range(9):
        for j in range(9):
            if tabuleiro[i][j] != 0:
                tabuleiroBool[i][j] = False


# Verifica se é o modo interativo:
if len(sys.argv) == 2:


    # Modo Interativo (INÍCIO):
    contador = 0
    flag4 = False

    while flag2:

        if contador == 0:
            # Exibir o tabuleiro inicial:
            fun.print_tabuleiro(tabuleiro, tabuleiroBool)
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

        # Verificando se a entrada é válida:
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
                    simNao = fun.certeza("\nVocê tem certeza que deseja apagar essa célula? ")
                    if simNao == "s":
                        print("\nApagando linha", linha, "coluna", coluna + ".")
                        tabuleiro[linha][colunaNum] = 0
                        fun.print_tabuleiro(tabuleiro, tabuleiroBool)
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
                        if fun.check(tabuleiro, colunaNum, linha, numeros[i]):
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
                
                elif not fun.check(tabuleiro, coluna, linha, numero):
                    print("\nA jogada é inválida!\nA jogada fere as regras do jogo.")
                
                elif fun.check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] == 0:
                    print("\nJogada válida!\n")
                    tabuleiro[linha][coluna] = numero
                    fun.sleep(1)
                    fun.limpar_terminal()
                    fun.print_tabuleiro(tabuleiro, tabuleiroBool)
                
                elif fun.check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] != 0:
                    simNao = fun.certeza("\nA jogada é válida, mas a célula escolhida já está preenchida, "
                                "deseja substituí-la? (s/n)\n")
                    if simNao == "s":
                        tabuleiro[linha][coluna] = numero
                        print("\nSubstituindo...\n")
                        fun.sleep(1)
                        fun.limpar_terminal()
                        fun.print_tabuleiro(tabuleiro, tabuleiroBool)
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
    
    # Modo Interativo (FIM).


    # Modo Batch (INÍCIO):
elif len(sys.argv) == 3:
    

    # Ler o arquivo de pistas e validá-lo e montar o tabuleiro com as pistas lidas (Já foi feito anteriormente)
    # Ler o arquivo de jogadas e armazenar as jogadas em uma lista:
    arquivo2 = sys.argv[2]
    lista_de_jogadas = []
    lista_de_jogadas = fun.ler_jogadas(arquivo2, lista_de_jogadas)


    # Percorrer a lista de jogadas validando cada jogada uma a uma, e salvando as inválidas em uma lista separada:
    lista_de_jogadas_erradas = []

    for jogada in lista_de_jogadas:

        entrada = jogada
        if entrada:
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
                
                elif not fun.check(tabuleiro, coluna, linha, numero):
                    lista_de_jogadas_erradas.append(entrada)
                
                elif fun.check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] == 0:
                    tabuleiro[linha][coluna] = numero
                    
                
                elif fun.check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and tabuleiro[linha][coluna] != 0:
                    tabuleiro[linha][coluna] = numero
                
                else:
                    lista_de_jogadas_erradas.append(entrada)


    # Checando se a grade foi preenchida ou não:
    nao_terminou = False
    i = 0
    while i < 9 and not nao_terminou:
        j = 0
        while j < 9 and not nao_terminou:
            if tabuleiro[i][j] == 0:
                nao_terminou = True
            j += 1
        i += 1


    fun.print_tabuleiro(tabuleiro, tabuleiroBool)
    print(" ")

    # Printando as jogadas erradas:
    for jogada in lista_de_jogadas_erradas:

        entrada = jogada

        coluna, linha, numero = entrada[0], entrada[1], entrada[2]

        print(f"A jogada ({coluna}, {linha}) = {numero} eh invalida!")


    # Printando se a grade foi preenchida ou não:
    if nao_terminou:
        print("")
        print("A grade nao foi preenchida!")
    else:
        fun.mensagem_final()

    # Modo Batch (FIM)
#### FIM DO CODIGO ####
