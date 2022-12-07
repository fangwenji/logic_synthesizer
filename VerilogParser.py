from ast import operator
from asyncio import constants
import sys, re
from ply.lex import TOKEN, lex
from ply.yacc import yacc

def vlg_parser(expr):
    # --- Tokenizer

    # All tokens must be named in advance.
    # consts = ('INTNUM_DEC')
    # # identifiers = ('REG', 'WIRE')
    # parentheses = ('LPAREN', 'RPAREN')
    # operators = ('BAND', 'BOR', 'BNOT', 'AND', 'OR', 'NOT')
    # tokens = consts + parentheses + operators +()
    tokens = ('INTNUM_BIN', 'INTNUM_OCT', 'INTNUM_DEC', 'INTNUM_HEX', \
                'SIGNED_INTNUM_BIN', 'SIGNED_INTNUM_OCT', 'SIGNED_INTNUM_DEC', 'SIGNED_INTNUM_HEX', \
                'LPAREN', 'RPAREN', \
                'MUL', 'DIV', 'ADD', 'SUB', \
                'BAND', 'BOR', 'BNOT', 'AND', 'OR', 'NOT', \
                'ID', \
                'EQ', 'NE', 'LT', 'GT'
            )




    t_ignore = ' \t'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_ADD = r'\+'
    t_SUB = r'\-'
    t_BAND = r'\&'
    t_BOR = r'\|'
    t_BNOT = r'\~'
    t_AND = r'\&\&'
    t_OR = r'\|\|'
    t_NOT = r'\!' 
    t_EQ = r'=='
    t_NE = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_ID = r'(([a-zA-Z_])([a-zA-Z_0-9$])*)|((\\\S)(\S)*)'


    bin_number = '[0-9]*\'[bB][0-1xXzZ?][0-1xXzZ?_]*'
    signed_bin_number = '[0-9]*\'[sS][bB][0-1xZzZ?][0-1xXzZ?_]*'
    octal_number = '[0-9]*\'[oO][0-7xXzZ?][0-7xXzZ?_]*'
    signed_octal_number = '[0-9]*\'[sS][oO][0-7xXzZ?][0-7xXzZ?_]*'
    decimal_number = '([0-9]*\'[dD][0-9xXzZ?][0-9xXzZ?_]*)|([0-9][0-9_]*)'
    signed_decimal_number = '[0-9]*\'[sS][dD][0-9xXzZ?][0-9xXzZ?_]*'
    hex_number = '[0-9]*\'[hH][0-9a-fA-FxXzZ?][0-9a-fA-FxXzZ?_]*'
    signed_hex_number = '[0-9]*\'[sS][hH][0-9a-fA-FxXzZ?][0-9a-fA-FxXzZ?_]*'




    @TOKEN(bin_number)
    def t_INTNUM_BIN(t):
        return t

    @TOKEN(octal_number)
    def t_INTNUM_OCT(t):
        return t

    @TOKEN(decimal_number)
    def t_INTNUM_DEC(t):
        return t

    @TOKEN(hex_number)
    def t_INTNUM_HEX(t):
        return t

    @TOKEN(signed_bin_number)
    def t_SIGNED_INTNUM_BIN(t):
        return t

    @TOKEN(signed_octal_number)
    def t_SIGNED_INTNUM_OCT(t):
        return t

    @TOKEN(signed_decimal_number)
    def t_SIGNED_INTNUM_DEC(t):
        return t

    @TOKEN(signed_hex_number)
    def t_SIGNED_INTNUM_HEX(t):
        return t


    # Ignored token with an action associated with it
    def t_ignore_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    # Error handler for illegal characters
    def t_error(t):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

    # Build the lexer object
    lexer = lex(debug=False)
        
    # ---------------- Parser -----------------
    #===================== priority ==========================
    precedence = (
            # <- Weak
            ('left', 'OR'),
            ('left', 'AND'),
            ('left', 'BOR'),
            ('left', 'BAND'),
            ('left', 'EQ', 'NE'),
            ('left', 'LT', 'GT'),
            ('left', 'ADD', 'SUB'),
            ('left', 'MUL', 'DIV'),
            ('right', 'NOT', 'BNOT'),
            # -> Strong
        )

    # Write functions for each grammar rule which is
    # specified in the docstring.
    def p_expression_mul(p):
        '''
        expression : expression MUL expression
        '''
        p[0] = ('mul', p[1], p[3])

    def p_expression_div(p):
        '''
        expression : expression DIV expression
        '''
        p[0] = ('div', p[1], p[3])

    def p_expression_add(p):
        '''
        expression : expression ADD expression
        '''
        p[0] = ('add', p[1], p[3])

    def p_expression_sub(p):
        '''
        expression : expression SUB expression
        '''
        p[0] = ('sub', p[1], p[3])

    def p_expression_or(p):
        '''
        expression : expression OR expression
        '''
        # p[0] = ('or',  p[2],  p[1], p[3])
        p[0] = ('or', p[1], p[3])

    def p_expression_and(p):
        '''
        expression : expression AND expression
        '''
        # p[0] = ('and',  p[2],  p[1], p[3])
        p[0] = ('and', p[1], p[3])


    def p_expression_bor(p):
        '''
        expression : expression BOR expression
        '''
        # p[0] = ('bor',  p[2],  p[1], p[3])
        p[0] = ('bor', p[1], p[3])


    def p_expression_band(p):
        '''
        expression : expression BAND expression
        '''
        # p[0] = ('band',  p[2],  p[1], p[3])
        p[0] = ('band', p[1], p[3])


    def p_expression_eq(p):
        '''
        expression : expression EQ expression
        '''
        p[0] = ('eq', p[1], p[3])

    def p_expression_ne(p):
        '''
        expression : expression NE expression
        '''
        p[0] = ('ne', p[1], p[3])

    def p_expression_lt(p):
        '''
        expression : expression LT expression
        '''
        p[0] = ('lt', p[1], p[3])

    def p_expression_gt(p):
        '''
        expression : expression GT expression
        '''
        p[0] = ('gt', p[1], p[3])

    def p_expression_not(p):
        '''
        expression : NOT expression
        '''
        p[0] = ('not', p[2])

    def p_expression_bnot(p):
        '''
        expression : BNOT expression
        '''
        p[0] = ('bnot', p[2])

    def p_expression_grouped(p):
        '''
        expression : LPAREN expression RPAREN
        '''
        # p[0] = ('grouped', p[2])
        p[0] = p[2]

    def p_expression_id(p):
        '''
        expression : ID
        '''
        # p[0] = ('id', p[1])
        p[0] = p[1]
    def p_expression_const(p):
        '''
        expression : intnumber
        '''
        p[0] = p[1]
    # def p_const_expression_intnum(p):
    #     '''
    #     const_expression : intnumber
    #     '''
    #     # p[0] = ('intconst', p[1])
    #     p[0] = p[1]
    def p_intnumber(p):
        '''
        intnumber : INTNUM_BIN
        | INTNUM_OCT
        | INTNUM_DEC
        | INTNUM_HEX
        | SIGNED_INTNUM_BIN
        | SIGNED_INTNUM_OCT
        | SIGNED_INTNUM_DEC
        | SIGNED_INTNUM_HEX
        '''
        p[0] = p[1]



    def p_error(p):
        print(f'Syntax error at {p.value!r}')

    # Build the parser
    parser = yacc(debug=True)

    # Parse an expression
    ast = parser.parse(expr)
    ast_str = str(ast)
    ast_re = re.sub(r"\(", r"[", ast_str)
    ast_re = re.sub(r"\)", r"]", ast_re)
    ast_re = eval(ast_re)

    return ast_re
