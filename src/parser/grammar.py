from common.pycompiler import Grammar
import semantics.ast as ast

# grammar
G = Grammar()

# non-terminals

# Definiciones de programa y tipos
program, definition_list, definition, fun_def, type_def = G.NonTerminals('<program> <definition-list> <definition> <fun-def> <type-def>')

# Expresiones
expr, simple_expr, block_expr, expr_list = G.NonTerminals('<expr> <simple-expr> <block-expr> <expr-list>')
lego_expr, paren_expr, atom = G.NonTerminals('<lego-expr> <paren-expr> <atom>')                                     

# Sentencias (Statements)
let_in_stmt, var_defs, typed_var, while_stmt, for_stmt = G.NonTerminals('<let-in-stmt> <var-defs> <typed-var> <while-stmt> <for-stmt>')
if_else_stmt, elif_stmts, d_assign, member_call, fun_call = G.NonTerminals('<if-else-stmt> <elif-stmts> <d-assign> <member-call> <fun-call>')
                                                                            
# Argumentos y Tipos
args_list, args_list_eps, typed_arg = G.NonTerminals('<args-list> <args-list-eps> <typed-arg>')
opt_typing, inherit_eps, type_args_eps = G.NonTerminals('<opt-typing> <inherit-eps> <type-args-eps>')                                                    

# Operadores
d_assign_op, or_op, and_op, eq_op, ineq_op, type_test_op, concat_op = G.NonTerminals('<d-assign-op> <or-op> <and-op> <eq-op> <ineq-op> <type-test-op> <concat-op>')
add_sub_op, mul_div_op, neg_op, pow_op, inst_op, not_op = G.NonTerminals('<add-sub-op> <mul-div-op> <neg-op> <pow-op> <inst-op> <not-op>')
                                                                       
# Combinaciones de Expresiones
expr_list_comma, expr_list_comma_eps = G.NonTerminals('<expr-list-comma> <expr-list-comma-eps>')

# Definiciones de Miembros de Clase/Tipo
type_def_body, type_def_body_eps, member_def, method_def, attr_def = G.NonTerminals('<type-def-body> <type-def-body-eps> <member-def> <method-def> <attr-def>')
 

# terminals
type_, inherits, base, idx, new, is_ , as_ = G.Terminals('type inherits base <id> new is as')
let, in_, equal, d_assign = G.Terminals('let in = :=')
function, arrow = G.Terminal('function =>')
if_, elif_, else_ = G.Terminals('if elif else')
while_, for_ = G.Terminals('while for')
plus, minus, star, div, mod, pow, pow2, number_lit = G.Terminals('+ - * / % ^ ** <number>')
eq, neq, le, ge, lt, gt = G.Terminals('== != <= >= < >')
and_ , or_, not_, bool_lit = G.Terminals('& | ! <bool>')
at, double_at, string_lit = G.Terminals('@ @@ <string>')
s_colon, colon, comma, dot, opar, cpar, ocur, ccur = G.Terminals('; : , . ( ) { }')

# productions
program %= definition_list + simple_expr, lambda h,s: ast.ProgramNode(s[1], s[2])
program %= definition_list + lego_expr, lambda h,s: ast.ProgramNode(s[1], s[2])
program %= simple_expr, lambda h,s: ast.ProgramNode([], s[1])
program %= lego_expr, lambda h,s: ast.ProgramNode([], s[1])

definition_list %= definition + definition_list, lambda h,s: [s[1]] + s[2]
definition_list %= definition, lambda h,s: [s[1]] 

definition %= fun_def, lambda h,s: s[1]
definition %= type_def, lambda h,s: s[1]          

expr %= simple_expr, lambda h,s: s[1]
expr %= block_expr, lambda h,s: s[1]

simple_expr %= let_in_stmt, lambda h, s: s[1]   
simple_expr %= while_stmt, lambda h, s: s[1]
simple_expr %= for_stmt, lambda h, s: s[1]
simple_expr %= if_else_stmt, lambda h, s: s[1]
simple_expr %= d_assign, lambda h, s: s[1]

block_expr %= ocur + expr_list + ccur, lambda h,s: ast.ExpressionBlockNode(s[2])

lego_expr %= expr + s_colon, lambda h,s: s[1]
lego_expr %= block_expr, lambda h,s: s[1]

expr_list %= lego_expr + expr_list, lambda h,s: [s[1]] + s[2]
expr_list %= lego_expr, lambda h,s: [s[1]] 
expr_list %= simple_expr, lambda h,s: [s[1]]

expr_list_comma_eps %= G.Epsilon, lambda h, s: []
expr_list_comma_eps %= expr_list_comma, lambda h, s: s[1]

expr_list_comma %= expr, lambda h, s: [s[1]]
expr_list_comma %= expr + comma + expr_list_comma, lambda h, s: [s[1]] + s[3]

#hierarchy

#destructive assignment has right asociation 
d_assign_op %= or_op + d_assign + d_assign_op, 
d_assign_op %= or_op,

