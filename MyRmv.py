import sys
import statistics

## +++++++++++++  LEER ARCHIVO OBJETO GENERADO POR COMPILADOR  +++++++++++
nameFile = sys.argv[1]
with open(nameFile, 'r') as file:
    global tabla_simbolos, tabla_vectores, quadruple, constantes
    data = file.read()
    entrada = eval(data)
    tabla_simbolos_in = entrada['symbol_table']
    tabla_vectores_in = entrada['vector_table']
    quadruple_in = entrada['quadruple']
    const_in = entrada['constant_table']

## ++++++++++++  LEER Y ASIGNAR MEMORIAS PARA DIRECCIONES LOCALES Y GLOBALES
global memoriaG, memoriaL, memoriaV, const_finales, funcion_actual
memoriaG       = {}
memoriaL       = []
memoriaV       = {}
const_finales  = {}
funcion_actual = 'main'

lista_vectores = [];

## ++++++++++++  INSTRUCCIONES PARA TRANSPONER LA TABLA DE CONSTANTES
for key, val in const_in.items():
    const_finales[val['address']] = key

global actual

## ++++++++++++++ INSTRUCCIONES PARA CREAR LISTA  ++++++++++++++++++++++++
def crear_lista(name, addr, qty):
    for direc in range(0, qty):
        address = addr + direc
        valor = leer_mem(address)
        lista_vectores.append(valor)

## ++++++++++++ INSTRUCCIONES PARA LEER LOS VALORES EN LA MEMORIA
def leer_mem(direccion, prof=-1):
    dir_t = int(direccion)
    val = None

    # direcciones globales
    if dir_t >= 1000 and dir_t < 3000:
        val = int(memoriaG.get(direccion, None))
    elif dir_t >= 3000 and dir_t < 5000:
        val = float(memoriaG.get(direccion, None))
    elif dir_t >= 5000 and dir_t < 7000:
        val = int(memoriaG.get(direccion, None))
    elif dir_t >= 7000 and dir_t < 8000:
        val = str(memoriaG.get(direccion, None))
    # direcciones locales
    elif dir_t >= 8000 and dir_t < 10000:
        val = int(memoriaL[prof].get(direccion, None))
    elif dir_t >= 10000 and dir_t < 12000:
        val = float(memoriaL[prof].get(direccion, None))
    elif dir_t >= 12000 and dir_t < 14000:
        val = int(memoriaL[prof].get(direccion, None))
    elif dir_t >= 14000 and dir_t < 15000:
        val = str(memoriaL[prof].get(direccion, None))
    # direcciones de vector
    elif dir_t >= 30000 and dir_t < 39000:
        val = int(memoriaV.get(direccion, None))
    elif dir_t >= 40000 and dir_t < 49000:
        val = float(memoriaV.get(direccion, None))
    elif dir_t >= 50000 and dir_t < 59000:
        val = str(memoriaV.get(direccion, None))
    # direcciones de constantes
    elif dir_t >= 15000 and dir_t < 17000:
        val = int(const_finales.get(direccion, None))
    elif dir_t >= 17000 and dir_t < 19000:
        val = float(const_finales.get(direccion, None))
    elif dir_t >= 19000 and dir_t < 20000:
        val = str(const_finales.get(direccion, None))
    elif dir_t >= 20000 and dir_t < 21000:
        val = str(const_finales.get(direccion, None))

    if val is None:
        error('ACCESO A UNA VARIABLE NO ASIGNADA')
        actual = -1
        return
    return val

## ++++++++++++  INSTRUCCIONES PARA ASIGNAR VALORES A LAS MEMORIAS
def escribir_mem(direccion, valor, prof=-1):
    global memoriaG, memoriaL
    dir_t = int(direccion)

    if dir_t >= 8000 and dir_t < 12000:
        memoriaL[prof][dir_t] = valor
    elif dir_t >= 20000 and dir_t < 21000:
        memoriaL[prof][dir_t] = valor
    elif dir_t >= 30000 and dir_t < 59000:
        memoriaV[dir_t] = valor
    else:
        memoriaG[dir_t] = valor

