import ply.yacc as yacc

import MyRCubo
from MyRLex import tokens

####  LISTAS, DICCIONARIOS, TABLAS Y DATOS ESTRUCTURADOS

funcion_actual = '#global'
variable_actual = None
variTipo_actual = None

tabla_simbolos = {
    '#global': {
        'vars': {},
    }
}

parametros         = []
contador_parametro = 0
funcion_llamada    = ''
ret_flag           = 0

constantes                  = {}
siguiente_entero            = 1000
siguiente_decimal           = 5000
siguiente_char              = 9000
siguiente_global_entero     = 11000
siguiente_global_decimal    = 15000
siguiente_global_char       = 19000
siguiente_constante_entera  = 21000
siguiente_constante_decimal = 25000
siguiente_constante_char    = 29000

quadruple = [
    ['START', '-', '-', '-']
]

tipos       = []
valores     = []    
operaciones = []    
saltos      = []
conta       = 0

####  INSTRUCCIONES GENERALES DE PROGRAMA

inicio = 'programa'

def p_programa(p):
    '''programa : PROGRAM ID SEMI vars funcion main
                | PROGRAM ID SEMI funcion main
                | PROGRAM ID SEMI vars main
                | PROGRAM ID SEMI main'''
    pass

def p_main(p):
    '''main : MAIN function_name main_name function_all end_main'''

def p_vars(p):
    '''vars : VAR list_vars'''

def p_list_vars(p):
    '''list_vars : list_vars COMMA ID vars_name vars_type
                 | memType ID vars_name vars_type SEMI'''

def p_func_vars(p):
    '''func_vars : memType ID vars_name vars_type param_type COMMA func_vars
                 | memType ID vars_name vars_type param_type'''

def p_memType(p):
    '''memType : INT loType
               | FLOAT loType
               | CHAR loType'''

def p_function_all(p):
    '''function_all : LBRACKET vars statement_func RBRACKET
                    | LBRACKET vars RBRACKET
                    | LBRACKET statement_func RBRACKET
                    | LBRACKET RBRACKET'''

def p_bloque(p):
    '''bloque : LBRACKET statement_func RBRACKET
              | LBRACKET RBRACKET'''

def p_statement_func(p):
    '''statement_func : statement statement_func
                      | statement'''

def p_statement(p):
    '''statement : statement_assign SEMI
                 | statement_function SEMI
                 | statement_condition SEMI
                 | statement_while SEMI
                 | statement_for SEMI'''

def p_statement_assign(p):
    '''statement_assign : ID const_id EQ opera_add expression add_tabla'''

def p_expression(p):
    '''expression : expr oper_y AND opera_add expression
                  | expr oper_y '''

def p_expr(p):
    '''expr : expr_aux oper_o OR opera_add expr
            | expr_aux oper_o '''

def p_expr_aux(p):
    '''expr_aux : expr_sumres expr_rel LT opera_add expr_aux
                | expr_sumres expr_rel LTE opera_add expr_aux
                | expr_sumres expr_rel GT opera_add expr_aux
                | expr_sumres expr_rel GTE opera_add expr_aux
                | expr_sumres expr_rel SIM opera_add expr_aux
                | expr_sumres expr_rel NE opera_add expr_aux
                | expr_sumres expr_rel '''
    
def p_expr_sumres(p):
    '''expr_sumres : expr_muldiv term_sumres PLUS opera_add expr_sumres
                   | expr_muldiv term_sumres MINUS opera_add expr_sumres
                   | expr_muldiv term_sumres'''

def p_expr_muldiv(p):
    '''expr_muldiv : const term_muldiv TIMES opera_add expr_muldiv
                   | const term_muldiv DIVIDE opera_add expr_muldiv
                   | const term_muldiv POWER opera_add expr_muldiv
                   | const term_muldiv'''

def p_const(p):
    '''const : LPARENT fondo_virtual expression RPARENT pop_fondo_virtual
             | INTEGERCTE const_int
             | FLOATCTE const_float
             | CHARCTE const_char
             | ID const_id'''

