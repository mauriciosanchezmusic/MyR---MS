##Gestor de memorias virtuales y establecimiento de reglas para la formacion de instrucciones.
##Creador del cuadruplo con las memorias gestionadas y operaciones
##Formador del codigo objeto

import sys
import pprint
sys.path.insert(0,"../..")

import MyRLex
import MyRCubo
import MyRMemory
import MyRParse

##Comentar para no incluir cuadruplos
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
    ##Temporales
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
###############################
##Accede al nombre del archivo línea de comandos.
fileToRead = sys.argv[1]
file = open(fileToRead, 'r')
data = file.read()

##Analisis sintactico de ply
prog = MyRParse.parse(data)

##Comentar para no imprimir cuadruplos
print_object()
####################################

##Se crea el nombre del archivo de salida (fileToWrite + '.o') eliminando 
##la extensión del archivo de entrada.
nameSplit = fileToRead.split(".",1)
fileToWrite = nameSplit[0]

with open(fileToWrite + '.o', 'w') as file:
##Se guarda en el archivo de salida un diccionario con las siguientes estructuras de datos importantes 
##Tabla de símbolos, Tabla de vectores, Tabla de constantes y los Cuádruplos.
    save_data = {
        'symbol_table':MyRParse.tabla_simbolos,
        'vector_table':MyRParse.tabla_vectores,
        'constant_table':MyRParse.constantes,
        'quadruple':MyRParse.quadruple,
    }
    file.write(str(save_data))

file.close()
