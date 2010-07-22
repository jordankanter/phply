# ----------------------------------------------------------------------
# phplex.py
#
# A lexer for PHP.
# ----------------------------------------------------------------------

import ply.lex as lex

# todo: end-of-line comments containing ?>
# todo: double-quoted strings
# todo: number literals (LNUMBER, DNUMBER)
# todo: heredocs
# todo: backticks
# todo: namespaces
# todo: casts
# todo: "die" as alias for "exit"
# todo: BAD_CHARACTER
# todo: CURLY_OPEN, DOLLAR_OPEN_CURLY_BRACES, STRING_VARNAME
# todo: <script> syntax (does anyone use this?)
# todo: HALT_COMPILER (??)

states = (
    ('php', 'exclusive'),
)

# Reserved words
reserved = (
    'ARRAY', 'AS', 'BREAK', 'CASE', 'CLASS', 'CONST', 'CONTINUE', 'DECLARE',
    'DEFAULT', 'DO', 'ECHO', 'ELSE', 'ELSEIF', 'EMPTY', 'ENDDECLARE',
    'ENDFOR', 'ENDFOREACH', 'ENDIF', 'ENDSWITCH', 'ENDWHILE', 'EVAL', 'EXIT',
    'EXTENDS', 'FOR', 'FOREACH', 'FUNCTION', 'GLOBAL', 'IF', 'INCLUDE',
    'INCLUDE_ONCE', 'INSTANCEOF', 'ISSET', 'LIST', 'NEW', 'PRINT', 'REQUIRE',
    'REQUIRE_ONCE', 'RETURN', 'STATIC', 'SWITCH', 'UNSET', 'USE', 'VAR',
    'WHILE', 'FINAL', 'INTERFACE', 'IMPLEMENTS', 'PUBLIC', 'PRIVATE',
    'PROTECTED', 'ABSTRACT', 'CLONE', 'TRY', 'CATCH', 'THROW', 'CFUNCTION',
    'OLD_FUNCTION',
)

tokens = reserved + (
    'WHITESPACE', 'INLINE_HTML',

    # Operators
    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'XOR', 'SL',
    'SR', 'BOOLEAN_AND', 'BOOLEAN_OR', 'BOOLEAN_NOT', 'IS_SMALLER',
    'IS_GREATER', 'IS_SMALLER_OR_EQUAL', 'IS_GREATER_OR_EQUAL', 'IS_EQUAL',
    'IS_NOT_EQUAL', 'IS_IDENTICAL', 'IS_NOT_IDENTICAL',

    # Assignment operators
    'EQUALS', 'MUL_EQUAL', 'DIV_EQUAL', 'MOD_EQUAL', 'PLUS_EQUAL',
    'MINUS_EQUAL', 'SL_EQUAL', 'SR_EQUAL', 'AND_EQUAL', 'OR_EQUAL',
    'XOR_EQUAL', 'CONCAT_EQUAL',

    # Increment/decrement
    'INC', 'DEC',

    # Arrows
    'OBJECT_OPERATOR', 'DOUBLE_ARROW', 'DOUBLE_COLON',

    # Delimiters
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA',
    'CONCAT', 'QUESTION', 'COLON', 'SEMI', 'AT',

    # Comments
    'COMMENT', 'DOC_COMMENT',

    # Escaping from HTML
    'OPEN_TAG', 'OPEN_TAG_WITH_ECHO', 'CLOSE_TAG',

    # Identifiers and reserved words
    'DIR', 'FILE', 'LINE', 'FUNC_C', 'CLASS_C', 'METHOD_C', 'NS_C',
    'LOGICAL_AND', 'LOGICAL_OR', 'LOGICAL_XOR',
    'STRING', 'VARIABLE',
    'LNUMBER', 'DNUMBER',
    'CONSTANT_ENCAPSED_STRING',
)

# Newlines
def t_php_WHITESPACE(t):
    r'[ \t\r\n]+'
    t.lexer.lineno += t.value.count("\n")
    return t

