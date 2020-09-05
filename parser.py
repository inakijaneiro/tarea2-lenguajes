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

# Solución por:
# Sergio Diosdado - A00516971
# Iñaki Janeiro - A00516978

import sys
import obten_token as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        token = scanner.obten_token()
    else:
        error(">>ERROR SINTÁCTICO<<")

# Función principal: implementa el análisis sintáctico
def parser():
    global token 
    token = scanner.obten_token() # inicializa con el primer token
    prog()
    if token == scanner.END:
        print(">>ENTRADA CORRECTA<<")
    else:
        error(">>ERROR SINTÁCTICO<<")

# Parte principal y de arranque de la gramática
def prog():
    print("No terminal <prog>")
    if token == scanner.LRP or token == scanner.SYM or token  == scanner.NUM \
        or token == scanner.ESP or token == scanner.CRT or token == scanner.STR \
        or token == scanner.BOO:
        exp()
        prog()
    elif token == scanner.END:
        return
    else:
        error(">>ERROR SINTÁCTICO<<")


# Módulo que reconoce expresiones
def exp():
    print("No terminal <exp>")
    if token == scanner.LRP:
        lista()
    elif token == scanner.ESP or token == scanner.CRT:
        match(token)
    else:
        atomo()

# Mapa de la gramática que expresa una parte atómica de una expresión atomo -> SYMBOL | <lista>
def atomo():
    print("No terminal <atomo>")
    if token == scanner.SYM:
        match(token)
    else:
        constante()

# Mapa de la gramatica que se encarga de las literales. constante -> NUM | BOOL | STRING
def constante():
    print("No terminal <constante>")
    if token == scanner.BOO or token == scanner.STR or token == scanner.NUM:
        match(token)

# Mapa de la gramática elementos -> <exp> <elementos> | vacio
def elementos():
    print("No terminal <elementos>")
    if  token != scanner.RRP and token != scanner.ERR and token != scanner.END:
        exp()
        elementos()

# Detecta la secuencia de una lista - lista -> ( elementos )
def lista():
    print("No terminal <lista>")
    match(scanner.LRP)
    elementos()
    match(scanner.RRP)

# Termina con un mensaje de error
def error(mensaje):
    print(mensaje)
    sys.exit(1)
    
parser()