def p_funcion(p):
    '''funcion : FUNCION VOID loType ID function_name parametro rev_quad function_all fin_funcion SEMI funcion
               | FUNCION memType ID function_name parametro rev_quad function_all fin_funcion SEMI funcion
               | FUNCION VOID loType ID function_name parametro rev_quad function_all fin_funcion SEMI
               | FUNCION memType ID function_name parametro rev_quad function_all fin_funcion SEMI'''

def p_parametro(p):
    '''parametro : LPARENT func_vars RPARENT
                 | LPARENT RPARENT'''

def p_statement_function(p):
    '''statement_function : ID existe_funcion crea_funcion LPARENT funcion_aux verifica_param RPARENT crea_subfuncion
                          | ID existe_funcion crea_funcion LPARENT RPARENT crea_subfuncion'''

def p_funcion_aux(p):
    '''funcion_aux : expression revisar_parametro cuenta_parametro COMMA funcion_aux
                   | expression revisar_parametro'''

def p_statement_condition(p):
    '''statement_condition : IF LPARENT expression RPARENT THEN revisar_expression bloque ELSE else_expression bloque condition_end
                           | IF LPARENT expression RPARENT THEN revisar_expression bloque condition_end'''

def p_statement_while(p):
    '''statement_while : WHILE opera_while LPARENT expression RPARENT condicion_while DO bloque loop_while'''

def p_statement_for(p):
    '''statement_for : FOR ID const_id EQ expression TO expression DO bloque'''

####  FUNCIONES DE CONTROL
# +++++++++++  TIPOS DE MEMORIAS  ++++++++++++++++++
def p_loType(p):
    'loType : '
    global variTipo_actual
    variTipo_actual = p[-1]

# +++++++++++  ALMACENAR EL NOMBRE DE LA VARIABLE EN LA TABLA DE SÍMBOLOS
def p_vars_name(p):
    'vars_name : '
    global tabla_simbolos,variable_actual,funcion_actual
    if(funcion_actual == '#global'):
        tabla_simbolos['#global']['vars'][p[-1]] = {
            'type': None,
            'address': None
        }
        variable_actual = p[-1]
    else:
        tabla_simbolos[funcion_actual]['vars'][p[-1]] = {
            'type': None,
            'address': None
        }
        variable_actual = p[-1]

# +++++++++++  ASIGNACIÓN DE DIRECCIONES DE MEMORIA Y VARIABLES  +++++++++++++++++++
def nueva_direccion():
    global funcion_actual, variTipo_actual, siguiente_global_entero, siguiente_global_decimal, siguiente_global_char, siguiente_entero, siguiente_decimal, siguiente_char
    aux = 0
    if funcion_actual == '#global' or funcion_actual == 'main':
        if variTipo_actual == 'int':
            if siguiente_global_entero > 14999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_entero
            siguiente_global_entero += 1
        elif variTipo_actual == 'float':
            if siguiente_global_decimal > 18999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_decimal
            siguiente_global_decimal += 1
        elif variTipo_actual == 'char':
            if siguiente_global_char > 20999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_global_char
            siguiente_global_char += 1
    else:
        if variTipo_actual == 'int':
            if siguiente_entero > 4999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_entero
            siguiente_entero += 1
        elif variTipo_actual == 'float':
            if siguiente_decimal > 8999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_decimal
            siguiente_decimal += 1
        elif variTipo_actual == 'char':
            if siguiente_char > 10999:
                error('YA NO PUEDE AGREGAR MAS VARIABLES {}'.format(variTipo_actual))
            aux = siguiente_char
            siguiente_char += 1
    return aux

def siguiente_constante_direccion(const_tipo):
    global tipo, constantes, siguiente_constante_entera, siguiente_constante_decimal, siguiente_constante_char
    aux = 0
    if const_tipo == 'int':
        if siguiente_constante_entera > 24999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES ENTERAS')
        aux = siguiente_constante_entera
        siguiente_constante_entera += 1
    elif const_tipo == 'float':
        if siguiente_constante_decimal > 28999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES DECIMALES')
        aux = siguiente_constante_decimal
        siguiente_constante_decimal += 1
    elif const_tipo == 'char':
        if siguiente_constante_char > 30999:
            error('YA NO PUEDE AGREGAR MAS CONSTANTES CHAR')
        aux = siguiente_constante_char
        siguiente_constante_char += 1
    return aux