## ++++++++++++  MANEJO DE LAS INSTRUCCIONES DEL COMPILADOR
actual = [0]
while actual[-1] != -1:
    # Leer el quadruple
    if quadruple_in[actual[-1]][0] == 'START':
        memoriaL.append({})
        actual[-1] = quadruple_in[actual[-1]][3]
    elif quadruple_in[actual[-1]][0] == 'END':
        actual[-1] = -1
        
    # operacion suma y resta
    elif quadruple_in[actual[-1]][0] == '+':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        res = val1 + val2
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '-':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        res = val1 - val2
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
        
    # operacion multiplicación, división y potencia
    elif quadruple_in[actual[-1]][0] == '*':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        res = val1 * val2
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '#':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val2 == 0:
            error("NO SE PUEDE HACER LA DIVISIÓN PORQUE ES UNA DIVISION ENTRE 0")
            actual[-1] = -1
        else:
            res = val1 // val2
            escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '/':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val2 == 0:
            error("NO SE PUEDE HACER LA DIVISIÓN PORQUE ES UNA DIVISION ENTRE 0")
            actual[-1] = -1
        else:
            res = val1 / val2
            escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '%':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val2 == 0:
            error("NO SE PUEDE HACER LA DIVISIÓN PORQUE ES UNA DIVISION ENTRE 0")
            actual[-1] = -1
        else:
            res = val1 % val2
            escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '^':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        res = val1 ** val2
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
        
    # operación para asignar valores a variables
    elif quadruple_in[actual[-1]][0] == '=':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        escribir_mem(quadruple_in[actual[-1]][3], val1)
        actual[-1] = actual[-1]+1
        
    # operaciones relacionales
    elif quadruple_in[actual[-1]][0] == '<':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 < val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '<=':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 <= val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '>':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 > val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '>=':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 >= val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '==':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 == val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '!=':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 != val2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1

    # operaciones lógicas
    elif quadruple_in[actual[-1]][0] == '&':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 == 2 and val2 == 2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == '|':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        val2 = leer_mem(quadruple_in[actual[-1]][2])
        if val1 == 2 or val2 == 2:
            res = 2
        else:
            res = 1
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1

    # operaciones estadísticas
    elif quadruple_in[actual[-1]][0] == 'MEDIA':
        var_name = quadruple_in[actual[-1]][1]
        var_dir = quadruple_in[actual[-1]][2]
        vec_length = quadruple_in[actual[-1]][3]
        crear_lista(var_name,var_dir,vec_length)
        res = statistics.mean(lista_vectores)
        print(res)
        actual[-1] = actual[-1]+1

    elif quadruple_in[actual[-1]][0] == 'MEDIANA':
        var_name = quadruple_in[actual[-1]][1]
        var_dir = quadruple_in[actual[-1]][2]
        vec_length = quadruple_in[actual[-1]][3]
        crear_lista(var_name,var_dir,vec_length)
        res = statistics.median(lista_vectores)
        print(res)
        actual[-1] = actual[-1]+1

    elif quadruple_in[actual[-1]][0] == 'MODA':
        var_name = quadruple_in[actual[-1]][1]
        var_dir = quadruple_in[actual[-1]][2]
        vec_length = quadruple_in[actual[-1]][3]
        crear_lista(var_name,var_dir,vec_length)
        res = statistics.mode(lista_vectores)
        print(res)
        actual[-1] = actual[-1]+1

    elif quadruple_in[actual[-1]][0] == 'VARIANZA':
        var_name = quadruple_in[actual[-1]][1]
        var_dir = quadruple_in[actual[-1]][2]
        vec_length = quadruple_in[actual[-1]][3]
        crear_lista(var_name,var_dir,vec_length)
        res = statistics.variance(lista_vectores)
        print(res)
        actual[-1] = actual[-1]+1

    elif quadruple_in[actual[-1]][0] == 'ESDEV':
        var_name = quadruple_in[actual[-1]][1]
        var_dir = quadruple_in[actual[-1]][2]
        vec_length = quadruple_in[actual[-1]][3]
        crear_lista(var_name,var_dir,vec_length)
        res = statistics.stdev(lista_vectores)
        print(res)
        actual[-1] = actual[-1]+1

    # Instrucciones para manejar los saltos en contador de programa
    elif quadruple_in[actual[-1]][0] == 'GOTOFUN':
        val1 = leer_mem(quadruple_in[actual[-1]][1])
        if val1 == 1:
            actual[-1] = quadruple_in[actual[-1]][3]
        else:
            actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == 'GOTO':
        actual[-1] = quadruple_in[actual[-1]][3]
    elif quadruple_in[actual[-1]][0] == 'ERA':
        memoriaL.append({})
        funcion_actual = quadruple_in[actual[-1]][3]
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == 'GOTOSUB':
        funcion_actual = quadruple_in[actual[-1]][3]
        actual[-1] = actual[-1]+1
        actual.append(tabla_simbolos_in[funcion_actual]['start'])
    elif quadruple_in[actual[-1]][0] == 'PARAMETER':
        dir_or = quadruple_in[actual[-1]][2]
        val_or = leer_mem(dir_or)
        dir_des = quadruple_in[actual[-1]][3]
        escribir_mem(dir_des, val_or)
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == 'RETURN':
        dir_t = tabla_simbolos_in['#global']['vars'][funcion_actual]['address']
        escribir_mem(dir_t, quadruple_in[actual[-1]][3])
        actual[-1] = actual[-1]+1
    elif quadruple_in[actual[-1]][0] == 'FINFUNC':
        memoriaL.pop()
        actual.pop()
            
    # operación para escribir resultados en pantalla
    elif quadruple_in[actual[-1]][0] == 'WRITE':
        val1 = leer_mem(quadruple_in[actual[-1]][3])
        print(val1)
        actual[-1] = actual[-1]+1

    # operacion para leer datos escritos en teclado
    elif quadruple_in[actual[-1]][0] == 'READ':
        res = input()
        escribir_mem(quadruple_in[actual[-1]][3], res)
        actual[-1] = actual[-1]+1

    else:
        print('INSTRUCCION NO IMPLEMENTADA: ', quadruple_in[actual[-1]][0])
        actual[-1] = -1

## ++++++++++++++  INSTRUCCIONES PARA EL MANEJO DE ERRORES  ++++++++++++++
def error(msg):
    print(msg)
