# Função para gerar e imprimir o tabuleiro (onde tem 0, fica vazio):

def print_tabuleiro(tabuleiro):
  print("     A   B   C    D   E   F    G   H   I")
  for i in range(9):
    if i == 3 or i == 6:
        print("  ++===+===+===++===+===+===++===+===+===++")
    else:
        print("  ++---+---+---++---+---+---++---+---+---++")
    print(i + 1, "||", end = " ")

    for j in range(9):
      if tabuleiro[i][j] != 0:
        print(tabuleiro[i][j], end = " ")
      else:
        print(" ", end = " ")

      if j < 8:

        if j == 2 or j == 5:
          print("||", end = " ")
        else:
          print("|", end = " ")
    print("||", end = " ")
    print(end = "\n")
  print("  ++---+---+---++---+---+---++---+---+---++")

# Função que verifica se um número pode ser colocado em um determinado quadrante:

def check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
  for i in range(3):
    for j in range(3):
      if tabuleiro[i_inicial + i][j_inicial + j] == numero:
        return True

# Função que verifica se um número pode ser colocado em uma célula[linha][coluna]:
def check(tabuleiro, coluna, linha, numero):
  i_inicial = linha // 3 * 3
  j_inicial = coluna // 3 * 3
  
  for i in range(9):
    if tabuleiro[i][coluna] == numero or \
    tabuleiro[linha][i] == numero or \
    check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
      return False
  return True

# Enquanto não conseguimos ler o arquivo de dicas, vamos gerar um sudoku "na marra":

tabuleiro = [[0 for i in range(9)] for i in range(9)]
tabuleiro[0][0] = 9
tabuleiro[0][1] = 8
tabuleiro[0][2] = 5
tabuleiro[0][3] = 4
tabuleiro[0][5] = 1
tabuleiro[1][4] = 3
tabuleiro[2][0] = 1
tabuleiro[2][2] = 6
tabuleiro[3][3] = 5
tabuleiro[4][0] = 4
tabuleiro[4][2] = 2
tabuleiro[4][5] = 9
tabuleiro[4][8] = 3
tabuleiro[5][1] = 9
tabuleiro[5][4] = 6
tabuleiro[5][5] = 3
tabuleiro[5][6] = 4
tabuleiro[6][1] = 6
tabuleiro[6][4] = 1
tabuleiro[7][3] = 3
tabuleiro[7][5] = 6
tabuleiro[7][8] = 5
tabuleiro[8][0] = 2
tabuleiro[8][4] = 8
tabuleiro[8][8] = 1

# Versão em Bool do tabuleiro que irá verificar a cada jogada se aquela jogada é em cima de um número que foi dado como dica:

tabuleiroBool = [[True for i in range(9)] for i in range(9)]
for i in range(9):
  for j in range(9):
    if tabuleiro[i][j] != 0:
      tabuleiroBool[i][j] = False
print_tabuleiro(tabuleiro)

# Interatividade do sistema (Início): 

contador = 0
flag2 = True
while flag2:
  
  if contador == 0:
    entrada = input("Entre com uma jogada: ")
  else:
    entrada = input("Próxima jogada! ")

  # Condições que implementam o comando de apagar uma célula:

  if entrada[0] == "!":
    entrada = entrada.replace("!", "")
    entrada = entrada.replace(",", " ")
    coluna, linha = entrada.split()
    colunaNum = str.lower(coluna)
    colunaNum = ord(colunaNum) - ord("a")
    linha = int(linha) - 1

    if linha > 9 or linha < 0 or colunaNum > 9 or colunaNum < 0:
      print("Jogada no formato inválido!")

    elif tabuleiroBool[linha][colunaNum] and tabuleiro[linha][colunaNum] != 0: 
      print("Apagando linha", linha, "coluna", coluna)
      tabuleiro[linha][colunaNum] = 0
      print_tabuleiro(tabuleiro)
      
    elif not tabuleiroBool[linha][colunaNum]:
      print("Não é possível apagar uma célula-dica!")
      
    else:
      print("A célula escolhida já é vazia...")

  # Condições que implementam o comando de saber quais números podem ser colocados em uma célula:

  elif entrada[0] == "?":
    entrada = entrada.replace("?", "")
    entrada = entrada.replace(",", " ")
    coluna, linha = entrada.split()
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
    
    # A entrada será no formato "<coluna>, <linha> : <numero>", então primeiro vamos dar replace em tudo:

  else:
    entrada = entrada.replace(":", " ")
    entrada = entrada.replace(",", " ")
    
    # Vamos utilizar .split para "partir", e .strip para retirar os espaços extras:
    
    coluna, linha, numero = entrada.split()
    linha = linha.strip()
    linha = int(linha) - 1
    numero = numero.strip()
    numero = int(numero)
    coluna = coluna.strip()

    # Agora precisamos converter a coluna de uma letra para um número.
    # Função ord retorna o valor unicode do char, no caso do A é 65:

    coluna = str.lower(coluna)
    coluna = ord(coluna) - ord("a")

    if numero > 9 or numero < 0 or linha > 9 or \
    linha < 0 or coluna > 9 or coluna < 0 or entrada == " ":
      print("\nJogada no formato inválido!")
    
    elif not tabuleiroBool[linha][coluna]:
      print("\nA jogada é inválida!\nNão se pode substituir um número-dica.")

    elif tabuleiro[linha][coluna] == numero:
      print("\nA jogada não mudará o tabuleiro...\n")
      
    elif not check(tabuleiro, coluna, linha, numero):
      print("\nA jogada é inválida!\nA jogada fere as regras do jogo.")
      
    elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and \
    tabuleiro[linha][coluna] == 0:
      print("\nJogada válida!\n")
      tabuleiro[linha][coluna] = numero
      print_tabuleiro(tabuleiro)
    
    elif check(tabuleiro, coluna, linha, numero) and tabuleiroBool[linha][coluna] and \
    tabuleiro[linha][coluna] != 0:
      simNao = input("\nA jogada é válida, mas a célula escolhida já está preenchida, "
        "deseja substituí-la? (s/n)\n")
      simNao = str.lower(simNao).strip()
      if simNao[0] == "s":
        tabuleiro[linha][coluna] = numero
        print("\nSubstituindo...\n")
        print_tabuleiro(tabuleiro)

      else: 
        print("A célula foi mantida!\n")

  i = 0
  j = 0
  flag2 = False
  while i < 9 and not flag2:
    while j < 9 and not flag2:
      if tabuleiro[i][j] == 0:
        flag2 = True
      j += 1
    i += 1
  contador += 1

# Interatividade do sistema (Fim).