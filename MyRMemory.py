import sys
import MyRParse

siguiente_global_entero     = 1000
siguiente_global_decimal    = 3000
siguiente_global_bool       = 5000
siguiente_global_char       = 7000
siguiente_entero            = 8000
siguiente_decimal           = 10000
siguiente_bool              = 12000
siguiente_char              = 14000
siguiente_constante_entera  = 15000
siguiente_constante_decimal = 17000
siguiente_constante_char    = 19000
siguiente_constante_string  = 20000
siguiente_vector_entero     = 30000
siguiente_vector_decimal    = 40000
siguiente_vector_char       = 50000

funcion_actual = MyRParse.funcion_actual
constantes = MyRParse.constantes

def nueva_direccion(variTipo_actual):
    global funcion_actual, siguiente_global_entero, siguiente_global_decimal, siguiente_global_bool, siguiente_global_char, siguiente_entero, siguiente_decimal, siguiente_bool, siguiente_char
    aux = 0
    if funcion_actual == '#global' or funcion_actual == 'main':
        if variTipo_actual == 'int':
            if siguiente_global_entero > 2999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_entero
            siguiente_global_entero += 1
        elif variTipo_actual == 'float':
            if siguiente_global_decimal > 4999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_decimal
            siguiente_global_decimal += 1
        elif variTipo_actual == 'bool':
            if siguiente_global_bool > 6999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_bool
            siguiente_global_bool += 1            
        elif variTipo_actual == 'char':
            if siguiente_global_char > 7999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_char
            siguiente_global_char += 1
    else:
        if variTipo_actual == 'int':
            if siguiente_entero > 9999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_entero
            siguiente_entero += 1
        elif variTipo_actual == 'float':
            if siguiente_decimal > 11999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_decimal
            siguiente_decimal += 1
        elif variTipo_actual == 'bool':
            if siguiente_bool > 13999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_bool
            siguiente_bool += 1
        elif variTipo_actual == 'char':
            if siguiente_char > 14999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_char
            siguiente_char += 1
    return aux

def siguiente_constante_direccion(const_tipo):
    global constantes, siguiente_constante_entera, siguiente_constante_decimal, siguiente_constante_char, siguiente_constante_string
    aux = 0
    if const_tipo == 'int':
        if siguiente_constante_entera > 16999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES ENTERAS')
        aux = siguiente_constante_entera
        siguiente_constante_entera += 1
    elif const_tipo == 'float':
        if siguiente_constante_decimal > 18999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES DECIMALES')
        aux = siguiente_constante_decimal
        siguiente_constante_decimal += 1
    elif const_tipo == 'char':
        if siguiente_constante_char > 19999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES CHAR')
        aux = siguiente_constante_char
        siguiente_constante_char += 1
    elif const_tipo == 'string':
        if siguiente_constante_string > 20999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES TIPO STRING')
        aux = siguiente_constante_string
        siguiente_constante_string += 1
    return aux

def siguiente_vector_direccion(const_tipo):
    global constantes, siguiente_vector_entero, siguiente_vector_decimal, siguiente_vector_char
    aux = 0
    if const_tipo == 'int':
        if siguiente_vector_entero > 39999:
            error('YA NO PUEDE AGREGAR MAS ARREGLOS ENTEROS')
        aux = siguiente_vector_entero
        siguiente_vector_entero += 1
    elif const_tipo == 'float':
        if siguiente_vector_decimal > 49999:
            error('YA NO PUEDE AGREGAR MAS ARREGLOS DECIMALES')
        aux = siguiente_vector_decimal
        siguiente_vector_decimal += 1
    elif const_tipo == 'char':
        if siguiente_vector_char > 59999:
            error('YA NO PUEDE AGREGAR MAS ARREGLOS CHAR')
        aux = siguiente_vector_char
        siguiente_vector_char += 1

    return aux
