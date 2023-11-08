import ply.yacc as yacc

from MyRLex import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'POWER'),
)

####  LISTAS, DICCIONARIOS, TABLAS Y DATOS ESTRUCTURADOS

funcion_actual = '#global'
variable_actual = None
variTipo_actual = None

tabla_simbolos = {
    '#global': {
        'vars': {},
    }
}

siguiente_entero         = 1000
siguiente_decimal        = 5000
siguiente_char           = 9000
siguiente_global_entero  = 11000
siguiente_global_decimal = 15000
siguiente_global_char    = 19000

quadruple = [
    ['START', '-', '-', '-']
]

saltos = []

####  INSTRUCCIONES GENERALES DE PROGRAMA

inicio = 'programa'

def p_programa(p):
    '''programa : PROGRAM ID SEMI main'''

def p_main(p):
    '''main : MAIN function_name main_name function_all end_main'''

def p_vars(p):
    'vars : VAR list_vars SEMI'

def p_list_vars(p):
    '''list_vars : list_vars COMMA ID vars_name vars_type
                 | memType ID vars_name vars_type'''

def p_memType(p):
    '''memType : INT loType
               | FLOAT loType
               | CHAR loType'''

def p_function_all(p):
    '''function_all : LBRACKET vars statement aux RBRACKET
                    | LBRACKET vars RBRACKET
                    | LBRACKET statement aux RBRACKET
                    | LBRACKET RBRACKET'''

def p_statement(p):
    '''statement : command NEWLINE'''
    p[0] = p[1]

def p_statement_assign(p):
    '''statement : ID EQ expression'''
    names[p[1]] = p[3]

def p_statement_expr(p):
    '''statement : expression'''
    print(p[1])

def p_command_int(p):
    '''command : INT variable'''
    p[0] = p[2]

def p_command_float(p):
    '''command : FLOAT variable'''
    p[0] = p[2]

def p_command_char(p):
    '''command : CHAR variable'''
    p[0] = p[2]

def p_expression_group(p):
    'expression : LPARENT expression RPARENT'
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INTEGER
                  | FLOATV'''
    p[0] = eval(p[1])

def p_expression_name(p):
    'expression : ID'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

####  OPERACIONES ARITMÉTICAS
        
def ArOp(op1, op, op2):
    if op == '+': return op1 + op2
    elif op == '-': return op1 - op2
    elif op == '*': return op1 * op2
    elif op == '/': return op1 / op2
    elif op == '^': return op1 ** op2

def p_binary_operators(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | MINUS expression'''
    if (len(p) == 3): p[0] = -p[2]
    else: p[0] = ArOp(p[1], p[2], p[3])

####  OPERACIONES RELACIONALES

def RelOp(rel1, rel, rel2):
    if rel == '<':    return rel1 < rel2
    elif rel == '<=': return rel1 <= rel2
    elif rel == '>':  return rel1 > rel2
    elif rel == '>=': return rel1 >= rel2
    elif rel == '==': return rel1 == rel2
    elif rel == '!=': return rel1 != rel2

def p_rel_expression(p):
    '''expression : expression LT expression
                  | expression LTE expression
                  | expression GT expression
                  | expression GTE expression
                  | expression SIM expression
                  | expression NE expression'''
    p[0] = RelOp(p[1], p[2], p[3])

####  IF-ELSE DECISIONES
def IfDec(relop, exp1):
    if relop: return exp1

def IfElseDec(relop, exp1, exp2):
    if relop: return exp1
    else: return exp2

def p_statement_if(p):
    '''expression : IF expression THEN expression'''
    p[0] = IfDec(p[2], p[4])

def p_statement_if_else(p):
    '''expression : IF expression THEN expression ELSE expression'''
    p[0] = IfElseDec(p[2], p[4], p[6])        

####  FOR Y WHILE LOOPS
def forStat(varInit, varFinal, expr):
    for x in range(varInit, varFinal + 1):
        print("x: ", x * expr)

def whileStat(relex, expr):
    x = 0
    while (x < relex):
        print(x * expr)
        x = x + 1
    
def p_for(p):
    '''expression : FOR expression TO expression DO expression'''
    p[0] = forStat(p[2], p[4], p[6])

def p_while(p):
    '''expression : WHILE expression DO expression'''
    p[0] = whileStat(p[2], p[4])

####  DECLARACIÓN DE VARIABLES
def p_variable(p):
    '''variable : ID'''
    p[0] = p[1]

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
    if(funcion_actual == "#global"):
        tabla_simbolos['#global']['vars'][p[-1]] = {
            'type':None,
            'address':None
        }
        variable_actual = p[-1]
    else:
        tabla_simbolos[funcion_actual]['vars'][p[-1]] = {
            'type':None,
            'address':None
        }
        variable_actual = p[-1]

# +++++++++++  ASIGNACIÓN DE DIRECCIONES DE MEMORIA  +++++++++++++++++++
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

def p_vars_type(p):
    'vars_type : '
    global tabla_simbolos, funcion_actual, variable_actual, variTipo_actual
    tabla_simbolos[funcion_actual]['vars'][variable_actual] = {
        'type':variTipo_actual,
        'address':nueva_direccion()
    }

# +++++++++++++++  DEFINICIÓN DE FUNCIONES PRINCIPAL Y CREADAS +++++++
def p_function_name(p):
    'function_name : '
    global tabla_simbolos, funcion_actual, variTipo_actual, siguiente_entero
    global siguente_decimal, siguiente_char, quadruple, tabla_simbolos
    siguiente_entero  = 1000
    siguiente_decimal = 5000
    siguiente_char    = 9000
    funcion_nombre = p[-1]

    if funcion_nombre in tabla_simbolos:
        error('LA FUNCIÓN {} YA EXISTE'.format(funcion_nombre))

    if funcion_nombre in tabla_simbolos['#global']['vars']:
        error('VARIABLE GLOBAL CON EL MISMO NOMBRE {}'.format(funcion_nombre))
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
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntaxis error in input")

MyRparse = yacc.yacc()

def parse(data,debug=0):
    MyRparse.error = 0
    p = MyRparse.parse(data,debug=debug)
    if MyRparse.error: return None
    return p
