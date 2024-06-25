from common.semantic import Scope
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
    def __init__(self, idx, params, body_expr, ret_type=None):   #( store params in tuples??) 
        super().__init__() 
        self.id = idx               
        self.param_ids, self.param_types = zip(*params) if params else ([], [])
        self.body_expr = body_expr
        self.ret_type = ret_type

class TypeDefNode(DefNode):                      
    def __init__(self, idx, params, body, parent_type, parent_params=None):
        super().__init__()
        self.id = idx
        self.param_ids, self.param_types = zip(*params) if params else (None, None)
        self.method_list = [method for method in body if isinstance(method, MethodDefNode)]
        self.attr_list = [attr for attr in body if isinstance(attr, AttrDefNode)]
        self.parent_type = parent_type
        self.parent_params = parent_params

class MethodDefNode(DefNode):                  
    def __init__(self, idx, params, body_expr, ret_type=None):    #( store params in tuples??) 
        super().__init__()       
        self.id = idx                                       
        self.param_ids, self.param_types = zip(*params) if params else ([], [])
        self.body_expr = body_expr
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
        self.id = idx
        self.args = args

class IfElseNode(ExprNode):                        
    def __init__(self, if_stmts: List[Tuple], else_expr):
        super().__init__()
        self.if_stmts = if_stmts
        self.else_expr = else_expr

class WhileNode(ExprNode):              
    def __init__(self, cond, body_expr):
        super().__init__()
        self.cond = cond
        self.body_expr = body_expr

class ForNode(ExprNode):
    def __init__(self, var, iter, expr):
        super().__init__()
        self.var = var
        self.iter = iter
        self.expr = expr

class LetInNode(ExprNode):               
    def __init__(self, var_defs, body):
        super().__init__()
        self.var_defs : List[VarDefNode] = var_defs
        self.body : ExprNode = body

class VarDefNode(DefNode):              
    def __init__(self, idx, expr, type_=None):
        super().__init__()
        self.id = idx
        self.expr: ExprNode = expr
        self.type_ = type_    

class DestructiveAssignNode(ExprNode):
    def __init__(self, var_name, expr):
        super().__init__()
        self.var_name = var_name
        self.expr = expr       

class AttrAssignNode(ExprNode):
    def __init__(self, idx, attr, expr):
        super().__init__()
        self.id = idx
        self.attr = attr
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
        self.id = idx
        self.args = args

class AttrCallNode(ExprNode):
    def __init__(self, obj, attr):
        super().__init__()
        self.obj = obj
        self.attr = attr

class MethodCallNode(ExprNode):         
    def __init__(self, prev_expr, method_idx, args):
        super().__init__()
        self.prev_expr = prev_expr
        self.method_id = method_idx
        self.args = args

class BaseCallNode(ExprNode):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.method_id = None         
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