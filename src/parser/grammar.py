from common.pycompiler import Grammar
import semantics.ast as ast

# grammar
G = Grammar()

# non-terminals
program = G.NonTerminal('<program>', startSymbol=True)

class_list, def_class = G.NonTerminals('<class-list> <def-class>')
feature_list, def_attr, def_func = G.NonTerminals('<feature-list> <def-attr> <def-func>')
param_list, param, expr_list = G.NonTerminals('<param-list> <param> <expr-list>')
expr, arith, term, factor, atom = G.NonTerminals('<expr> <arith> <term> <factor> <atom>')
func_call, arg_list  = G.NonTerminals('<func-call> <arg-list>')


# terminals
plus, minus, star, div, mod, pow, pow2, number_lit = G.Terminals('+ - * / % ^ ** <number>')
eq, neq, le, ge, lt, gt = G.Terminals('== != <= >= < >')
semi, colon, comma, dot, opar, cpar, ocur, ccur = G.Terminals('; : , . ( ) { }')
and_ , or_, not_, bool_lit = G.Terminals('& | ! <bool>')
at, double_at, string_lit = G.Terminals('@ @@ <string>')
type_, inherits, base, idx, new, is_ , as_ = G.Terminals('type inherits base <id> new is as')
if_, elif_, else_ = G.Terminals('if elif else')
let, in_, equal, assign = G.Terminals('let in = :=')
while_, for_ = G.Terminals('while for')
function, arrow = G.Terminal('function =>')

# productions
program %= class_list, lambda h,s: ProgramNode(s[1])