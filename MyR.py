import sys
import pprint
sys.path.insert(0,"../..")

import MyRLex
import MyRCubo
import MyRParse

def print_object():
    pp = pprint.PrettyPrinter(indent=4)
    print('TABLA DE SÍMBOLOS:')
    pp.pprint(MyRParse.tabla_simbolos)
    print('')
    print('TABLA DE CONSTANTES:')
    pp.pprint(MyRParse.constantes)
    print('')
    print('QUADRUPLE:')
    pp.pprint(MyRParse.quadruple)

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
        'constant_table':MyRParse.constantes,
        'quadruple':MyRParse.quadruple,
    }
    file.write(str(save_data))

file.close()
