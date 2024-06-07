from common.pycompiler import Grammar
import semantics.ast as ast

# grammar
G = Grammar()

# non-terminals
program = G.NonTerminal('<program>', startSymbol=True)

definition_list = G.NonTerminal('<definition-list>') 
definition = G.NonTerminal('<definition>') 
func_def = G.NonTerminal('<func-def>') 
type_def = G.NonTerminal('<type-def>') 

expr = G.NonTerminal('<expr>') 
simple_expr = G.NonTerminal('<simple-expr>') 
block_expr = G.NonTerminal('<block-expr>') 
expr_list = G.NonTerminal('<expr-list>') 
lego_expr = G.NonTerminal('<lego-expr>') 

let_in_stmt = G.NonTerminal('<let-in-stmt>')
while_stmt = G.NonTerminal('<while-stmt>')
for_stmt = G.NonTerminal('<for-stmt>')
if_else_stmt = G.NonTerminal('<if-else-stmt>')
d_assign = G.NonTerminal('<d-assign>')
args_list = G.NonTerminal('<args-list>')
typed_arg = G.NonTerminal('<typed-arg>') 
opt_typing = G.NonTerminal('<opt-typing>')


# terminals
type_, inherits, base, idx, new, is_ , as_ = G.Terminals('type inherits base <id> new is as')
let, in_, equal, d_assign_op = G.Terminals('let in = :=')
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

definition %= func_def, lambda h,s: s[1]
definition %= type_def, lambda h,s: s[1]          

expr %= simple_expr, lambda h,s: s[1]
expr %= block_expr, lambda h,s: s[1]

simple_expr %= let_in_stmt, lambda h, s: s[1]   
simple_expr %= while_stmt, lambda h, s: s[1]
simple_expr %= for_stmt, lambda h, s: s[1]
simple_expr %= if_else_stmt, lambda h, s: s[1]
simple_expr %= d_assign, lambda h, s: s[1]

block_expr %= ocur + expr_list + ccur, lambda h,s: ast.ExpressionBlockNode(s[2])

expr_list %= lego_expr + expr_list, lambda h,s: [s[1]] + s[2]
expr_list %= lego_expr, lambda h,s: [s[1]] 
expr_list %= simple_expr, lambda h,s: [s[1]]

lego_expr %= expr + s_colon, lambda h,s: s[1]
lego_expr %= block_expr, lambda h,s: s[1]

##
func_def %= (
    function + idx + opar + args_list + cpar + opt_typing + arrow + simple_expr + s_colon,
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[8], s[6])
)

func_def %= (
    function + idx + opar + args_list + cpar + opt_typing + block_expr, 
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[7], s[6])
)

func_def %= (
    function + idx + opar + args_list + cpar + opt_typing + block_expr, s_colon,
    lambda h,s: ast.FunctionDefinitionNode(s[2], s[4], s[7], s[6])
)

args_list %= typed_arg + comma + args_list, lambda h, s: [s[1]] + s[3]
args_list %= typed_arg, lambda h,s: [s[1]]
args_list %= G.Epsilon, lambda h,s: []

typed_arg %= idx + opt_typing, lambda h, s: (s[1], s[2])

opt_typing %= colon + idx, lambda h, s: s[2]
opt_typing %= G.Epsilon, lambda h, s: None
 