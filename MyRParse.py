import ply.yacc as yacc

from MyRLex import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'POWER'),
)

##Diccionario de variables
names = { }

####  INSTRUCCIONES GENERALES

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

###CUBOp
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
