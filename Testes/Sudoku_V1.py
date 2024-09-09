tabuleiro = [[0 for i in range(9)] for i in range(9)]
#inicializa o tabuleiro com tudo 0

def print_tabuleiro(tabuleiro):
  #função pra printar o tabuleiro bonitinho
  #onde tem 0 fica vazio
  print("     A   B   C    D   E   F    G   H   I")
  for i in range(9):

    if i == 3 or i == 6:
      print("  ++===+===+===++===+===+===++===+===+===++")
    else:

      print("  ++---+---+---++---+---+---++---+---+---++")

    print(i, "||", end = " ")
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

print_tabuleiro(tabuleiro)

def check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
  #função que verifica se um número pode ser colocado em um determinado quadrante
  for i in range(3):
    for j in range(3):
      if tabuleiro[i_inicial + i][j_inicial + j] == numero:
        return True
        
def check(tabuleiro, coluna, linha, numero):
  #função que verifica se um número pode ser colocado em uma célula[linha][coluna]

  i_inicial = linha // 3 * 3
  j_inicial = coluna // 3 * 3
  
  for i in range(9):
    
    if tabuleiro[i][coluna] == numero or \
    tabuleiro[linha][i] == numero or \
    check_quadrante(tabuleiro, j_inicial, i_inicial, numero):
      return False
    else:
        return True