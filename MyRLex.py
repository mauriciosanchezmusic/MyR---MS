import ply.lex as lex

reservadas = {
    ## MAIN PROGRAM
    'program':'PROGRAM',
    'main':'MAIN',
    'funcion':'FUNCION',
    ## VARS & TYPE
    'var':'VAR',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'string':'STRING',
    'void':'VOID',
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
    'ID', 'COMMENT',
    'INTEGERCTE', 'FLOATCTE', 'CHARCTE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'EQ',
    'LT', 'LTE', 'GT', 'GTE', 'SIM', 'NE',
    'LPARENT', 'RPARENT', 'LBRACKET', 'RBRACKET',
    'NEWLINE', 'AND', 'OR',
    'SEMI', 'COMMA',
]

t_STRING   = r'\".*?\"'
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
t_AND      = r'&'
t_OR       = r'\|'
t_LPARENT  = r'\('
t_RPARENT  = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_SEMI     = r';'
t_COMMA    = r'\,'
t_INTEGERCTE = r'[0-9][0-9]*'
t_FLOATCTE   = r'[0-9][0-9]*\.[0-9]'
t_CHARCTE    = r'(\'[^\']\')'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value,'ID')
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
