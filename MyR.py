import sys
import pprint
sys.path.insert(0,"../..")

import MyRLex
import MyRCubo
import MyRParse

def imprimir_producto():
    pp = pprint.PrettyPrinter(indent=4)
    print('TABLA DE SÍMBOLOS:')
    pp.pprint(MyRParse.tabla_simbolos)
    print('TABLA DE CONSTANTES:')
    pp.pprint(MyRParse.constantes)
    print('LIST DE OPERACIONES:')
    pp.pprint(MyRParse.operaciones)
    print('TABLA DE DATOS:')
    pp.pprint(MyRParse.valores)
    print('TABLA DE TIPOS DE MEMORIAS:')
    pp.pprint(MyRParse.tipos)
    print('QUADRUPLETS:')
    pp.pprint(MyRParse.quadruple)

fileToRead = sys.argv[1]
file = open(fileToRead, 'r')
data = file.read()
imprimir_producto()

prog = MyRParse.parse(data)

file.close()
