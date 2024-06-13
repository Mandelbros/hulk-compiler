from common.automata import NFA, DFA, nfa_to_dfa
from common.automata import automata_union, automata_concatenation, automata_closure, automata_minimization

EPSILON = 'ε'    ######################### ?

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1, finals=[0], transitions={})

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return DFA(states=2, finals=[1], transitions={(0, s) : 1})

SymbolNode('a').evaluate() 

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)
    
ClosureNode(SymbolNode('a')).evaluate()

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)

UnionNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)

ConcatNode(SymbolNode('a'), SymbolNode('b')).evaluate()

class PClosureNode(UnaryNode):
    @staticmethod
    def operate(value):        
        return automata_concatenation(value, value.automata_closure())
    
class OptionalNode(UnaryNode):
    @staticmethod
    def operate(value):        
        return automata_union(value, EpsilonNode(EPSILON).evaluate())
    
class SymbolSetNode(Node):
    def __init__(self, symbols: list[SymbolNode]) -> None:
        self.symbols = symbols

    def evaluate(self):
        value = self.symbols[0].evaluate()  
        for symbol in self.symbols[1:]:            
            value = value.automata_union(symbol.evaluate())  
        return value

class RangeNode(Node):
    def __init__(self, first: SymbolNode, last: SymbolNode) -> None:
        self.first = first
        self.last = last

    def evaluate(self):
        value = [self.first]
        for i in range(ord(self.first.lex) + 1, ord(self.last.lex)):
            value.append(SymbolNode(chr(i)))
        value.append(self.last)
        return value