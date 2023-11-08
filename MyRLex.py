import ply.lex as lex

reservadas = {
    ## MAIN PROGRAM
    'program':'PROGRAM',
    'main':'MAIN',
    ## VARS & TYPE
    'var':'VAR',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'string':'STRING',
    ## IF-ELSE
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    ## LOOPS
    'for':'FOR',
    'to':'TO',
    'while':'WHILE',
    'do':'DO',
}

tokens = list(reservadas.values()) + [
    'ID', 'COMMENT', 'INTEGER', 'FLOATV', 'CHARV', 
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'EQ',
    'LT', 'LTE', 'GT', 'GTE', 'SIM', 'NE',
    'LPARENT', 'RPARENT', 'LBRACKET', 'RBRACKET',
    'NEWLINE',
    'SEMI', 'COMMA',
]

t_INTEGER  = r'\d+'
t_FLOATV   = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING   = r'\".*?\"'
t_CHARV    = r'([_A-Za-z])'
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_POWER    = r'\^'
t_EQ       = r'='
t_LT       = r'<'
t_LTE      = r'<='
t_GT       = r'>'
t_GTE      = r'>='
t_SIM      = r'=='
t_NE       = r'!='
t_LPARENT  = r'\('
t_RPARENT  = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_SEMI     = r';'
t_COMMA    = r'\,'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value,'ID')
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_COMMENT(p):
    r'%% .'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_TO(t):
    r'to'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
