from src.semantics.hulk_ast import *
import src.common.visitor as visitor
from src.common.semantic import SemanticError, ErrorType, AutoType, SelfType, VariableInfo, NumberType, BoolType

class ScopeBuilder(object):
    def __init__(self, context, errors = []):
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope = None):
        # Create global scope
        scope = Scope()

        # Define default variables
        scope.define_variable('PI', NumberType())
        scope.define_variable('E', NumberType())
        scope.define_variable('true', BoolType())
        scope.define_variable('false', BoolType())

        node.scope = scope

        # Visit the function and type definitions
        for definition in node.def_list:
            self.visit(definition, scope.create_child())

        # Visit global expression
        self.visit(node.expr, scope.create_child())

        return scope

    @visitor.when(TypeDefNode)
    def visit(self, node, scope):
        node.scope = scope

        # Current defined type, return if error
        self.current_type = self.context.get_type(node.id)
        if isinstance(self.current_type, ErrorType):
            return

        # Get parent params
        if node.parent_params == []:
            if node.param_ids == []:
                node.param_ids, node.param_types = self.current_type.param_ids, self.current_type.param_types = self.current_type.get_params()
                node.parent_params = [VarNode(param_id) for param_id in self.current_type.param_ids]

        # Scope for the type's attributes
        attr_scope = scope.create_child()

        # Build the attr_scope
        for i in range(len(self.current_type.param_ids)):
            param_id = self.current_type.param_ids[i]
            param_type = self.current_type.param_types[i]
            attr_scope.define_variable(param_id, param_type, is_param = True)
            self.current_type.param_vars.append(VariableInfo(param_id, param_type))

        # Visit parent's params
        for expr in node.parent_params:
            self.visit(expr, attr_scope.create_child())

        # Visit the attribute defs
        for attr in node.attr_list:
            self.visit(attr, attr_scope.create_child())

        # Scope for the type's methods
        methods_scope = scope.create_child()
        methods_scope.define_variable('self', SelfType(self.current_type))

        # Visit the method defs
        for method in node.method_list:
            self.visit(method, methods_scope.create_child())

    @visitor.when(AttrDefNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.expr, scope.create_child())

    @visitor.when(MethodDefNode)
    def visit(self, node, scope):
        node.scope = scope
        method_scope = scope.create_child()

        method = self.current_type.get_method(node.id)

        # Build the method_scope
        for i in range(len(method.param_ids)):
            param_id = method.param_ids[i]
            param_type = method.param_types[i]
            method_scope.define_variable(param_id, param_type, is_param = True)
            method.param_vars.append(VariableInfo(param_id, param_type))

        # Visite the body expression
        self.visit(node.body_expr, method_scope)

    @visitor.when(FuncDefNode)
    def visit(self, node, scope):
        node.scope = scope
        function_scope = scope.create_child()

        function = self.context.get_function(node.id)

        # Build the function_scope
        for i in range(len(function.param_ids)):
            param_id = function.param_ids[i]
            param_type = function.param_types[i]
            function_scope.define_variable(param_id, param_type, is_param = True)
            function.param_vars.append(VariableInfo(param_id, param_type))

        # Visite the body expression
        self.visit(node.body_expr, function_scope)

    @visitor.when(ExprBlockNode)
    def visit(self, node, scope):
        # Scope of the block
        block_scope = scope.create_child()
        node.scope = block_scope

        # Visit the block's expressions
        for expr in node.expr_list:
            self.visit(expr, block_scope.create_child())

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        node.scope = scope
        
        last_scope = scope
        # Progressively build the scope
        for definition in node.var_defs:
            self.visit(definition, last_scope)
            last_scope = definition.scope

        # Visite the body
        self.visit(node.body, last_scope.create_child())

    @visitor.when(VarDefNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope.create_child())

        node.scope = scope.create_child()

        # Resolve the variable's type
        if node.type_ is None:
            type_ = AutoType()
        else:
            try:
                type_ = self.context.get_type(node.type_)
            except SemanticError as e:
                self.errors.append(e)
                type_ = ErrorType()

        node.scope.define_variable(node.id, type_)

    @visitor.when(DestructiveAssignNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the variable
        self.visit(node.var, scope.create_child())
        # Visit the expression
        self.visit(node.expr, scope.create_child())

    @visitor.when(AttrAssignNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the attribute
        self.visit(node.id, scope.create_child())
        # Visit the expression
        self.visit(node.expr, scope.create_child())

    @visitor.when(IfElseNode)
    def visit(self, node, scope):
        node.scope = scope
        conditions = [stmt[0] for stmt in node.if_stmts]
        expressions = [stmt[1] for stmt in node.if_stmts]

        # Visit the conditions
        for condition in conditions:
            self.visit(condition, scope.create_child())

        # Visit the expressions of the 'if's/'elif's
        for expression in expressions:
            self.visit(expression, scope.create_child())

        # Visit the expression of the 'else'
        self.visit(node.else_expr, scope.create_child())

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the condition
        self.visit(node.cond, scope.create_child())
        # Visit the body expression
        self.visit(node.body_expr, scope.create_child())

    @visitor.when(ForNode)
    def visit(self, node, scope):
        node.scope = scope
        # Scope of the for cycle
        for_scope = scope.create_child()

        # Define the iteration variable
        for_scope.define_variable(node.var, AutoType(), is_param = True)

        # Visit the iteration variable
        self.visit(node.iter, scope.create_child())
        # Visit the expression
        self.visit(node.expr, for_scope)

    @visitor.when(InstantiationNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the constructor's arguments
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(IsNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the expression
        self.visit(node.expr, scope.create_child())

    @visitor.when(AsNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the expression
        self.visit(node.expr, scope.create_child())

    @visitor.when(AttrCallNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the attribute's owner
        self.visit(node.obj, scope.create_child())

    @visitor.when(MethodCallNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the method's owner
        self.visit(node.prev_expr, scope.create_child())
        # Visit the call's arguments
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the call's arguments
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(BaseCallNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the call's arguments
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the left operand
        self.visit(node.lvalue, scope.create_child())
        # Visit the right operand
        self.visit(node.rvalue, scope.create_child())

    @visitor.when(UnaryNode)
    def visit(self, node, scope):
        node.scope = scope
        # Visit the unary operand
        self.visit(node.operand, scope.create_child())

    @visitor.when(VarNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(ConstBoolNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(ConstNumNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(ConstStrNode)
    def visit(self, node, scope):
        node.scope = scope