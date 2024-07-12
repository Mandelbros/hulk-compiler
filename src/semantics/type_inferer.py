from src.semantics.hulk_ast import *
from src.common.semantic import *
import src.common.visitor as visitor

class TypeInferer(object):
    def __init__(self, context, errors = []):
        self.context = context
        self.current_type = None # Keep track of the current type being defined
        self.current_method = None # Keep track of the current method being defined
        self.errors = errors
        self.changed = False # Whether it got new infered types

    def add_infered_type(self, node, scope, infered_type):
        """If the node is a VarNode, with a variable defined in the scope, whose type is AutoType, adds the infered type to it's inferences array.

        Args:
            node: The AST node.
            scope: The scope of definition.
            infered_type: the type infered for the node.

        Returns:
            None
        """
        if isinstance(infered_type, AutoType):
            return
        # If it is a defined variable
        if isinstance(node, VarNode) and scope.is_defined(node.lex):
            var_info = scope.find_variable(node.lex)
            # If has AutoType
            if not isinstance(var_info.type, AutoType) or isinstance(var_info.type, ErrorType):
                return
            var_info.infered_types.append(infered_type)
            if not isinstance(infered_type, AutoType):
                self.changed = True
        
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        # Visit the function and type definitions
        for definition in node.def_list:
            self.visit(definition)

        # Visit the global expression
        self.visit(node.expr)

        # If types changed (got new infered types), revisit the entire AST
        if self.changed:
            self.changed = False
            self.visit(node)

    @visitor.when(TypeDefNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        if isinstance(self.current_type, ErrorType):
            return

        attr_scope = node.scope.children[0]

        arg_types = [self.visit(arg) for arg in node.parent_params]

        if not isinstance(self.current_type.parent, ErrorType):
            for arg, param_type in zip(node.parent_params, self.current_type.parent.param_types):
                self.add_infered_type(arg, arg.scope, param_type)

            for i in range(min(len(self.current_type.parent.param_types), len(arg_types))):
                param_type = self.current_type.parent.param_types[i]
                arg = arg_types[i]
                if isinstance(param_type, AutoType):
                    var = self.current_type.parent.param_vars[i]
                    var.infered_types.append(arg)
                    self.changed = True

        for attr in node.attr_list:
            self.visit(attr)

        # Infer the types of the params
        for i in range(len(self.current_type.param_types)):
            param_id = self.current_type.param_ids[i]
            param_type = self.current_type.param_types[i]
            local_var = attr_scope.find_variable(param_id)
            local_var.type = param_type

            # Infer the param type from the body of the methods
            if isinstance(param_type, AutoType) and local_var.is_param and local_var.infered_types:
                try:
                    most_specialized_type = get_most_specialized_type(local_var.infered_types, var_name = param_id)
                except SemanticError as e:
                    e.pos = node.pos
                    self.errors.append(e)
                    most_specialized_type = ErrorType()
                self.current_type.param_types[i] = most_specialized_type
                if not isinstance(most_specialized_type, AutoType):
                    self.changed = True
                local_var.type = most_specialized_type
                local_var.infered_types = []

            # Infer the param type from the calls to the methods
            if isinstance(self.current_type.param_types[i], AutoType) and self.current_type.param_vars[i].infered_types:
                lca_type = get_list_lowest_common_ancestor(self.current_type.param_vars[i].infered_types)
                self.current_type.param_types[i] = lca_type
                if not isinstance(lca_type, AutoType):
                    self.changed = True
                local_var.type = lca_type
                self.current_type.param_vars[i].infered_types = []

        for method in node.method_list:
            self.visit(method)

        self.current_type = None

    @visitor.when(AttrDefNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)

        attr = self.current_type.get_attribute(node.id)
        
        if isinstance(attr.type, AutoType):
            attr.type = expr_type
            
        return attr.type

    @visitor.when(MethodDefNode)
    def visit(self, node):
        self.current_method = self.current_type.get_method(node.id)

        method_scope = node.body_expr.scope
        return_type = self.visit(node.body_expr)

        if isinstance(self.current_method.return_type, AutoType) and not isinstance(return_type, AutoType):
            self.changed = True
            self.current_method.return_type = return_type

        # Infer the types of the params
        for i in range(len(self.current_method.param_types)):
            param_id = self.current_method.param_ids[i]
            param_type = self.current_method.param_types[i]
            local_var = method_scope.find_variable(param_id)
            local_var.type = param_type

            # Infer the param type from the body of the method
            if isinstance(param_type, AutoType) and local_var.is_param and local_var.infered_types:
                try:
                    most_specialized_type = get_most_specialized_type(local_var.infered_types, var_name = param_id)
                except SemanticError as e:
                    e.pos = node.pos
                    self.errors.append(e)
                    most_specialized_type = ErrorType()
                self.current_method.param_types[i] = most_specialized_type
                if not isinstance(most_specialized_type, AutoType):
                    self.changed = True
                local_var.type = most_specialized_type
                local_var.infered_types = []

            # Infer the param type from calls to the method
            if isinstance(self.current_method.param_types[i], AutoType) and self.current_method.param_vars[i].infered_types:
                lca_type = get_list_lowest_common_ancestor(self.current_method.param_vars[i].infered_types)
                self.current_method.param_types[i] = lca_type
                if not isinstance(lca_type, AutoType):
                    self.changed = True
                local_var.type = lca_type
                self.current_method.param_vars[i].infered_types = []

        self.current_method = None
        return return_type

    @visitor.when(FuncDefNode)
    def visit(self, node):
        function = self.context.get_function(node.id)

        return_type = self.visit(node.body_expr)

        if isinstance(function.return_type, AutoType) and not isinstance(return_type, AutoType):
            self.changed = True
            function.return_type = return_type

        expr_scope = node.body_expr.scope

        # Infer the types of the params
        for i in range(len(function.param_types)):
            param_id = function.param_ids[i]
            param_type = function.param_types[i]
            local_var = expr_scope.find_variable(param_id)
            local_var.type = param_type

            # Infer the param type from the body of the function
            if isinstance(param_type, AutoType) and local_var.is_param and local_var.infered_types:
                try:
                    most_specialized_type = get_most_specialized_type(local_var.infered_types, var_name = param_id)
                except SemanticError as e:
                    e.pos = node.pos
                    self.errors.append(e)
                    most_specialized_type = ErrorType()
                function.param_types[i] = most_specialized_type
                if not isinstance(most_specialized_type, AutoType):
                    self.changed = True
                local_var.type = most_specialized_type
                local_var.infered_types = []

            # Infer the param type from calls to the function
            if isinstance(function.param_types[i], AutoType) and function.param_vars[i].infered_types:
                lca_type = get_list_lowest_common_ancestor(function.param_vars[i].infered_types)
                function.param_types[i] = lca_type
                if not isinstance(lca_type, AutoType):
                    self.changed = True
                local_var.type = lca_type
                function.param_vars[i].infered_types = []

        return return_type

    @visitor.when(ExprBlockNode)
    def visit(self, node):
        expr_type = ErrorType()
        for expr in node.expr_list:
            expr_type = self.visit(expr)
        return expr_type

    @visitor.when(LetInNode)
    def visit(self, node):
        for definition in node.var_defs:
            self.visit(definition)
        return self.visit(node.body)
    
    @visitor.when(VarDefNode)
    def visit(self, node):
        infered_type = self.visit(node.expr)

        var = node.scope.find_variable(node.id)

        if isinstance(var.type, AutoType):
            var.type = infered_type
            
        return var.type

    @visitor.when(DestructiveAssignNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        var_type = self.visit(node.var)

        if isinstance(var_type, SelfType):
            return print(ErrorType())

        if isinstance(expr_type, AutoType) and not isinstance(var_type, AutoType):
            self.add_infered_type(node.expr, node.scope, var_type)

        return var_type
    
    @visitor.when(AttrAssignNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        var_type = self.visit(node.id)

        if not isinstance(var_type, SelfType):
            return ErrorType()
        
        var_type = self.current_type.get_attribute(node.attr).type

        if isinstance(expr_type, AutoType) and not isinstance(var_type, AutoType):
            self.add_infered_type(node.expr, node.scope, var_type)

        return var_type

    @visitor.when(IfElseNode)
    def visit(self, node):
        conditions = [stmt[0] for stmt in node.if_stmts]
        expressions = [stmt[1] for stmt in node.if_stmts]

        for cond in conditions:
            self.visit(cond)

        expr_types = [self.visit(expression) for expression in expressions]

        else_type = self.visit(node.else_expr)

        return get_list_lowest_common_ancestor(expr_types + [else_type])

    @visitor.when(WhileNode)
    def visit(self, node):
        self.visit(node.cond)
        return self.visit(node.body_expr)
    
    @visitor.when(ForNode)
    def visit(self, node):
        return ErrorType()

    @visitor.when(InstantiationNode)
    def visit(self, node):
        arg_types = [self.visit(arg) for arg in node.args]

        try:
            type_ = self.context.get_type(node.id)
        except SemanticError:
            return ErrorType()

        if isinstance(type_, ErrorType):
            return ErrorType()

        for arg, param_type in zip(node.args, type_.param_types):
            self.add_infered_type(arg, node.scope, param_type)

        for i in range(min(len(type_.param_types), len(arg_types))):
            param_type = type_.param_types[i]
            arg = arg_types[i]
            if isinstance(param_type, AutoType):
                var = type_.param_vars[i]
                var.infered_types.append(arg)
                self.changed = True

        return type_

    @visitor.when(IsNode)
    def visit(self, node):
        self.visit(node.expr)
        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node):
        self.visit(node.expr)

        try:
            cast_type = self.context.get_type_or_protocol(node.type_)
        except SemanticError:
            cast_type = ErrorType()

        return cast_type
    
    @visitor.when(AttrCallNode)
    def visit(self, node):
        obj_type = self.visit(node.obj)
        if isinstance(obj_type, SelfType):
            try:
                attr = self.current_type.get_attribute(node.attr)
                return attr.type
            except SemanticError:
                return ErrorType()
        else:
            return ErrorType()

    @visitor.when(MethodCallNode)
    def visit(self, node):
        scope = node.scope
        prev_expr_type = self.visit(node.prev_expr)
        arg_types = [self.visit(arg) for arg in node.args]

        if isinstance(prev_expr_type, ErrorType):
            return ErrorType()

        try:
            if isinstance(prev_expr_type, SelfType):
                method = self.current_type.get_method(node.method_id)
            else:
                method = prev_expr_type.get_method(node.method_id)
        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, method.param_types):
            self.add_infered_type(arg, scope, param_type)

        for i in range(min(len(method.param_types), len(arg_types))):
            method_param_type = method.param_types[i]
            arg = arg_types[i]
            if isinstance(method_param_type, AutoType):
                var = method.param_vars[i]
                var.infered_types.append(arg)
                self.changed = True

        return method.return_type
    
    @visitor.when(FuncCallNode)
    def visit(self, node):
        scope = node.scope

        arg_types = [self.visit(arg) for arg in node.args]

        try:
            function = self.context.get_function(node.id)
        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, function.param_types):
            self.add_infered_type(arg, scope, param_type)

        for i in range(min(len(function.param_types), len(arg_types))):
            func_param_type = function.param_types[i]
            arg = arg_types[i]
            if isinstance(func_param_type, AutoType):
                var = function.param_vars[i]
                var.infered_types.append(arg)
                self.changed = True

        return function.return_type

    @visitor.when(BaseCallNode)
    def visit(self, node):
        scope = node.scope
        arg_types = [self.visit(arg) for arg in node.args]

        if self.current_method is None:
            return ErrorType()

        try:
            method = self.current_type.parent.get_method(self.current_method.name)
        except SemanticError:
            return ErrorType()

        for arg, param_type in zip(node.args, method.param_types):
            self.add_infered_type(arg, scope, param_type)

        for i in range(min(len(method.param_types), len(arg_types))):
            method_param_type = method.param_types[i]
            arg_type = arg_types[i]
            if isinstance(method_param_type, AutoType):
                var = method.param_vars[i]
                var.infered_types.append(arg_type)
                self.changed = True

        return method.return_type

    @visitor.when(EqualityExprNode)
    def visit(self, node):
        self.visit(node.lvalue)
        self.visit(node.rvalue)

        return self.context.get_type('Boolean')

    @visitor.when(InequalityExprNode)
    def visit(self, node):
        scope = node.scope
        
        number_type = self.context.get_type('Number')
        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if isinstance(lvalue_type, AutoType):
            self.add_infered_type(node.lvalue, scope, number_type)
        elif not isinstance(lvalue_type, NumberType):
            return ErrorType()

        if isinstance(rvalue_type, AutoType):
            self.add_infered_type(node.rvalue, scope, number_type)
        elif not isinstance(rvalue_type, NumberType):
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(BoolBinaryNode)
    def visit(self, node):
        scope = node.scope

        bool_type = self.context.get_type('Boolean')
        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if isinstance(lvalue_type, AutoType):
            self.add_infered_type(node.lvalue, scope, bool_type)
        elif not isinstance(lvalue_type, BoolType):
            return ErrorType()

        if isinstance(rvalue_type, AutoType):
            self.add_infered_type(node.rvalue, scope, bool_type)
        elif not isinstance(rvalue_type, BoolType):
            return ErrorType()

        return bool_type
    
    @visitor.when(ArithmeticExprNode)
    def visit(self, node):
        scope = node.scope

        number_type = self.context.get_type('Number')
        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if isinstance(lvalue_type, AutoType):
            self.add_infered_type(node.lvalue, scope, number_type)
        elif not isinstance(lvalue_type, NumberType):
            return ErrorType()

        if isinstance(rvalue_type, AutoType):
            self.add_infered_type(node.rvalue, scope, number_type)
        elif not isinstance(rvalue_type, NumberType):
            return ErrorType()

        return number_type

    @visitor.when(StrBinaryNode)
    def visit(self, node):
        scope = node.scope

        object_type = self.context.get_type('Object')
        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if isinstance(lvalue_type, AutoType):
            self.add_infered_type(node.lvalue, scope, object_type)
        elif isinstance(lvalue_type, ErrorType):
            return ErrorType()

        if isinstance(rvalue_type, AutoType):
            self.add_infered_type(node.rvalue, scope, object_type)
        elif isinstance(rvalue_type, ErrorType):
            return ErrorType()

        return self.context.get_type('String')

    @visitor.when(NegNode)
    def visit(self, node):
        scope = node.scope

        number_type = self.context.get_type('Number')
        operand_type = self.visit(node.operand)

        if isinstance(operand_type, AutoType):
            self.add_infered_type(node.operand, scope, number_type)
        elif not isinstance(operand_type, NumberType):
            return ErrorType()

        return number_type

    @visitor.when(NotNode)
    def visit(self, node):
        scope = node.scope

        bool_type = self.context.get_type('Boolean')
        operand_type = self.visit(node.operand)

        if isinstance(operand_type, AutoType):
            self.add_infered_type(node.operand, scope, bool_type)
        elif not isinstance(operand_type, BoolType):
            return ErrorType()

        return bool_type
    
    @visitor.when(VarNode)
    def visit(self, node):
        var = node.scope.find_variable(node.lex)

        if var is None:
            return ErrorType()
        return var.type

    @visitor.when(ConstBoolNode)
    def visit(self, node):
        return self.context.get_type('Boolean')

    @visitor.when(ConstNumNode)
    def visit(self, node):
        return self.context.get_type('Number')

    @visitor.when(ConstStrNode)
    def visit(self, node):
        return self.context.get_type('String')