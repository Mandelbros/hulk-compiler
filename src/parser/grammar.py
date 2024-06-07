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
semi, colon, comma, dot, opar, cpar, ocur, ccur = G.Terminals('; : , . ( ) { }')

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

# simple_expr %= 

block_expr %= ocur + expr_list + ccur, lambda h,s: ast.ExpressionBlockNode(s[2])

expr_list %= lego_expr + expr_list, lambda h,s: [s[1]] + s[2]
expr_list %= lego_expr, lambda h,s: [s[1]] 
expr_list %= simple_expr, lambda h,s: [s[1]]

lego_expr %= expr + semi, lambda h,s: s[1]
lego_expr %= block_expr, lambda h,s: s[1]

