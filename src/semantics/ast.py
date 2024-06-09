from common.utils import Scope 

class Node:
    def __init__(self):
        self.scope: Scope

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DefinitionNode(Node):
    pass

class FunctionDefinitionNode(DefinitionNode):
    def __init__(self, idx, args, expr, ret_type=None):
        super().__init__()
        params_ids, params_types = zip(*args) if args else ([], [])
        self.id = idx
        self.params_ids = params_ids        #( store params in tuples??)
        self.params_types = params_types
        self.expr = expr
        self.ret_type = ret_type