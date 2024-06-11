from common.utils import Scope  
from typing import List, Tuple

class Node():
    def __init__(self):
        self.scope: Scope

class DefNode(Node):
    pass

class ExprNode(Node):
    pass

class ExprBlockNode(ExprNode):
    def __init__(self, expr_list):
        super().__init__()
        self.expr_list = expr_list

class AtomicNode(ExprNode):
    def __init__(self, lex):
        super().__init__()
        self.lex = lex

class BinaryNode(ExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.oper = None

class UnaryNode(ExprNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand
        self.oper = None

class ConstNumNode(AtomicNode):
    pass

class ConstBoolNode(AtomicNode):
    pass

class ConstStrNode(AtomicNode):
    pass

class VarNode(AtomicNode):
    pass

class StrBinaryNode(BinaryNode):
    pass

class BoolBinaryNode(BinaryNode):
    pass

class ArithmeticExprNode(BinaryNode):
    pass

class EqualityExprNode(BinaryNode):
    pass

class InequalityExprNode(BinaryNode):
    pass

class NotNode(UnaryNode):
    pass

class NegNode(UnaryNode):
    pass

class ProgramNode(Node):
    # def_list: List[DefNode]
    # expr: ExprNode
    def __init__(self, def_list, expr):
        super().__init__()
        self.def_list = def_list
        self.expr = expr

class FuncDefNode(DefNode):                
    def __init__(self, idx, params, expr, ret_type=None):   #( store params in tuples??) 
        super().__init__() 
        self.id = idx               
        self.param_ids, self.param_types = zip(*params) if params else ([], [])
        self.expr = expr
        self.ret_type = ret_type

class TypeDefNode(DefNode):                      
    def __init__(self, idx, args, body, parent_type, parent_args=None):
        super().__init__()
        self.idx = idx
        self.param_ids, self.param_types = zip(*args) if args else (None, None)
        self.method_list = [method for method in body if isinstance(method, MethodDefNode)]
        self.attr_list = [attr for attr in body if isinstance(attr, AttrDefNode)]
        self.parent_type = parent_type
        self.parent_args = parent_args

class MethodDefNode(DefNode):                  
    def __init__(self, idx, params, expr, ret_type=None):    #( store params in tuples??) 
        super().__init__()       
        self.id = idx                                       
        self.param_ids, self.param_types = zip(*params) if params else ([], [])
        self.expr = expr
        self.ret_type = ret_type

class AttrDefNode(DefNode):
    def __init__(self, idx, expr, type_=None):     
        super().__init__()
        self.id = idx
        self.expr = expr
        self.type_ = type_

class InstantiationNode(ExprNode):
    def __init__(self, idx, args):
        super().__init__()
        self.idx = idx
        self.args = args

class IfElseNode(ExprNode):                         
    def __init__(self, if_stmts: List[Tuple], else_expr):
        super().__init__()
        cond_list, expr_list = zip(*if_stmts)
        self.cond_list = cond_list
        self.expr_list = expr_list
        self.else_expr = else_expr

class WhileNode(ExprNode):
    def __init__(self, cond, expr):
        super().__init__()
        self.cond = cond
        self.expr = expr

class ForNode(ExprNode):
    def __init__(self, var, iter, expr):
        super().__init__()
        self.var = var
        self.iter = iter
        self.expr = expr

class LetInNode(ExprNode):
    def __init__(self, var_defs, body):
        super().__init__()
        self.var_defs = var_defs
        self.body = body

class VarDefNode(DefNode):
    def __init__(self, idx, expr, type_=None):
        super().__init__()
        self.id = idx
        self.expr = expr
        self.type_ = type_    

class DestructiveAssignNode(ExprNode):
    def __init__(self, var, expr):
        super().__init__()
        self.var = var
        self.expr = expr       

class IsNode(ExprNode):
    def __init__(self, expr, type_):
        super().__init__()
        self.expr = expr
        self.type_ = type_                       

class AsNode(ExprNode):
    def __init__(self, expr, type_):
        super().__init__()
        self.expr = expr               
        self.type_ = type_                   

class FuncCallNode(ExprNode):
    def __init__(self, idx, args):
        super().__init__()
        self.idx = idx
        self.args = args

class AttrCallNode(ExprNode):
    def __init__(self, obj, attr):
        super().__init__()
        self.obj = obj
        self.attr = attr

class MethodCallNode(ExprNode):
    def __init__(self, obj, method, args):
        super().__init__()
        self.obj = obj
        self.method = method
        self.args = args

class BaseCallNode(ExprNode):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.method_idx = None         
        self.parent_type = None

####################        OPS
class AddNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '+'

class SubNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '-'

class MulNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '*'

class DivNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '/'

class ModNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '%'

class PowNode(ArithmeticExprNode):
    def __init__(self, lvalue, rvalue, oper):
        super().__init__(lvalue, rvalue)
        self.oper = oper
class EqualNode(EqualityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '=='

class NotEqualNode(EqualityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '!='

class LessThanNode(InequalityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '<'

class GreaterThanNode(InequalityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '>'

class LessOrEqualNode(InequalityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '<='

class GreaterOrEqualNode(InequalityExprNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '>='

class OrNode(BoolBinaryNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '|'

class AndNode(BoolBinaryNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '&'

class ConcatNode(StrBinaryNode):
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)
        self.oper = '(@, @@)'