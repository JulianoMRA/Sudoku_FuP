import sys
import re

# Funções de utilidade:
def exibir_grade(grade):
    print("    A   B   C    D   E   F    G   H   I")
    print(" ++---+---+---++---+---+---++---+---+---++")
    for i, linha in enumerate(grade):
        linha_str = f"{i+1}||"
        for j, valor in enumerate(linha):
            linha_str += f" {valor if valor != 0 else ' '} |"
            if j in [2, 5]:
                linha_str += "|"
        linha_str += f"|{i+1}"
        print(linha_str)
        print(" ++---+---+---++---+---+---++---+---+---++")
    print("    A   B   C    D   E   F    G   H   I")

def valida_entrada(celulas):
    # Valida as pistas fornecidas
    for i in range(9):
        for j in range(9):
            num = celulas[i][j]
            if num != 0:
                for k in range(9):
                    if (celulas[i][k] == num and k != j) or (celulas[k][j] == num and k != i):
                        return False
                x, y = 3 * (i // 3), 3 * (j // 3)
                for k in range(3):
                    for l in range(3):
                        if celulas[x + k][y + l] == num and (x + k, y + l) != (i, j):
                            return False
    return True

def possibilidades(celulas, linha, coluna):
    numeros_possiveis = set(range(1, 10))
    for i in range(9):
        numeros_possiveis.discard(celulas[linha][i])
        numeros_possiveis.discard(celulas[i][coluna])
    x, y = 3 * (linha // 3), 3 * (coluna // 3)
    for i in range(3):
        for j in range(3):
            numeros_possiveis.discard(celulas[x + i][y + j])
    return numeros_possiveis

# Inicializando a grade
grade = [[0 for _ in range(9)] for _ in range(9)]
pistas_iniciais = set()

# Checando o número de argumentos
if len(sys.argv) == 2:
    # Modo Interativo
    arquivo_pistas = sys.argv[1]

    # Lendo o arquivo de pistas
    with open(arquivo_pistas, 'r') as f:
        for linha in f:
            correspondencia = re.match(r"([A-I]),\s*([1-9])\s*:\s*([1-9])", linha.strip(), re.I)
            if correspondencia:
                col = ord(correspondencia.group(1).upper()) - ord('A')
                lin = int(correspondencia.group(2)) - 1
                num = int(correspondencia.group(3))
                grade[lin][col] = num
                pistas_iniciais.add((lin, col))

    # Mostrando a grade inicial
    exibir_grade(grade)

    # Validando as pistas iniciais
    if not valida_entrada(grade):
        print("Configuracao de dicas invalida.")
        sys.exit()

    # Loop de jogadas do usuário
    while True:
        jogada = input("Digite sua jogada (ou comando ?<col>,<lin> ou !<col>,<lin>): ").strip()
        
        if jogada.startswith("?"):
            correspondencia = re.match(r"\?([A-I]),\s*([1-9])", jogada.strip(), re.I)
            if correspondencia:
                col = ord(correspondencia.group(1).upper()) - ord('A')
                lin = int(correspondencia.group(2)) - 1
                if (lin, col) not in pistas_iniciais:
                    possiveis = possibilidades(grade, lin, col)
                    print(f"Possíveis valores para {correspondencia.group(1).upper()},{lin+1}: {sorted(possiveis)}")
                else:
                    print("Essa célula contém uma pista e não pode ser alterada.")
            continue
        
        if jogada.startswith("!"):
            correspondencia = re.match(r"!([A-I]),\s*([1-9])", jogada.strip(), re.I)
            if correspondencia:
                col = ord(correspondencia.group(1).upper()) - ord('A')
                lin = int(correspondencia.group(2)) - 1
                if (lin, col) in pistas_iniciais:
                    print("Essa célula contém uma pista e não pode ser apagada.")
                elif grade[lin][col] == 0:
                    print("Essa célula já está vazia.")
                else:
                    grade[lin][col] = 0
                    exibir_grade(grade)
            continue
        
        correspondencia = re.match(r"([A-I]),\s*([1-9])\s*:\s*([1-9])", jogada.strip(), re.I)
        if correspondencia:
            col = ord(correspondencia.group(1).upper()) - ord('A')
            lin = int(correspondencia.group(2)) - 1
            num = int(correspondencia.group(3))

            if (lin, col) in pistas_iniciais:
                print("Essa célula contém uma pista e não pode ser alterada.")
            elif grade[lin][col] != 0:
                sobrescrever = input(f"A célula {correspondencia.group(1).upper()},{lin+1} já está preenchida com {grade[lin][col]}. Deseja sobrescrever? (s/n): ").strip().lower()
                if sobrescrever != 's':
                    continue
            
            # Validando a jogada
            grade[lin][col] = num
            if not valida_entrada(grade):
                print(f"A jogada ({correspondencia.group(1).upper()},{lin+1}) = {num} eh invalida!")
                grade[lin][col] = 0
            else:
                exibir_grade(grade)

            # Verificando se a grade foi preenchida
            if all(all(valor != 0 for valor in linha) for linha in grade):
                print("A grade foi preenchida com sucesso!")
                break

elif len(sys.argv) == 3:
    # Modo Batch
    arquivo_pistas = sys.argv[1]
    arquivo_jogadas = sys.argv[2]

    # Lendo o arquivo de pistas
    pistas_validas = True
    with open(arquivo_pistas, 'r') as f:
        for linha in f:
            correspondencia = re.match(r"([A-I]),\s*([1-9])\s*:\s*([1-9])", linha.strip(), re.I)
            if correspondencia:
                col = ord(correspondencia.group(1).upper()) - ord('A')
                lin = int(correspondencia.group(2)) - 1
                num = int(correspondencia.group(3))
                if grade[lin][col] != 0:
                    pistas_validas = False
                    break
                grade[lin][col] = num
                pistas_iniciais.add((lin, col))

    if not pistas_validas or not valida_entrada(grade):
        print("Configuracao de dicas invalida.")
        sys.exit()

    # Lendo o arquivo de jogadas
    jogadas_invalidas = []
    with open(arquivo_jogadas, 'r') as f:
        for linha in f:
            correspondencia = re.match(r"([A-I]),\s*([1-9])\s*:\s*([1-9])", linha.strip(), re.I)
            if correspondencia:
                col = ord(correspondencia.group(1).upper()) - ord('A')
                lin = int(correspondencia.group(2)) - 1
                num = int(correspondencia.group(3))
                
                if (lin, col) in pistas_iniciais or grade[lin][col] != 0:
                    jogadas_invalidas.append(f"A jogada ({correspondencia.group(1).upper()},{lin+1}) = {num} eh invalida!")
                else:
                    grade[lin][col] = num
                    if not valida_entrada(grade):
                        jogadas_invalidas.append(f"A jogada ({correspondencia.group(1).upper()},{lin+1}) = {num} eh invalida!")
                        grade[lin][col] = 0

    # Exibindo as jogadas inválidas
    for jogada_invalida in jogadas_invalidas:
        print(jogada_invalida)

    # Verificando se a grade foi preenchida com sucesso
    if all(all(valor != 0 for valor in linha) for linha in grade) and len(jogadas_invalidas) == 0:
        print("A grade foi preenchida com sucesso!")
    else:
        print("A grade nao foi preenchida!")

else:
    print("Número de argumentos inválido. Use:\n  - Modo Interativo: python3 sudoku.py <arquivo_pistas>\n  - Modo Batch: python3 sudoku.py <arquivo_pistas> <arquivo_jogadas>")
