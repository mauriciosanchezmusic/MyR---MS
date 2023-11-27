import sys
import pprint
sys.path.insert(0,"../..")

import MyRLex
import MyRCubo
import MyRMemory
import MyRParse

def print_object():
    pp = pprint.PrettyPrinter(indent=4)
    print('TABLA DE SÍMBOLOS:')
    pp.pprint(MyRParse.tabla_simbolos)
    print('')
    print('TABLA DE VECTORES:')
    pp.pprint(MyRParse.tabla_vectores)
    print('')
    print('TABLA DE CONSTANTES:')
    pp.pprint(MyRParse.constantes)
    print('')
    print('QUADRUPLE:')
    pp.pprint(MyRParse.quadruple)
    print('')
    print('LAS SIGUIENTES TABLAS SON DE VISUALIZACIÓN Y NO SE ADJUNTAN AL ARCHIVO OBJETO')
    print('TABLA DE OPERADORES')
    pp.pprint(MyRParse.operaciones)
    print('')
    print('TABLA DE DIRECCIONES ASIGNADAS')
    pp.pprint(MyRParse.valores)
    print('')
    print('TABLA DE TIPOS DE MEMORIAS ASIGNADAS')
    pp.pprint(MyRParse.tipos)
    print('')
    print('TABLA DE SALTOS DE INSTRUCCIÓN')
    pp.pprint(MyRParse.saltos)

fileToRead = sys.argv[1]
file = open(fileToRead, 'r')
data = file.read()

prog = MyRParse.parse(data)
print_object()

nameSplit = fileToRead.split(".",1)
fileToWrite = nameSplit[0]

with open(fileToWrite + '.o', 'w') as file:
    save_data = {
        'symbol_table':MyRParse.tabla_simbolos,
        'vector_table':MyRParse.tabla_vectores,
        'constant_table':MyRParse.constantes,
        'quadruple':MyRParse.quadruple,
    }
    file.write(str(save_data))

file.close()
