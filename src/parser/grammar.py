from common.pycompiler import Grammar
import semantics.ast as ast

# grammar
G = Grammar()

# non-terminals

# Definiciones de programa y tipos
program, definition_list, definition, func_def, type_def = G.NonTerminals('<program> <definition-list> <definition> <fun-def> <type-def>')

# Expresiones
expr, simple_expr, block_expr, expr_list = G.NonTerminals('<expr> <simple-expr> <block-expr> <expr-list>')
lego_expr, paren_expr, atom = G.NonTerminals('<lego-expr> <paren-expr> <atom>')                                     

# Sentencias (Statements)
let_in_stmt, var_defs, typed_var, while_stmt, for_stmt = G.NonTerminals('<let-in-stmt> <var-defs> <typed-var> <while-stmt> <for-stmt>')
if_else_stmt, elif_stmts, d_assign, member_call, func_call = G.NonTerminals('<if-else-stmt> <elif-stmts> <d-assign> <member-call> <fun-call>')
                                                                            
# Parametros y Tipos 
params_list, params_list_eps, typed_param = G.NonTerminals('<params-list> <params-list-eps> <typed-param>')
opt_typing, inherit_eps, type_params_eps = G.NonTerminals('<opt-typing> <inherit-eps> <type-params-eps>')                                                    

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

########### productions

program %= definition_list + simple_expr, lambda h,s: ast.ProgramNode(s[1], s[2])
program %= definition_list + lego_expr, lambda h,s: ast.ProgramNode(s[1], s[2])
program %= simple_expr, lambda h,s: ast.ProgramNode([], s[1])
program %= lego_expr, lambda h,s: ast.ProgramNode([], s[1])

definition_list %= definition + definition_list, lambda h,s: [s[1]] + s[2]
definition_list %= definition, lambda h,s: [s[1]] 

definition %= func_def, lambda h,s: s[1]
definition %= type_def, lambda h,s: s[1]          

expr %= simple_expr, lambda h,s: s[1]
expr %= block_expr, lambda h,s: s[1]

simple_expr %= let_in_stmt, lambda h, s: s[1]   
simple_expr %= while_stmt, lambda h, s: s[1]
simple_expr %= for_stmt, lambda h, s: s[1]
simple_expr %= if_else_stmt, lambda h, s: s[1]
simple_expr %= d_assign, lambda h, s: s[1]

block_expr %= ocur + expr_list + ccur, lambda h,s: ast.ExprBlockNode(s[2])

lego_expr %= expr + s_colon, lambda h,s: s[1]
lego_expr %= block_expr, lambda h,s: s[1]

expr_list %= lego_expr + expr_list, lambda h,s: [s[1]] + s[2]
expr_list %= lego_expr, lambda h,s: [s[1]] 
expr_list %= simple_expr, lambda h,s: [s[1]]

expr_list_comma_eps %= G.Epsilon, lambda h, s: []
expr_list_comma_eps %= expr_list_comma, lambda h, s: s[1]

expr_list_comma %= expr, lambda h, s: [s[1]]
expr_list_comma %= expr + comma + expr_list_comma, lambda h, s: [s[1]] + s[3]

##### definitions

#func definitions
func_def %= (
    function + idx + opar + params_list_eps + cpar + opt_typing + arrow + simple_expr + s_colon,
    lambda h,s: ast.FuncDefNode(s[2], s[4], s[8], s[6])
)

func_def %= (
    function + idx + opar + params_list_eps + cpar + opt_typing + block_expr, 
    lambda h,s: ast.FuncDefNode(s[2], s[4], s[7], s[6])
)

func_def %= (
    function + idx + opar + params_list_eps + cpar + opt_typing + block_expr, s_colon,
    lambda h,s: ast.FuncDefNode(s[2], s[4], s[7], s[6])
)

params_list_eps %= params_list + comma, lambda h,s: s[1]
params_list_eps %= G.Epsilon, lambda h,s: []

