# Implementación de un parser
# Reconoce expresiones mediante la gramática:
# EXP -> EXP op EXP | EXP -> (EXP) | cte
# la cual fué modificada para eliminar ambigüedad a:
# EXP  -> cte EXP1 | (EXP) EXP1
# EXP1 -> op EXP EXP1 | vacío
# los elementos léxicos (delimitadores, constantes y operadores)
# son reconocidos por el scanner
#
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado Agosto 2015)

import sys
import obten_token as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        token = scanner.obten_token()
    else:
        error("token equivocado")

# Función principal: implementa el análisis sintáctico
def parser():
    global token 
    token = scanner.obten_token() # inicializa con el primer token
    prog()
    if token == scanner.END:
        print("Expresion bien construida!!")
    else:
        error("expresion mal terminada")

def prog():
    if token == scanner.LRP or token == scanner.SYM or token  == scanner.NUM or token == scanner.ESP or token == scanner.CRT or token == scanner.STR or token == scanner.BOO:
        exp()
        prog()
    elif token == scanner.END:
        return
    else:
        error("Expresion mal iniciada!!!!")


# Módulo que reconoce expresiones
def exp():
    if token == scanner.LRP:
        lista()
    elif token == scanner.ESP or token == scanner.CRT:
        match(token)
    else:
        atomo()

def atomo():
    if token == scanner.SYM:
        match(token)
    else:
        constante()

def constante():
    if token == scanner.BOO or token == scanner.STR or token == scanner.NUM:
        match(token)

def elementos():
    if  token != scanner.RRP and token != scanner.ERR:
        exp()
        elementos()

def lista():
    match(scanner.LRP)
    elementos()
    match(scanner.RRP)

# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)
    
parser()
