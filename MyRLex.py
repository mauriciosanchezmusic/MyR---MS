import ply.lex as lex

reservadas = {
    ## MAIN PROGRAM AND FUNCTIONS
    'program':'PROGRAM',
    'main':'MAIN',
    'funcion':'FUNCION',
    ## VARS & TYPE
    'var':'VAR',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
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
    ## RESERVED FOR GENERAL USE
    'newline':'NEWLINE',
    'read':'READ',
    'write':'WRITE',
}

tokens = list(reservadas.values()) + [
    'ID', 'COMMENT', 'RETURN',
    'INTEGERCTE', 'FLOATCTE', 'CHARCTE', 'STRINGCTE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'EQ',
    'LT', 'LTE', 'GT', 'GTE', 'SIM', 'NE',
    'LPARENT', 'RPARENT', 'LBRACKET', 'RBRACKET', 'LSQUARE', 'RSQUARE',
    'AND', 'OR',
    'SEMI', 'COMMA',
]

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
t_LSQUARE  = r'\['
t_RSQUARE  = r'\]'
t_SEMI     = r';'
t_COMMA    = r'\,'
t_INTEGERCTE = r'[0-9][0-9]*'
t_FLOATCTE   = r'[0-9][0-9]*\.[0-9]'
t_CHARCTE    = r'(\'[^\']\')'
t_STRINGCTE  = r'\"[\w\d\s\,. ]*\"'

def t_COMMENT(t):
    r'\%% .*'
    pass

def t_RETURN(t):
    r'return'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value,'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("CARACTER ILEGAL '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