def p_vars_type(p):
    'vars_type : '
    global tabla_simbolos, funcion_actual, variable_actual, variTipo_actual
    tabla_simbolos[funcion_actual]['vars'][variable_actual] = {
        'type':variTipo_actual,
        'address':nueva_direccion()
    }

# ++++++++++++++++  REVISAR LOS IDENTIFICADORES GENERADOS  ++++++++++++++
def address_find(id):
    global tabla_simbolos, funcion_actual
    if id in tabla_simbolos['#global']['vars']:
        return tabla_simbolos['#global']['vars'][id]['address']
    elif id in tabla_simbolos[funcion_actual]['vars']:
        return tabla_simbolos[funcion_actual]['vars'][id]['address']
    else:
        error('LA VARIABLE {} NO TIENE UNA DIRECCION ASIGNADA'.format(id))

def type_find(id):
    global tabla_simbolos, funcion_actual
    if id in tabla_simbolos['#global']['vars']:
        return tabla_simbolos['#global']['vars'][id]['type']
    elif id in tabla_simbolos[funcion_actual]['vars']:
        return tabla_simbolos[funcion_actual]['vars'][id]['type']
    else:
        error('LA VARIABLE {} NO TIENE UN TIPO ASIGNADO'.format(id))

def p_const_id(p):
    'const_id : '
    global valores, tipos
    valores.append(address_find(p[-1]))
    tipos.append(type_find(p[-1]))

def p_const_int(p):
    'const_int : '
    global valores, tipos, constantes, siguiente_constante_entera
    if (p[-1] not in constantes):
        constantes[p[-1]] = {
            'address': siguiente_constante_direccion('int'),
            'type': 'int'
        }
    valores.append(constantes[p[-1]]['address'])
    tipos.append('int')

def p_const_float(p):
    'const_float : '
    global valores, tipos, constantes, siguiente_constante_decimal
    if (p[-1] not in constantes):
        constantes[p[-1]] = {
            'address': siguiente_constante_direccion('float'),
            'type': 'float'
        }
    valores.append(constantes[p[-1]]['address'])
    tipos.append('float')

def p_const_char(p):
    'const_char : '
    global valores, tipos, constantes, siguiente_constante_char
    const_char = p[-1]
    const_char = const_char[1:-1]
    if const_char not in constantes:
        constantes[const_char] = {
            'address': siguiente_constante_direccion('char'),
            'type': 'char'
        }
    valores.append(constantes[const_char]['address'])
    tipos.append('char')

def p_add_tabla(p):
    'add_tabla : '
    global valores, tipos, quadruple, operaciones
    res_tipo = tipos.pop()
    res_val = valores.pop()
    id_t = tipos.pop()
    id = valores.pop()
    operador = operaciones.pop()
    resCubo = MyRCubo.cubo_ret(id_t, res_tipo, '=')
    if res_tipo == True and operador == '=':
        quadruple.append(['=', res_val, '-', id])
    else:
        error('NO CONCUERDA {}. EL TIPO NO PUEDE SER ASIGNADO A {}'.format(id_t,res_tipo))

def p_opera_add(p):
    'opera_add : '
    global operaciones
    operaciones.append(p[-1])

# +++++++++++++++  ASIGNACIÓN DE SIMBOLO DE OPERACIONES +++++++
def p_term_sumres(p):
    'term_sumres : '
    identificador(['+','-'])

def p_term_muldiv(p):
    'term_muldiv : '
    identificador(['*','/','^'])

def p_expr_rel(p):
    'expr_rel : '
    identificador(['<', '<=', '>', '>=', '==', '!='])
    