params_list %= typed_param + comma + params_list, lambda h, s: [s[1]] + s[3]
params_list %= typed_param, lambda h,s: [s[1]] 

typed_param %= idx + opt_typing, lambda h, s: (s[1], s[2])

opt_typing %= colon + idx, lambda h, s: s[2]
opt_typing %= G.Epsilon, lambda h, s: None

#type definition
type_def %= type_ + idx + type_params_eps + inherit_eps + ocur + type_def_body_eps + ccur, lambda h, s: (
    ast.TypeDefNode(s[2], s[3], s[6], s[4])
)

type_def %= type_ + idx + type_params_eps + inherits + idx + opar + expr_list_comma_eps + cpar + ocur + type_def_body_eps + ccur, lambda h, s: (
    ast.TypeDefNode(s[2], s[3], s[10], s[5], s[7])
)

inherit_eps %= G.Epsilon, lambda h, s: []
inherit_eps %= inherits + idx, lambda h, s: s[2]

type_params_eps %= opar + params_list_eps + cpar, lambda h, s: s[2]
type_params_eps %= G.Epsilon, lambda h, s: None

type_def_body %= G.Epsilon, lambda h, s: []
type_def_body %= member_def + type_def_body, lambda h, s: [s[1]] + s[2]
member_def %= method_def, lambda h, s:  s[1]
member_def %= attr_def, lambda h, s: s[1]

#methods
method_def %= (
    idx + opar + params_list_eps + cpar + opt_typing + arrow + simple_expr + s_colon,
    lambda h,s: ast.MethodDefNode(s[2], s[4], s[8], s[6])                     
)

method_def %= (
    idx + opar + params_list_eps + cpar + opt_typing + block_expr, 
    lambda h,s: ast.MethodDefNode(s[2], s[4], s[7], s[6])                 
)

method_def %= (
    idx + opar + params_list_eps + cpar + opt_typing + block_expr, s_colon,
    lambda h,s: ast.MethodDefNode(s[2], s[4], s[7], s[6])                 
)

#attributes
attr_def %= idx + opt_typing + eq + lego_expr, lambda h, s: ast.AttrDefNode(s[1], s[4], s[2])

##### statements

#letin
let_in_stmt %= let + var_defs + in_ + expr, lambda h, s: ast.LetInNode(s[2], s[4])

var_defs %= typed_var + comma + var_defs, lambda h, s: [s[1]] + s[3]
var_defs %= typed_var, lambda h, s: [s[1]]

typed_var %= idx + opt_typing + eq + expr, lambda h, s: ast.VarDefNode(s[1], s[4], s[2])
 
#if_else
if_else_stmt %= if_ + opar + expr + cpar + expr + elif_stmts + else_ + expr, lambda h, s: ast.IfElseNode([(s[3], s[5])] + s[6], s[8])

elif_stmts %= elif_ + opar + expr + cpar + expr + elif_stmts, lambda h, s: [(s[3], s[5])] + s[6]
elif_stmts %= G.Epsilon, lambda h, s: []

#loopsssss
while_stmt %= while_ + opar + expr + cpar + expr, lambda h, s: ast.WhileNode(s[3], s[5])
for_stmt %= for_ + opar + idx + in_ + expr + cpar + expr, lambda h, s: ast.ForNode(s[3], s[5], s[7])

#func_call
func_call %= idx + opar + expr_list_comma_eps + cpar, lambda h, s: ast.FuncCallNode(s[1], s[3])

#hierarchy
#destructive assignment has right asociation 
d_assign_op %= or_op + d_assign + d_assign_op, lambda h, s: ast.DestructiveAssignNode(s[1], s[3])
d_assign_op %= or_op, lambda h, s: s[1]

or_op %= or_op + or_ + and_op, lambda h, s: ast.OrNode(s[1], s[3])
or_op %= and_op, lambda h, s: s[1]

and_op %= and_op + and_ + eq_op, lambda h, s: ast.AndNode(s[1], s[3])
and_op %= eq_op, lambda h, s: s[1]