or_op %= or_op + or_ + and_op,
or_op %= and_op,

and_op %= and_op + and_ + eq_op,
and_op %= eq_op,

eq_op %= eq_op + eq + ineq_op,
eq_op %= eq_op + neq + ineq_op,
eq_op %= ineq_op

ineq_op %= ineq_op + le + type_test_op,
ineq_op %= ineq_op + ge + type_test_op,
ineq_op %= ineq_op + lt + type_test_op,
ineq_op %= ineq_op + gt + type_test_op,
ineq_op %= type_test_op,

type_test_op %= concat_op + is_ + idx,
type_test_op %= concat_op + as_ + idx,
type_test_op %= concat_op,

concat_op %= concat_op + at + add_sub_op, 
concat_op %= concat_op + double_at + add_sub_op,
concat_op %= add_sub_op,

add_sub_op %= add_sub_op + plus + mul_div_op,
add_sub_op %= add_sub_op + minus + mul_div_op,
add_sub_op %= mul_div_op,

mul_div_op %= mul_div_op + star + neg_op,
mul_div_op %= mul_div_op + div + neg_op,
mul_div_op %= mul_div_op + mod + neg_op,
mul_div_op %= neg_op,

#neg stands for negation
neg_op %= minus + pow_op,
neg_op %= pow_op,

#pow has right asociation 
pow_op %= inst_op + pow + pow_op,
pow_op %= inst_op + pow2 + pow_op,
pow_op %= inst_op,

#inst stands for instantiation
inst_op %= new + idx + opar + expr_list_comma_eps + cpar, 
inst_op %= not_op,

not_op %= not_ + member_call,
not_op %= member_call,

member_call %= member_call + dot + idx + opar + expr_list_comma_eps + cpar,
member_call %= member_call + dot + idx,
member_call %= paren_expr,

paren_expr %= opar + expr + cpar,
paren_expr %= atom,

atom %= idx,
atom %= number_lit,
atom %= bool_lit,
atom %= string_lit,
atom %= fun_call,
atom %= base + opar + expr_list_comma_eps + cpar,

#fun_call
fun_call %= idx + opar + expr_list_comma_eps + cpar, 

#letin

let_in_stmt %= let + var_defs + in_ + expr,

var_defs %= typed_var + comma + var_defs,
var_defs %= typed_var,

typed_var %= idx + opt_typing + eq + expr,
 
#if_else
if_else_stmt %= if_ + opar + expr + cpar + expr + elif_stmts + else_ + expr,

elif_stmts %= elif_ + opar + expr + cpar + expr + elif_stmts,
elif_stmts %= G.Epsilon

#loopsssss
while_stmt %= while_ + opar + expr + cpar + expr,

for_stmt %= for_ + opar + idx + in_ + expr + cpar + expr,

##
fun_def %= (
    function + idx + opar + args_list_eps + cpar + opt_typing + arrow + simple_expr + s_colon,
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[8], s[6])
)

fun_def %= (
    function + idx + opar + args_list_eps + cpar + opt_typing + block_expr, 
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[7], s[6])
)

fun_def %= (
    function + idx + opar + args_list_eps + cpar + opt_typing + block_expr, s_colon,
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[7], s[6])
)

args_list_eps %= args_list + comma, lambda h,s: s[1]
args_list_eps %= G.Epsilon, lambda h,s: []

args_list %= typed_arg + comma + args_list, lambda h, s: [s[1]] + s[3]
args_list %= typed_arg, lambda h,s: [s[1]] 

typed_arg %= idx + opt_typing, lambda h, s: (s[1], s[2])

opt_typing %= colon + idx, lambda h, s: s[2]
opt_typing %= G.Epsilon, lambda h, s: None

#types
type_def %= type_ + idx + type_args_eps + inherit_eps + ocur + type_def_body_eps + ccur,

inherit_eps %= G.Epsilon,
inherit_eps %= inherits + idx,

type_args_eps %= opar + args_list_eps + cpar,
type_args_eps %= G.Epsilon,

type_def_body %= G.Epsilon,
type_def_body %= member_def + type_def_body,
member_def %= method_def,
member_def %= attr_def,


##methods
method_def %= (
    idx + opar + args_list_eps + cpar + opt_typing + arrow + simple_expr + s_colon,
    lambda h,s: ast.MethodDefinitionNode(s[2], s[4], s[8], s[6])                     #change args???
)

method_def %= (
    idx + opar + args_list_eps + cpar + opt_typing + block_expr, 
    lambda h,s: ast.MethodDefinitionNode(s[2], s[4], s[7], s[6])                 #change args???
)

method_def %= (
    idx + opar + args_list_eps + cpar + opt_typing + block_expr, s_colon,
    lambda h,s: ast.MethodDefinitionNode(s[2], s[4], s[7], s[6])                 #change args???
)

#attributes
attr_def %= idx + opt_typing + eq + lego_expr,





 