def p_oper_y(p):
    'oper_y : '
    identificador(['&'])

def p_oper_o(p):
    'oper_o : '
    identificador(['|'])

def p_fondo_virtual(p):
    'fondo_virtual : '
    global operaciones
    operaciones.append('(')

def p_pop_fondo_virtual(p):
    'pop_fondo_virtual : '
    global operaciones
    arriba = operaciones.pop()
    if arriba != '(':
        error('ERROR EN LA PILA DE OPERACIONES')

def identificador(opera):
    global operaciones, tipos, quadruple, variTipo_actual
    if len(operaciones) > 0:
        if operaciones[-1] in opera:
            op1 = valores.pop()
            tipo1 = tipos.pop()
            op2 = valores.pop()
            tipo2 = tipos.pop()
            op = operaciones.pop()
            resultado = MyRCubo.cubo_ret(tipo2,tipo1,op)
            if resultado != 'Error':
                variTipo_actual = resultado
                res = nueva_direccion()
                quadruple.append([op,op2,op1,res])
                valores.append(res)
                tipos.append(resultado)
            else:
                error('ERROR EN EL CUADRUPLO')

# +++++++++++++++  DEFINICIÓN DE FUNCIONES PRINCIPAL Y CREADAS +++++++
def p_function_name(p):
    'function_name : '
    global tabla_simbolos, funcion_actual, variTipo_actual, siguiente_entero, siguente_decimal, siguiente_char, quadruple
    siguiente_entero  = 1000
    siguiente_decimal = 5000
    siguiente_char    = 9000
    funcion_nombre = p[-1]

    if funcion_nombre in tabla_simbolos:
        error('LA FUNCIÓN {} YA EXISTE'.format(funcion_nombre))

    if funcion_nombre in tabla_simbolos['#global']['vars']:
        error('VARIABLE GLOBAL CON EL MISMO NOMBRE QUE LA FUNCION {}'.format(funcion_nombre))
    else:
        tabla_simbolos['#global']['vars'][funcion_nombre] = {
            'type':variTipo_actual,
            'address': nueva_direccion()
        }

    tabla_simbolos[p[-1]] = {
        'vars': {},
        'type': variTipo_actual,
        'start': len(quadruple)
    }
    funcion_actual = p[-1]

def p_param_type(p):
    'param_type : '
    global parametros, variTipo_actual, funcion_actual, variable_actual
    direccion_parametro = tabla_simbolos[funcion_actual]['vars'][variable_actual]['address']
    parametros.append([funcion_actual,variTipo_actual,direccion_parametro])

def p_rev_quad(p):
    'rev_quad : '
    global quadruple, saltos

def p_fin_funcion(p):
    'fin_funcion : '
    global tabla_simbolos, quadruple, ret_flag
    tipo_funcion = tabla_simbolos['#global']['vars'][funcion_actual]['type']
    if tipo_funcion == 'void':
        quadruplet.append(['FINFUNC','-','-','-'])
    elif tipo_funcion != 'void' and ret_flag == 1:
        quadruplet.append(['FINFUNC','-','-','-'])
        ret_flag = 0
    else:
        error('FUNCION {} SIN CERRAR'.format(tipo_funcion))

def p_existe_funcion(p):
    'existe_funcion : '
    global tabla_simbolos, funcion_llamada
    funcion_llamada = p[-1]
    if funcion_llamada not in tabla_simbolos:
        error('LA FUNCION {} NO EXISTE'.format(funcion_llamada))

def p_crea_funcion(p):
    'crea_funcion : '
    global operaciones, quadruple, funcion_llamada
    quad = ['ERA','-','-',funcion_llamada]
    quadruple.append(quad)
    operaciones.append('[')

def p_crea_subfuncion(p):
    'crea_subfuncion : '
    global quadruple, funcion_llamada
    quad = ['GOTOSUB','-','-',funcion_llamada]
    quadruple.append(quad)
    
def p_verifica_param(p):
    'verifica_param : '
    global contador_parametro, parametros, funcion_llamada
    for i in range(len(parametros)):
        if parametros[i][0] == funcion_llamada:
            contador_parametro += 1

