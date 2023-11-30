import ply.yacc as yacc

from MyRLex import tokens
import MyRCubo
import MyRMemory

####  LISTAS[], DICCIONARIOS{}, TABLAS Y DATOS ESTRUCTURADOS

funcion_actual = '#global'
variable_actual = None
variTipo_actual = None

tabla_simbolos = {
    '#global': {
        'vars': {},
    }
}

tabla_vectores = {
    'vector': {},
}

parametros         = []
contador_parametro = 0
funcion_llamada    = ''
ret_flag           = 0

quadruple = [
    ['START', '-', '-', '-']
]

constantes  = {}
tipos       = []
valores     = []    
operaciones = []    
saltos      = []
vari_vector = []

instruccion_for = 0
vector_var = None
write_vector_index = ''
vector_size = {}

list_vec = ()

####  INSTRUCCIONES GENERALES DE PROGRAMA
####  REGLAS DE PRODUCCION
start = 'programa'

def p_programa(p):
    '''programa : PROGRAM ID SEMI vars funcion main
                | PROGRAM ID SEMI funcion main
                | PROGRAM ID SEMI vars main
                | PROGRAM ID SEMI main'''
    pass

def p_main(p):
    '''main : MAIN function_name verifica_name LPARENT RPARENT function_all end_main'''

def p_vars(p):
    '''vars : vars list_vars SEMI
            | VAR list_vars SEMI'''

def p_list_vars(p):
    '''list_vars : list_vars COMMA vars_array
                 | list_vars COMMA ID vars_name vars_type
                 | memType vars_array
                 | memType ID vars_name vars_type'''