eq_op %= eq_op + eq + ineq_op, lambda h, s: ast.EqualNode(s[1], s[3])
eq_op %= eq_op + neq + ineq_op, lambda h, s: ast.NotEqualNode(s[1], s[3])
eq_op %= ineq_op, lambda h, s: s[1]

ineq_op %= ineq_op + le + type_test_op, lambda h, s: ast.LessOrEqualNode(s[1], s[3])
ineq_op %= ineq_op + ge + type_test_op, lambda h, s: ast.GreaterOrEqualNode(s[1], s[3])
ineq_op %= ineq_op + lt + type_test_op, lambda h, s: ast.LessThanNode(s[1], s[3])
ineq_op %= ineq_op + gt + type_test_op, lambda h, s: ast.GreaterThanNode(s[1], s[3])
ineq_op %= type_test_op, lambda h, s: s[1]

type_test_op %= concat_op + is_ + idx, lambda h, s: ast.IsNode(s[1], s[3])
type_test_op %= concat_op + as_ + idx, lambda h, s: ast.AsNode(s[1], s[3])
type_test_op %= concat_op, lambda h, s: s[1]

concat_op %= concat_op + at + add_sub_op,  lambda h, s: ast.ConcatNode(s[1], s[3])
concat_op %= concat_op + double_at + add_sub_op, lambda h, s: ast.ConcatNode(s[1], ast.ConcatNode(ast.ConstStrNode("\" \""),s[3]))
concat_op %= add_sub_op, lambda h, s: s[1]

add_sub_op %= add_sub_op + plus + mul_div_op, lambda h, s: ast.AddNode(s[1], s[3])
add_sub_op %= add_sub_op + minus + mul_div_op, lambda h, s: ast.SubNode(s[1], s[3])
add_sub_op %= mul_div_op, lambda h, s: s[1]

mul_div_op %= mul_div_op + star + neg_op, lambda h, s: ast.MulNode(s[1], s[3])
mul_div_op %= mul_div_op + div + neg_op, lambda h, s: ast.DivNode(s[1], s[3])
mul_div_op %= mul_div_op + mod + neg_op, lambda h, s: ast.ModNode(s[1], s[3])
mul_div_op %= neg_op, lambda h, s: s[1]

#neg stands for negation
neg_op %= minus + pow_op, lambda h, s: ast.NegNode(s[2])
neg_op %= pow_op, lambda h, s: s[1]

#pow has right asociation 
pow_op %= inst_op + pow + pow_op, lambda h, s: ast.PowNode(s[1], s[3], s[2])
pow_op %= inst_op + pow2 + pow_op, lambda h, s: ast.PowNode(s[1], s[3], s[2])
pow_op %= inst_op, lambda h, s: s[1]

#inst stands for instantiation
inst_op %= new + idx + opar + expr_list_comma_eps + cpar, lambda h, s: ast.InstantiationNode(s[2], s[4])
inst_op %= not_op, lambda h, s: s[1]

not_op %= not_ + member_call, lambda h, s: ast.NotNode(s[2])
not_op %= member_call, lambda h, s: s[1]

member_call %= member_call + dot + idx + opar + expr_list_comma_eps + cpar, lambda h, s: ast.MethodCallNode(s[1], s[3], s[5])
member_call %= member_call + dot + idx, lambda h, s: ast.AttrCallNode(s[1], s[3])
member_call %= paren_expr, lambda h, s: s[1]

#parenthesized expression
paren_expr %= opar + expr + cpar, lambda h, s: s[2]
paren_expr %= atom, lambda h, s: s[1]

atom %= idx, lambda h, s: ast.VarNode(s[1])
atom %= number_lit, lambda h, s: ast.ConstNumNode(s[1])
atom %= bool_lit, lambda h, s: ast.ConstBoolNode(s[1])
atom %= string_lit, lambda h, s: ast.ConstStrNode(s[1])
atom %= func_call, lambda h, s: s[1]
atom %= base + opar + expr_list_comma_eps + cpar, lambda h, s:  ast.BaseCallNode(s[3])







 
