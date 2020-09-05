# -*- coding: utf-8 -*-

# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado en Agosto 2015)

import sys

# tokens
SYM = 100  # Simbolos (identificadores)
NUM = 101  # Número (entero)
BOO = 102  # Booleanos
STR = 103  # Strings (solo contienen minusculas, espacios y numeros)
LRP = 104  # Delimitador: paréntesis izquierdo
RRP = 105  # Delimitador: paréntesis derecho
END = 106  # Fin de la entrada
ESP = 107  # Delimitador: Espacio
CRT = 108  # Delimitador: Salto de linea
ERR = 400  # Error léxico: palabra desconocida

#h
#t

# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#        dig  char  (    )  raro  esp    #    "  \n   $   
MT = [
        [  2,   1, LRP, RRP,   5, ESP,   3,   4, CRT, END, ], # edo 0 - estado inicial
        [  5,   1, SYM, SYM,   5, SYM, ERR, ERR, SYM, SYM, ], # edo 1 - simbolos
        [  2,   5, NUM, NUM,   5, NUM, ERR, ERR, NUM, NUM, ], # edo 2 - numeros
        [ERR, BOO, ERR, ERR, ERR ,ERR, ERR, ERR, ERR, BOO, ], # edo 3 - booleanos
        [  4,   4,   5,   5,   5,   4,   5, STR,   5,   5, ], # edo 4 - strings
        [  5,   5, ERR, ERR,   5, ERR, ERR,   5, ERR, ERR, ], # edo 5 - Error
     ]


# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado
def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c.isnumeric(): # dígitos
        return 0
    elif c.isalpha() and c.islower() and c != ' ': # chars
        return 1
    elif c == '(': # delimitador (
        return 2
    elif c == ')': # delimitador )
        return 3
    elif c == ' ': # blancos
        return 5
    elif c == '#': # punto
        return 6
    elif c == '"': # quote string
        return 7
    elif c == '\n': # salto de linea
        return 8
    elif c == '$': # Fin de linea
        return 9
    else: # caracter raro
        return 4

_c = None    # siguiente caracter
_leer = True # indica si se requiere leer un caracter de la entrada estándar

# Función principal: implementa el análisis léxico
def obten_token():
    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    global _c, _leer
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if _leer: _c = sys.stdin.read(1)
            else: _leer = True
            edo = MT[edo][filtro(_c)]
            if edo < 100 and edo != 0: lexema += _c
        if edo == SYM:    
            _leer = False # ya se leyó el siguiente caracter
            print("Simbolo", lexema)
            return SYM
        elif edo == NUM:   
            _leer = False # ya se leyó el siguiente caracter
            print("Numero", lexema)
            return NUM
        elif edo == BOO:   
            lexema += _c  # el último caracter forma el lexema
            if _c == 't' or _c == 'f':
                print("Booleano", lexema)
                return BOO
            else:
                leer = False # el último caracter no es raro
                print("ERROR! palabra ilegal", lexema)
                return ERR
        elif edo == STR:   
            lexema += _c  # el último caracter forma el lexema
            print("String", lexema)
            return STR
        elif edo == LRP:  
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador", lexema)
            return LRP
        elif edo == RRP:  
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador", lexema)
            return RRP
        elif edo == ESP:  
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador [ESPACIO]")
            return ESP
        elif edo == CRT:  
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador [SALTO DE LINEA]")
            return CRT
        elif edo == END:
            print("Fin de expresion")
            return END
        else:   
            leer = False # el último caracter no es raro
            print("ERROR! palabra ilegal", lexema)
            return ERR
    

