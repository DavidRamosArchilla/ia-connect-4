tablero = [[], [], [], [], [], [], []]

jugador_actual = 'X'  # persona

ALTURA_MAXIMA = 7



def cambiar_jugador():
    if jugador_actual == 'X':
        return 'O'
    else:
        return 'X'


def meter_ficha(columna):
    if (len(tablero[columna]) < ALTURA_MAXIMA):
        tablero[columna].append(jugador_actual)


def hay_ganador():
    cont = 1
    # columnas
    for columna in tablero:
        ficha_ant = ''
        for ficha in columna:
            if ficha_ant == ficha:
                cont += 1
            else:
                cont = 1
            if cont == 4:
                return ficha
            ficha_ant = ficha
    # filas
    filas = get_filas()
    posible_ganador_filas = hay_4_seguidos(filas)
    if posible_ganador_filas is not None:
        return posible_ganador_filas

    # diagonales
    # daigonales hacia la derecha
    diagonales = get_diagonales()
    posible_ganador_diag = hay_4_seguidos(diagonales)
    if posible_ganador_diag is not None:
        return posible_ganador_diag
    return '-'


def imprimir_tablero():
    filas = get_filas()
    for fila in filas[::-1]:
        print("|", end='')
        for item in fila:
            print(item + "|", end='')
        print('')
    print("|0|1|2|3|4|5|6|")


def get_filas():
    filas = []
    for i in range(ALTURA_MAXIMA):
        fila = [columna[i] if i < len(columna) else '-' for columna in tablero]
        filas.append(fila)
    return filas

def get_diagonales():
    filas = get_filas()
    # daigonales hacia la derecha
    diagonales = []
    for i in range(ALTURA_MAXIMA):
        diagonal_arriba = [filas[j + i][j] for j in range(ALTURA_MAXIMA) if i + j < ALTURA_MAXIMA]
        diagonal_abajo = [filas[j][j + i] for j in range(ALTURA_MAXIMA) if i + j < len(tablero)]
        if i != 0 and len(diagonal_abajo) > 3:
            diagonales.append(diagonal_abajo)
        diagonales.append(diagonal_arriba)

        # diagonales hacia la izquierda
    for i in range(ALTURA_MAXIMA):
        diagonal_arriba = [filas[j][-j - 1 - i] for j in range(ALTURA_MAXIMA) if -j - 1 - i >= -7]
        diagonal_abajo = [filas[j + i][-j - 1] for j in range(ALTURA_MAXIMA) if j + i < ALTURA_MAXIMA]
        diagonales.append(diagonal_abajo)
        if i != 0 and len(diagonal_arriba) > 3:  # para que no se duplique la primera diagonal
            diagonales.append(diagonal_arriba)
    return diagonales

def hay_4_seguidos(lineas):
    cont = 1
    for fila in lineas:
        ficha_ant = ''
        for ficha in fila:
            if ficha_ant != '-' and ficha_ant == ficha:
                cont += 1
            else:
                cont = 1
            if cont == 4:
                return ficha
            ficha_ant = ficha

def get_abiertos():
    return [i for i in range(len(tablero)) if len(tablero[i]) < ALTURA_MAXIMA]

def minimax(profundidad,jugador):
    ganador = hay_ganador()
    if ganador == 'X':
        return -1000000,None
    if ganador == 'O':
        return 1000000,None
    if profundidad == 0:
        return valorar_tablero(),None
    if jugador == 'O':
        val = -1000000
        abiertos = get_abiertos()
        posicion_mejor = 0
        mejor_valor = -1000000
        valores = []
        for pos in abiertos:
            tablero[pos].append(jugador)
            val = max(val, minimax(profundidad-1,'X')[0])
            tablero[pos].pop()
            if val > mejor_valor:
                mejor_valor = val
                posicion_mejor = pos
            valores.append(val)
        return val,posicion_mejor
    else:
        val2 = 1000000
        abiertos = get_abiertos()
        for pos in abiertos:
            tablero[pos].append(jugador)
            val2 = min(val2, minimax(profundidad - 1,'O')[0])
            tablero[pos].pop()

        return val2,None



def heuristico():
    #sobre el tablero acutal
    valor = 0
    filas = get_filas()
    diagonales = get_diagonales()
    columnas = [[fila[i] for fila in filas] for i in range(len(filas[0]))]
    lineas = diagonales + filas + columnas
    for linea in lineas:
        valor += heuristico_linea(linea)

def heuristico_linea(linea):
    cont_x=0
    cont_o=0

    for ficha in linea:
        pass



def valorar_tablero():
    puntuacion = 0

    filas = get_filas()
    diagonales = get_diagonales()
    columnas = [[fila[i] for fila in filas] for i in range(len(filas[0]))]
    lineas = diagonales + filas + columnas
    for fila in lineas:
        maq = 0
        per = 0
        hue = 0
        segmaq = 0
        segper = 0
        seghue = 0
        for elemento in fila:
            if elemento == 'O':
                maq += 1
                segmaq += 1
                if (per > 0):
                    hue=seghue
                else:
                    hue += seghue
                per=0
                seghue=0
                segper=0
            if (elemento == 'X') :
                per += 1
                segper += 1
                if (maq > 0):
                    hue=seghue
                else:
                    hue += seghue
                maq=0
                seghue=0
                segmaq=0
            if (elemento == '-'):
                seghue += 1
                segmaq=0
                segper=0
            if (segmaq+hue+seghue >= 4):
                puntuacion += valoraTira(segmaq, maq, seghue, hue)
            if (segper+hue+seghue >= 4):
                puntuacion -= valoraTira(segper, per, seghue, hue)

    return puntuacion

def valoraTira(numFichasSeguidas, numFichas,numHuecosSeguidos,numHuecos):
        PESOS_PUNTUACION=[0,10,100,10000,1000000,1000000,1000000]
        if (numFichas+numHuecos)>=4:
            return PESOS_PUNTUACION[numFichasSeguidas]+10*numFichas+3*numHuecosSeguidos+numHuecos
        else:
            return 0


imprimir_tablero()
while True:
    if jugador_actual == 'X':
        try:
            columna = int(input("juegan" + jugador_actual + " : "))
            meter_ficha(columna)
        except:
            continue
    else:
        tupla = minimax(4, 'O')
        print(tupla[0])
        meter_ficha(tupla[1])
    imprimir_tablero()
    posible_ganador = hay_ganador()
    if posible_ganador != '-':
        print("Ganan " + jugador_actual)
        break
    jugador_actual = cambiar_jugador()

