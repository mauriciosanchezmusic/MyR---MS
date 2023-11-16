import sys

## +++++++++++++  LEER ARCHIVO OBJETO GENERADO POR COMPILADOR  +++++++++++
nameFile = sys.argv[1]
with open(nameFile, 'r') as file:
    global tabla_simbolos, quadruple, constantes
    data = file.read()
    entrada = eval(data)
    tabla_simbolos_in = entrada['symbol_table']
    quadruple_in = entrada['quadruple']
    const_in = entrada['constant_table']

## ++++++++++++  LEER Y ASIGNAR MEMORIAS PARA DIRECCIONES LOCALES Y GLOBALES
global memoriaG, memoriaL, const_finales, funcion_actual
memoriaG       = {}
memoriaL       = []
const_finales  = {}
funcion_actual = 'main'

## ++++++++++++  INSTRUCCIONES PARA TRANSPONER LA TABLA DE CONSTANTES
for key, val in const_in.items():
    const_finales[val['address']] = key

global actual

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
    # direcciones de constantes
    elif dir_t >= 15000 and dir_t < 17000:
        val = int(const_finales.get(direccion, None))
    elif dir_t >= 17000 and dir_t < 19000:
        val = float(const_finales.get(direccion, None))
    elif dir_t >= 19000 and dir_t < 20000:
        val = str(const_finales.get(direccion, None))
    elif dir_t >= 20000 and dir_t > 21000:
        val = const_finales.get(direccion, None)

    if val is None:
        error('ACCESO A UNA VARIABLE NO ASIGNADA')
        actual = -1
        return
    return val

## ++++++++++++  INSTRUCCIONES PARA ASIGNAR VALORES A LAS MEMORIAS
def escribir_mem(direccion, valor, prof=-1):
    global memoriaG, memoriaL
    dir_t = int(direccion)

    if dir_t >= 8000 and dir_t < 12000 and dir_t >= 20000:
        memoriaL[prof][dir_t] = valor
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
    # operación para escribir resultados en pantalla
    elif quadruple_in[actual[-1]][0] == 'WRITE':
        val1 = leer_mem(quadruple_in[actual[-1]][3])
        print(val1)
        actual[-1] = actual[-1]+1

    else:
        print('INSTRUCCION NO IMPLEMENTADA: ', quadruple_in[actual[-1]][0])
        actual[-1] = -1

## ++++++++++++++  INSTRUCCIONES PARA EL MANEJO DE ERRORES  ++++++++++++++
def error(msg):
    print(msg)