def p_vars_array(p):
    '''vars_array : ID vars_name vars_type LSQUARE const RSQUARE add_memory'''

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
                 | statement_condition
                 | statement_while
                 | statement_for
                 | statement_read SEMI
                 | statement_write SEMI
                 | statement_return SEMI
                 | statement_statistics SEMI
                 | statement_math SEMI'''

def p_statement_assign(p):
    '''statement_assign : ID const_id LSQUARE const save_var RSQUARE EQ opera_add expression add_tabla
                        | ID const_id EQ opera_add expression add_tabla'''

def p_expression(p):
    '''expression : ID const_id LSQUARE const save_var RSQUARE
                  | expr oper_y AND opera_add expression
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
                   | const term_muldiv DIVENT opera_add expr_muldiv
                   | const term_muldiv DIVIDE opera_add expr_muldiv
                   | const term_muldiv MODULE opera_add expr_muldiv
                   | const term_muldiv POWER opera_add expr_muldiv
                   | const term_muldiv'''
    
def p_const(p):
    '''const : LPARENT fondo_virtual expression RPARENT pop_fondo_virtual
             | INTEGERCTE const_int
             | FLOATCTE const_float
             | CHARCTE const_char
             | ID const_id'''

def p_funcion(p):
    '''funcion : FUNCION VOID loType ID function_name parametro rev_quad function_all fin_funcion funcion
               | FUNCION memType ID function_name parametro rev_quad function_all fin_funcion funcion
               | FUNCION VOID loType ID function_name parametro rev_quad function_all fin_funcion
               | FUNCION memType ID function_name parametro rev_quad function_all fin_funcion'''

def p_parametro(p):
    '''parametro : LPARENT func_vars RPARENT
                 | LPARENT RPARENT'''

def p_statement_function(p):
    '''statement_function : ID existe_funcion crea_funcion LPARENT funcion_aux verifica_param RPARENT crea_subfuncion
                          | ID existe_funcion crea_funcion LPARENT RPARENT crea_subfuncion'''

def p_funcion_aux(p):
    '''funcion_aux : expression revisar_parametro
                   | expression revisar_parametro cuenta_parametro COMMA funcion_aux'''

def p_statement_condition(p):
    '''statement_condition : IF LPARENT expression RPARENT THEN revisar_expression bloque ELSE else_expression bloque condition_end
                           | IF LPARENT expression RPARENT THEN revisar_expression bloque condition_end'''

def p_statement_while(p):
    '''statement_while : WHILE opera_while LPARENT expression RPARENT condicion_while DO bloque loop_while'''

def p_statement_for(p):
    '''statement_for : FOR opera_for statement_assign TO const compara_for condicion_for DO bloque aumenta loop_for'''

def p_statement_read(p):
    '''statement_read : READ LPARENT read_1 RPARENT'''

def p_read_1(p):
    '''read_1 : ID read_instr read_1
              | ID read_instr'''

def p_statement_write(p):
    '''statement_write : WRITE LPARENT write_1 RPARENT'''

def p_write_1(p):
    '''write_1 : expression write_instr COMMA write_1
               | STRINGCTE const_str write_instr COMMA write_1
               | expression write_instr
               | STRINGCTE const_str write_instr'''

def p_statement_return(p):
    '''statement_return : RETURN return_function LPARENT expression RPARENT return_save_quadruple'''

def p_statement_statistics(p):
    '''statement_statistics : MEDIA LPARENT const read_arg_mean RPARENT
                            | MEDIANA LPARENT const read_arg_median RPARENT
                            | MODA LPARENT const read_arg_mode RPARENT
                            | VARIANZA LPARENT const read_arg_varianza RPARENT
                            | ESDEV LPARENT const read_arg_esdev RPARENT'''
##NEW
def p_statement_math(p):
    '''statement_math : ORDENAZ LPARENT const read_arg_sort RPARENT
                      | ORDENZA LPARENT const read_arg_reverse RPARENT'''
#### PUNTOS NEURALGICOS
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
    if(funcion_actual != '#global'):
        tabla_simbolos[funcion_actual]['vars'][p[-1]] = {
            'type': None,
            'address': None
        }
        variable_actual = p[-1]
    else:
        tabla_simbolos['#global']['vars'][p[-1]] = {
            'type': None,
            'address': None
        }
        variable_actual = p[-1]

# +++++++++++  ASIGNACIÓN DE DIRECCIONES DE MEMORIA Y VARIABLES  +++++++++++++++++++

def p_vars_type(p):
    'vars_type : '
    global tabla_simbolos, funcion_actual, variable_actual, variTipo_actual
    tabla_simbolos[funcion_actual]['vars'][variable_actual] = {
        'type':variTipo_actual,
        'address':MyRMemory.nueva_direccion(variTipo_actual)
    }

def p_add_memory(p):
    'add_memory : '
    global tabla_vectores, variable_actual
    tabla_vectores['vector'][p[-6]] = {
        '0' : {
            'type': None,
            'address': None
        }
    }
    variable_actual = p[-6]
    crear_direcciones_vector()

def crear_direcciones_vector():
    global vector_size
    name = variable_actual
    for key in constantes:
        maxim = key;
    vector_size[name] = maxim
    
    index = 0
    while index < int(maxim):
        if variTipo_actual == 'int':
            new_dir = MyRMemory.siguiente_vector_direccion('int')
            tabla_vectores['vector'][name][str(index)] = {
                'type': 'int',
                'address': new_dir
            }
        index = index+1
        
# ++++++++++++++++  GUARDAR Y REVISAR LOS IDENTIFICADORES GENERADOS  ++++++++++++++
def type_find(id):
    global tabla_simbolos, funcion_actual
    if id in tabla_simbolos[funcion_actual]['vars']:
        return tabla_simbolos[funcion_actual]['vars'][id]['type']
    elif id in tabla_simbolos['#global']['vars']:
        return tabla_simbolos['#global']['vars'][id]['type']
    else:
        error('LA VARIABLE {} NO TIENE UN TIPO ASIGNADO'.format(id))
        
def address_find(id):
    global tabla_simbolos, funcion_actual
    if id in tabla_simbolos[funcion_actual]['vars']:
        return tabla_simbolos[funcion_actual]['vars'][id]['address']
    elif id in tabla_simbolos['#global']['vars']:
        return tabla_simbolos['#global']['vars'][id]['address']
    else:
        error('LA VARIABLE {} NO TIENE UNA DIRECCION ASIGNADA'.format(id))

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
            'address': MyRMemory.siguiente_constante_direccion('int'),
            'type': 'int'
        }
    valores.append(constantes[p[-1]]['address'])
    tipos.append('int')

def p_const_float(p):
    'const_float : '
    global valores, tipos, constantes, siguiente_constante_decimal
    if (p[-1] not in constantes):
        constantes[p[-1]] = {
            'address': MyRMemory.siguiente_constante_direccion('float'),
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
            'address': MyRMemory.siguiente_constante_direccion('char'),
            'type': 'char'
        }
    valores.append(constantes[const_char]['address'])
    tipos.append('char')

def p_const_str(p):
    'const_str : '
    global valores, tipos, constantes, siguiente_constante_string
    const_str = p[-1]
    const_str = const_str[1:-1]
    if const_str not in constantes:
        constantes[const_str] = {
            'address' : MyRMemory.siguiente_constante_direccion('string'),
            'type' : 'string'
        }
    valores.append(constantes[const_str]['address'])
    tipos.append('string')

def p_add_tabla(p):
    'add_tabla : '
    global valores, tipos, quadruple, operaciones
    res_tipo = tipos.pop()
    res_val = valores.pop()
    id_t = tipos.pop()
    id = valores.pop()
    operador = operaciones.pop()
    resCubo = MyRCubo.cubo_ret(id_t,res_tipo,'=')
    if resCubo == True and operador == '=':
        quadruple.append(['=',res_val,'-',id])
    else:
        error('NO CONCUERDA {}. EL TIPO NO PUEDE SER ASIGNADO A {}'.format(id_t,res_tipo))

def p_save_var(p):
    'save_var : '
    global valores
    val = valores.pop()
    for key, vals in constantes.items():
        for address, direccion in vals.items():
            if direccion == val:
                index = key
    vari = tabla_vectores['vector'][variable_actual][index]['address']
    valores.append(vari)

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
    identificador(['*','#','/','%','^'])

def p_expr_rel(p):
    'expr_rel : '
    identificador(['<', '<=', '>', '>=', '==', '!='])

def p_oper_o(p):
    'oper_o : '
    identificador(['|'])
    
def p_oper_y(p):
    'oper_y : '
    identificador(['&'])

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
            op2 = valores.pop()
            tipo2 = tipos.pop()
            op1 = valores.pop()
            tipo1 = tipos.pop()
            op = operaciones.pop()
            resultado = MyRCubo.cubo_ret(tipo1,tipo2,op)
            if resultado != 'Error':
                variTipo_actual = resultado
                res = MyRMemory.nueva_direccion(variTipo_actual)
                quadruple.append([op,op1,op2,res])
                valores.append(res)
                tipos.append(resultado)
            else:
                error('ERROR EN EL CUADRUPLO')

# ++++++++++++++++++++++++  INICIO DEL CUADRUPLO  +++++++++++++
def p_verifica_name(p):
    'verifica_name : '
    global quadruple
    quadruple[0][3] = len(quadruple)

# +++++++++++++++  DEFINICIÓN DE FUNCIONES: PRINCIPAL Y PROGRAMADAS POR USUARIO +++++++
def p_param_type(p):
    'param_type : '
    global parametros, variTipo_actual, funcion_actual, variable_actual
    direccion_parametro = tabla_simbolos[funcion_actual]['vars'][variable_actual]['address']
    parametros.append([funcion_actual, variTipo_actual, direccion_parametro])

def p_rev_quad(p):
    'rev_quad : '
    global quadruple, saltos
    
def p_function_name(p):
    'function_name : '
    global tabla_simbolos, funcion_actual, variTipo_actual, siguiente_entero, siguente_decimal, siguiente_bool, siguiente_char, quadruple
    siguiente_entero  = 8000
    siguiente_decimal = 10000
    siguiente_bool    = 12000
    siguiente_char    = 14000
    fun_nombre        = p[-1]

    if fun_nombre in tabla_simbolos:
        error('LA FUNCIÓN {} YA EXISTE'.format(fun_nombre))

    if fun_nombre in tabla_simbolos['#global']['vars']:
        error('VARIABLE GLOBAL CON EL MISMO NOMBRE QUE LA FUNCION {}'.format(fun_nombre))
    else:
        tabla_simbolos['#global']['vars'][fun_nombre] = {
            'type':variTipo_actual,
            'address': MyRMemory.nueva_direccion(variTipo_actual)
        }

    tabla_simbolos[p[-1]] = {
	'vars':{},
        'type': variTipo_actual,
        'start':len(quadruple)
    }
    funcion_actual = p[-1]

def p_fin_funcion(p):
    'fin_funcion : '
    global tabla_simbolos, quadruple, ret_flag
    tipo_funcion = tabla_simbolos['#global']['vars'][funcion_actual]['type']
    if tipo_funcion != 'void' and ret_flag == 1:
        quadruple.append(['FINFUNC','-','-','-'])
        ret_flag = 0
    elif tipo_funcion == 'void':
        quadruple.append(['FINFUNC','-','-','-'])
    else:
        error('FUNCION {} SIN CERRAR CON "RETURN"'.format(tipo_funcion))

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
    valor_argumento = valores.pop()
    tipo_argumento = tipos.pop()
    direccion = ''
    for i in range(len(parametros)):
        if parametros[i][0] == funcion_llamada:
            funcion_parametros += 1
            contador_parametro -= 1
    if contador_parametro <= funcion_parametros:
        tipo_parametros = parametros[contador_parametro][1]
        direccion = parametros[contador_parametro][2]
        if tipo_argumento == tipo_parametros:
            quad = ['PARAMETER', '-', valor_argumento, direccion]
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
    quadruple[fin][3] = len(quadruple)

# ++++++++++++++++++++++  INSTRUCCIONES DE CICLO WHILE  ++++++++
def p_opera_while(p):
    'opera_while : '
    global saltos, quadruple
    saltos.append(len(quadruple))

def p_condicion_while(p):
    'condicion_while : '
    global tipos, valores, quadruple, saltos
    tipos_while = tipos.pop()
    if tipos_while != 'bool':
        error('EL TIPO DE VARIABLE NO CORRESPONDE CON LA EVALUACION DE LA CONDICION: {}'.format(tipos_while))
    else:
        resultado = valores.pop()
        quad = ['GOTOFUN',resultado,'-',0]
        quadruple.append(quad)
        saltos.append(len(quadruple)-1)

def p_loop_while(p):
    'loop_while : '
    global saltos, quadruple
    fin = saltos.pop()
    back = saltos.pop()
    quad = ['GOTO','-','-',back]
    quadruple.append(quad)
    quadruple[fin][3] = len(quadruple)

# ++++++++++++++++++  INSTRUCCIONES DE CICLO FOR  ++++++++++++++++
def p_opera_for(p):
    'opera_for : '
    global saltos, quadruple
    saltos.append(len(quadruple))

def p_compara_for(p):
    'compara_for : '
    global quadruple, valores, variTipo_actual, instruccion_for
    quad = quadruple[len(quadruple) - 1]
    val1 = quad[3]
    instruccion_for = val1
    val2 = valores.pop()
    tipo1 = 'int'
    tipo2 = 'int'
    resultado = MyRCubo.cubo_ret(tipo1,tipo2,'<=')
    if resultado != 'Error':
        variTipo_actual = resultado
        res = MyRMemory.nueva_direccion('int')
        quadruple.append(['<=',val1,val2,res])
        valores.append(res)
        tipos.append(resultado)
    else:
        error('ERROR EN EL CUADRUPLO')

def p_condicion_for(p):
    'condicion_for : '
    global tipos, valores, quadruple, saltos
    tipos.pop()
    tipo_for = tipos.pop()
    if tipo_for != 'int':
        error('EL TIPO DE VARIABLE NO CORRESPONDE CON LA EVALUACION DE LA CONDICION: {}'.format(tipo_for))
    else:
        resultado = valores.pop()
        quad = ['GOTOFUN',resultado,'-',0]
        quadruple.append(quad)
        saltos.append(len(quadruple)-1)

def p_aumenta(p):
    'aumenta : '
    global quadruple, valores, variTipo_actual, instruccion_for
    quad = quadruple[len(quadruple) - 1]
    val1 = instruccion_for
    tipo1 = 'int'
    if '1' not in constantes:
        constantes['1'] = {
            'address': MyRMemory.siguiente_constante_direccion('int'),
            'type': 'int'
        }
    val2 = constantes['1']['address']
    tipo2 = constantes['1']['type']
    resultado = MyRCubo.cubo_ret(tipo1,tipo2,'+')
    if resultado != 'Error':
        variTipo_actual = resultado
        res = MyRMemory.nueva_direccion('int')
        quadruple.append(['+',val1,val2,res])
        valores.append(res)
        tipos.append(resultado)
    else:
        error('ERROR EN EL CUADRUPLO')
        
    quad = quadruple[len(quadruple) - 1]
    val1 = quad[3]
    tipo1 = 'int'
    val2 = quad[1]
    tipo2 = 'int'
    op = '='
    resultado = MyRCubo.cubo_ret(tipo1,tipo2,op)
    if resultado == True and op == '=':
        quadruple.append(['=',val1,'-',val2])
    else:
        error('NO CONCUERDA {}. EL TIPO NO PUEDE SER ASIGNADO A {}'.format(id_t,res_tipo))

def p_loop_for(p):
    'loop_for : '
    global saltos, quadruple
    fin = saltos.pop()
    back = saltos.pop()
    quad = ['GOTO','-','-',back+1]
    quadruple.append(quad)
    quadruple[fin][3] = len(quadruple)

# +++++++++++++++++  INSTRUCCIONES DE ESTADÍSTICA ++++++++++
def p_read_arg_mean(p):
    'read_arg_mean : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['MEDIA',var_name,var_dir,length]
    quadruple.append(quad)

def p_read_arg_median(p):
    'read_arg_median : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['MEDIANA',var_name,var_dir,length]
    quadruple.append(quad)

def p_read_arg_mode(p):
    'read_arg_mode : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['MODA',var_name,var_dir,length]
    quadruple.append(quad)

def p_read_arg_varianza(p):
    'read_arg_varianza : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['VARIANZA',var_name,var_dir,length]
    quadruple.append(quad)

def p_read_arg_esdev(p):
    'read_arg_esdev : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['ESDEV',var_name,var_dir,length]
    quadruple.append(quad)

# +++++++++++++++++  INSTRUCCIONES DE MATEMÁTICAS NEW++++++++++++++++
def p_read_arg_sort(p):
    'read_arg_sort : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['ORDENAZ',var_name,var_dir,length]
    quadruple.append(quad)

def p_read_arg_reverse(p):
    'read_arg_reverse : '
    global valores, variable_actual, variTipo_actual
    var_name = variable_actual
    length = len(tabla_vectores['vector'][variable_actual])
    var_dir = tabla_vectores['vector'][var_name]['0']['address']
    quad = ['ORDENZA',var_name,var_dir,length]
    quadruple.append(quad)

# +++++++++++++++++  INSTRUCCIONES DE LECTURA  ++++++++++++++++
def p_read_instr(p):
    'read_instr : '
    global quadruple, valores
    dir_valor = address_find(p[-1])
    quad = ['READ','-','-',dir_valor]
    quadruple.append(quad)

# +++++++++++++++ INSTRUCCIONES DE ESCRITURA  +++++++++++++++++++++++

def p_write_instr(p):
    'write_instr : '
    global quadruple, valores
    if len(valores) > 0:
        res_valor = valores.pop()
        quad = ['WRITE', '-', '-', res_valor]
        quadruple.append(quad)
        tipos.pop()

# +++++++++++++++++++  INSTRUCCION DE RETURN  +++++++++++++++++
def p_return_function(p):
    'return_function : '
    global funcion_actual, tabla_simbolos, ret_flag
    tipo_funcion = tabla_simbolos['#global']['vars'][funcion_actual]['type']
    if tipo_funcion == 'void':
        error('LA FUNCION NO LLEVA EL "RETURN"')
    else:
        ret_flag = 1

def p_return_save_quadruple(p):
    'return_save_quadruple : '
    global valores, tipos, quadruple, tabla_simbolos, funcion_actual
    valor = valores.pop()
    tipo = tipos.pop()
    tipo_funcion = tabla_simbolos[funcion_actual]['type']
    if tipo == tipo_funcion:
        quad = ['RETURN','-','-',valor]
        quadruple.append(quad)
        variable_funcion = tabla_simbolos['#global']['vars'][funcion_actual]['address']
        quadr = ['=',valor,'-',variable_funcion]
        quadruple.append(quadr)
    else:
        error('EL TIPO DE "RETURN" NO ES {}'.format(tipo_funcion))

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