# Operators
t_php_PLUS                = r'\+'
t_php_MINUS               = r'-'
t_php_MUL                 = r'\*'
t_php_DIV                 = r'/'
t_php_MOD                 = r'%'
t_php_AND                 = r'&'
t_php_OR                  = r'\|'
t_php_NOT                 = r'~'
t_php_XOR                 = r'\^'
t_php_SL                  = r'<<'
t_php_SR                  = r'>>'
t_php_BOOLEAN_AND         = r'&&'
t_php_BOOLEAN_OR          = r'\|\|'
t_php_BOOLEAN_NOT         = r'!'
t_php_IS_SMALLER          = r'<'
t_php_IS_GREATER          = r'>'
t_php_IS_SMALLER_OR_EQUAL = r'<='
t_php_IS_GREATER_OR_EQUAL = r'>='
t_php_IS_EQUAL            = r'=='
t_php_IS_NOT_EQUAL        = r'(!=)|(<>)'
t_php_IS_IDENTICAL        = r'==='
t_php_IS_NOT_IDENTICAL    = r'!=='

# Assignment operators
t_php_EQUALS               = r'='
t_php_MUL_EQUAL            = r'\*='
t_php_DIV_EQUAL            = r'/='
t_php_MOD_EQUAL            = r'%='
t_php_PLUS_EQUAL           = r'\+='
t_php_MINUS_EQUAL          = r'-='
t_php_SL_EQUAL             = r'<<='
t_php_SR_EQUAL             = r'>>='
t_php_AND_EQUAL            = r'&='
t_php_OR_EQUAL             = r'\|='
t_php_XOR_EQUAL            = r'\^='
t_php_CONCAT_EQUAL         = r'\.='

# Increment/decrement
t_php_INC                  = r'\+\+'
t_php_DEC                  = r'--'

# Arrows
t_php_OBJECT_OPERATOR      = r'->'
t_php_DOUBLE_ARROW         = r'=>'
t_php_DOUBLE_COLON         = r'::'

# Delimeters
t_php_LPAREN               = r'\('
t_php_RPAREN               = r'\)'
t_php_LBRACKET             = r'\['
t_php_RBRACKET             = r'\]'
t_php_LBRACE               = r'\{'
t_php_RBRACE               = r'\}'
t_php_COMMA                = r','
t_php_CONCAT               = r'\.'
t_php_QUESTION             = r'\?'
t_php_COLON                = r':'
t_php_SEMI                 = r';'
t_php_AT                   = r'@'

# Comments

def t_php_DOC_COMMENT(t):
    r'/\*\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_php_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*?\n)|(\#.*?\n)'
    t.lexer.lineno += t.value.count("\n")
    return t

# Escaping from HTML

def t_OPEN_TAG(t):
    r'<[?%]((php)|=)?[ \t\r]*\n?'
    if t.value.endswith('='): t.type = 'OPEN_TAG_WITH_ECHO'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('php')
    return t

def t_php_CLOSE_TAG(t):
    r'[?%]>[ \t\r]*\n?'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.begin('INITIAL')
    return t

def t_INLINE_HTML(t):
    r'(([^<])|(<(?![?%])))+'
    t.lexer.lineno += t.value.count("\n")
    return t

# Identifiers and reserved words

reserved_map = {
    '__DIR__':       'DIR',
    '__FILE__':      'FILE',
    '__LINE__':      'LINE',
    '__FUNCTION__':  'FUNC_C',
    '__CLASS__':     'CLASS_C',
    '__METHOD__':    'METHOD_C',
    '__NAMESPACE__': 'NS_C',

    'AND':           'LOGICAL_AND',
    'OR':            'LOGICAL_OR',
    'XOR':           'LOGICAL_XOR',
}

for r in reserved:
    reserved_map[r] = r

# Identifier
def t_php_STRING(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value.upper(), 'STRING')
    return t

# Variable
def t_php_VARIABLE(t):
    r'\$[A-Za-z_][\w_]*'
    return t

# Integer literal (todo)
def t_php_LNUMBER(t):
    r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
    return t

# Floating literal (todo)
def t_php_DNUMBER(t):
    r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
    return t

# String literal
def t_php_CONSTANT_ENCAPSED_STRING(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    return t

def t_ANY_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex(optimize=0)
if __name__ == "__main__":
    lex.runmain(lexer)