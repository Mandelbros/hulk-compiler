from src.common.pycompiler import Grammar
from src.lexer.regex_ast import *

G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z, S = G.NonTerminals('T F A X Y Z S')
pipe, star, opar, cpar, symbol, epsilon, plus, minus, qmark, obrack, cbrack = G.Terminals('| * ( ) symbol ε + - ? [ ] ')

E %= E + pipe + T, lambda h, s: UnionNode(s[1], s[3])
E %= T, lambda h, s: s[1]
T %= T + F, lambda h, s: ConcatNode(s[1], s[2])
T %= F, lambda h, s: s[1]
F %= F + star, lambda h, s: ClosureNode(s[1])
F %= F + plus, lambda h, s: PClosureNode(s[1])
F %= F + qmark, lambda h, s: OptionalNode(s[1])
F %= A, lambda h, s: s[1]
A %= opar + E + cpar, lambda h, s: s[2]
A %= symbol, lambda h, s: SymbolNode(s[1])
A %= epsilon, lambda h, s: EpsilonNode(s[1])
A %= obrack + S + cbrack, lambda h, s: SymbolSetNode(s[2])
S %= symbol, lambda h, s: [SymbolNode(s[1])]
S %= symbol + S, lambda h, s: [SymbolNode(s[1])] + s[2]
S %= symbol + minus + symbol, lambda h, s: RangeNode(SymbolNode(s[1]), SymbolNode(s[3])).evaluate()
S %= symbol + minus + symbol + S, lambda h, s: RangeNode(SymbolNode(s[1]), SymbolNode(s[3])).evaluate() + s[4]


