from parser.hulk_grammar import *
 
symbols = '|'.join([',',':',';','<','>','!','=',r'\?','%','.','\'',' ','\n','\t',r'\\"'])
digits = '|'.join(str(n) for n in range(0,10))
nonzero_digits = '|'.join(str(n) for n in range(1,10))
lowercase_letters = '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1))
uppercase_letters = '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1))
letters = f'{lowercase_letters}|{uppercase_letters}'
alphanum = f'{letters}|{digits}'+'|'+'_' 

table = [
    (string_lit, f'((")({alphanum}|{symbols})*("))'),
    (type_, 'type'),
    (inherits, 'inherits'),
    (base, 'base'),
    (function, 'function'),
    (arrow, '=>'),
    (let , 'let'),
    (in_ , 'in'), 
    (while_, 'while'),
    (for_, 'for'),
    (if_,'if'),
    (elif_, 'elif'),
    (else_, 'else'),
    (as_, 'as'),
    (is_, 'is'),
    (new,'new'),
    (plus, r'\+'),
    (minus, r'\-'),
    (pow, r'^|(\*\*)'),
    (star, r'\*'),
    (div, '/'),
    (mod, '%'),
    (opar, r'\('),
    (cpar, r'\)'),
    (ocur, '{'),
    (ccur, '}'),
    (s_colon, ';'),
    (colon, ':'),
    (comma, ','),
    (dot, '.'),
    (equal, '='),
    (d_assign, ':='),
    (bool_lit, 'True|False'),
    (and_, '&'),
    (or_, r'\|'),
    (not_, '!'),
    (eq, '=='),
    (neq, '!='),
    (lt, '<'),
    (gt, '>'),
    (le, '<='),
    (ge, '>='),
    (idx, f'(({letters})({alphanum})*)'),
    (number_lit, f'(0|[1-9][0-9]*)(.[0-9]+)?'),
    (at, '@'),
    (double_at, '@@')
]