def p_cuenta_parametro(p):
    'cuenta_parametro : '
    global contador_parametro
    contador_parametro += 1

def p_revisar_parametro(p):
    'revisar_parametro : '
    global valores, tipos, quadruple, contador_parametro
    funcion_parametros = 0
    tipo_parametros = ''
    argumento = valores.pop()
    tipo_argumento = tipos.pop()
    direccion = ''
    for i in range(len(parametros)):
        if parametros[i][0] == funcion_llamada:
            funcion_parametros += 1
    if contador_parametros < funcion_parametros:
        tipo_parametros = parametros[contador_parametro][1]
        direccion = parametros[contador_parametro][2]
        if tipo_argumento == tipo_parametros:
            quad = ['PARAMETER', '-', argumento, direccion]
            quadruple.append(quad)
        else:
            error('EL TIPO DE PARAMETRO NO COINCIDE CON {}'.format(tipo_parametros))
    else:
        error('EL NUMERO DE PARAMETROS NO COINCIDE CON {}'.format(funcion_parametros))

# ++++++++++++++++++++++++  INSTRUCCIONES PARA IF THEN ELSE +++++++++++++++++++++
def p_revisar_expression(p):
    'revisar_expression : '
    global operaciones, tipos, saltos, quadruple, variTipo_actual
    tipo_expr = tipos.pop()
    if tipo_expr != 'bool':
        error('EL TIPO DE VARIABLE NO CORRESPONDE CON LA EVALUACIÓN DE LA CONDICIÓN: {}'.format(tipo_expr))
    else:
        resultado = valores.pop()
        quad = ['GOTOFUN',resultado,'-',0]
        quadruple.append(quad)
        saltos.append(len(quadruple)-1)

def p_else_expression(p):
    'else_expression : '
    global saltos, quadruple
    mover = ['GOTO','-','-',0]
    quadruple.append(mover)
    false = saltos.pop()
    saltos.append(len(quadruple)-1)
    quadruple[false][3] = len(quadruple)

def p_condition_end(p):
    'condition_end : '
    global saltos
    fin = saltos.pop()
    quadruple[fin][3] = len(quadruplet)

# ++++++++++++++++++++++  INSTRUCCIONES DE CICLO WHILE  ++++++++
def p_opera_while(p):
    'opera_while : '
    global saltos, quadruple
    saltos.append(len(quadruple))

def p_condicion_while(p):
    'condicion_while : '
    global tipos, valores, quadruple, saltos
    tipos_while = topos.pop()
    if tipos_while != 'bool':
        error('EL TIPO DE VARIABLE NO CORRESPONDE CON LA EVALUACION DE LA CONDICION: {}'.format(tipos_while))
    else:
        resultado = valores.pop()
        quad = ['GOTOFUN',resultado,'-',0]
        quadruple.append(quad)
        saltos.append(len(quadruple-1))

def p_loop_while(p):
    'loop_while : '
    global saltos, quadruple
    fin = saltos.pop()
    back = saltos.pop()
    quad = ['GOTO','-','-',back]
    quadruple.append(quad)
    quadrupe[fin][3] = len(quadruple)
    
# ++++++++++++++++++++++++  INICIO DEL CUADRUPLO  +++++++++++++
def p_main_name(p):
    'main_name : '
    global quadruple
    quadruple[0][3] = len(quadruple)

# ++++++++++++++++++++++  FIN DE FUNCIÓN MAIN Y DEL PROGRAMA ++++
def p_end_main(p):
    'end_main : '
    global quadruple,saltos
    quadruple.append(['END','-','-',-1])

####  CAPTURA DE ERRORES

def p_error(p):
    if not p:
        return
    print("Error en el Parser ", p)

def error(msg):
    print('Error: ', msg)

MyRparse = yacc.yacc()

def parse(data,debug=0):
    MyRparse.error = 0
    p = MyRparse.parse(data,debug=debug)
    if MyRparse.error: return None
    return p
