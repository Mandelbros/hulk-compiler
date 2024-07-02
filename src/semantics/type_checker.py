from src.semantics.hulk_ast import *
from src.common.semantic import *
import src.common.visitor as visitor

class TypeChecker(object):
    def __init__(self, context, errors = None):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for definition in node.def_list:
            self.visit(definition)

        self.visit(node.expr)

    @visitor.when(TypeDefNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        if isinstance(self.current_type, ErrorType):
            return

        for attr in node.attr_list:
            self.visit(attr)

        for method in node.method_list:
            self.visit(method)

        if isinstance(self.current_type.parent, ErrorType):
            return

        parent_arg_types = [self.visit(expr) for expr in node.parent_params]

        parent_param_types = self.current_type.parent.param_types

        if len(parent_arg_types) != len(parent_param_types):
            self.errors.append(SemanticError(SemanticError.DIF_EXPECTED_ARGUMENTS % (
                len(parent_param_types), len(parent_arg_types), self.current_type.parent.name)))
            return ErrorType()

        for parent_arg_type, parent_param_type in zip(parent_arg_types, parent_param_types):
            if not parent_arg_type.conforms_to(parent_param_type):
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (parent_arg_type.name, parent_param_type.name)))

        self.current_type = None

    @visitor.when(AttrDefNode)
    def visit(self, node):
        infered_type = self.visit(node.expr)

        attr_type = self.current_type.get_attribute(node.id).type

        if not infered_type.conforms_to(attr_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, attr_type.name)))

        return attr_type

    @visitor.when(MethodDefNode)
    def visit(self, node):
        self.current_method = self.current_type.get_method(node.id)

        infered_type = self.visit(node.body_expr)

        if not infered_type.conforms_to(self.current_method.return_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, self.current_method.return_type.name)))

        return_type = self.current_method.return_type

        if self.current_type.parent is None or isinstance(self.current_type.parent, ErrorType):
            return return_type

        try:
            parent_method = self.current_type.parent.get_method(node.id)
        except SemanticError:
            return return_type

        if parent_method.return_type != return_type or len(parent_method.param_types) != len(self.current_method.param_types):
            self.errors.append(SemanticError(SemanticError.WRONG_SIGNATURE % self.current_method.name))
        else:
            for i in range(len(parent_method.param_types)):
                parent_param_type = parent_method.param_types[i]
                param_type = self.current_method.param_types[i]
                if parent_param_type != param_type:
                    self.errors.append(SemanticError(SemanticError.WRONG_SIGNATURE % self.current_method.name))

        self.current_method = None

        return return_type

    @visitor.when(FuncDefNode)
    def visit(self, node):
        function = self.context.get_function(node.id)

        infered_return_type = self.visit(node.body_expr)

        if not infered_return_type.conforms_to(function.return_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (infered_return_type.name, function.return_type.name)))
            return ErrorType()

        return function.return_type

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
        scope = node.scope

        infered_type = self.visit(node.expr)
        var_type = scope.find_variable(node.id).type

        if not infered_type.conforms_to(var_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (infered_type.name, var_type.name)))
            var_type = ErrorType()

        return var_type

    @visitor.when(DestructiveAssignNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        var_type = self.visit(node.var)

        if isinstance(var_type, SelfType):
            self.errors.append(SemanticError(SemanticError.SELF_IS_READONLY))
            return ErrorType()

        if not expr_type.conforms_to(var_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (expr_type.name, var_type.name)))
            return ErrorType()

        return var_type
    
    @visitor.when(AttrAssignNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)
        var_type = self.visit(node.id)

        if not isinstance(var_type, SelfType):
            self.errors.append(SemanticError(SemanticError.ATTR_ACCESS_FROM_NON_SELF))
            return ErrorType()
        
        var_type = self.current_type.get_attribute(node.attr).type

        if not expr_type.conforms_to(var_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (expr_type.name, var_type.name)))
            return ErrorType()

        return var_type

    @visitor.when(IfElseNode)
    def visit(self, node):
        conditions = [stmt[0] for stmt in node.if_stmts]
        expressions = [stmt[1] for stmt in node.if_stmts]

        cond_types = [self.visit(cond) for cond in conditions]

        for cond_type in cond_types:
            if cond_type != BoolType():
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (cond_type.name, BoolType().name)))

        expr_types = [self.visit(expr) for expr in expressions]

        else_type = self.visit(node.else_expr)

        return get_list_lowest_common_ancestor(expr_types + [else_type])

    @visitor.when(WhileNode)
    def visit(self, node):
        cond_type = self.visit(node.cond)

        if cond_type != BoolType():
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (cond_type.name, BoolType().name)))

        return self.visit(node.body_expr)
    
    @visitor.when(ForNode)
    def visit(self, node):
        return ErrorType()
    
    @visitor.when(InstantiationNode)
    def visit(self, node):
        try:
            type_ = self.context.get_type(node.id, params_len = len(node.args))
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()
        
        if isinstance(type_, ErrorType):
            return ErrorType()

        args_types = [self.visit(arg) for arg in node.args]

        if len(args_types) != len(type_.param_types):
            self.errors.append(SemanticError(SemanticError.DIF_EXPECTED_ARGUMENTS % (len(type_.param_types), len(args_types), type_.name)))
            return ErrorType()

        for arg_type, param_type in zip(args_types, type_.param_types):
            if not arg_type.conforms_to(param_type):
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (arg_type.name, param_type.name)))
                return ErrorType()

        return type_
    
    @visitor.when(IsNode)
    def visit(self, node):
        self.visit(node.expr)

        try:
            self.context.get_type(node.type_)
        except SemanticError as e:
            self.errors.append(e)

        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node):
        expr_type = self.visit(node.expr)

        try:
            cast_type = self.context.get_type(node.type_)
        except SemanticError as e:
            self.errors.append(e)
            cast_type = ErrorType()

        if not expr_type.conforms_to(cast_type) and not cast_type.conforms_to(expr_type):
            self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (expr_type.name, cast_type.name)))
            return ErrorType()

        return cast_type

    @visitor.when(AttrCallNode)
    def visit(self, node):
        obj_type = self.visit(node.obj)

        if isinstance(obj_type, ErrorType):
            return ErrorType()

        if obj_type == SelfType():
            try:
                attr = self.current_type.get_attribute(node.attr)
                return attr.type
            except SemanticError as e:
                self.errors.append(e)
                return ErrorType()
        else:
            self.errors.append(SemanticError(SemanticError.ATTR_ACCESS_FROM_NON_SELF))
            return ErrorType()

    @visitor.when(MethodCallNode)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]
        prev_expr_type = self.visit(node.prev_expr)

        if isinstance(prev_expr_type, ErrorType):
            return ErrorType()

        try:
            if prev_expr_type == SelfType():
                method = self.current_type.get_method(node.method_id)
            else:
                method = prev_expr_type.get_method(node.method_id)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        if len(args_types) != len(method.param_types):
            self.errors.append(SemanticError(SemanticError.DIF_EXPECTED_ARGUMENTS % (len(method.param_types), len(args_types), method.name)))
            return ErrorType()

        for arg_type, param_type in zip(args_types, method.param_types):
            if not arg_type.conforms_to(param_type):
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (arg_type.name, param_type.name)))
                return ErrorType()

        return method.return_type
    
    @visitor.when(FuncCallNode)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]

        try:
            function = self.context.get_function(node.id)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        if len(args_types) != len(function.param_types):
            self.errors.append(SemanticError(SemanticError.DIF_EXPECTED_ARGUMENTS % (
                len(function.param_types), len(args_types), function.name)))
            return ErrorType()

        for arg_type, param_type in zip(args_types, function.param_types):
            if not arg_type.conforms_to(param_type):
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (arg_type.name, param_type.name)))
                return ErrorType()

        return function.return_type

    @visitor.when(BaseCallNode)
    def visit(self, node):
        args_types = [self.visit(arg) for arg in node.args]

        if self.current_method is None:
            self.errors.append(SemanticError(SemanticError.BASE_OUTSIDE_METHOD))
            return ErrorType()

        try:
            method = self.current_type.parent.get_method(self.current_method.name)
            node.method_id = self.current_method.name
            node.parent_type = self.current_type.parent
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        if len(args_types) != len(method.param_types):
            self.errors.append(SemanticError(SemanticError.DIF_EXPECTED_ARGUMENTS % (len(method.param_types), len(args_types), method.name)))
            return ErrorType()

        for arg_type, param_type in zip(args_types, method.param_types):
            if not arg_type.conforms_to(param_type):
                self.errors.append(SemanticError(SemanticError.INCOMPATIBLE_TYPES % (arg_type.name, param_type.name)))
                return ErrorType()

        return method.return_type

    @visitor.when(EqualityExprNode)
    def visit(self, node):
        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if not lvalue_type.conforms_to(rvalue_type) and not rvalue_type.conforms_to(lvalue_type):
            self.errors.append(SemanticError(SemanticError.INVALID_OPERATION % (node.oper, lvalue_type.name, rvalue_type.name)))
            return ErrorType()

        return self.context.get_type('Boolean')

    @visitor.when(InequalityExprNode)
    def visit(self, node):
        bool_type = self.context.get_type('Boolean')

        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if lvalue_type != NumberType() or rvalue_type != NumberType():
            self.errors.append(SemanticError(SemanticError.INVALID_OPERATION % (node.oper, lvalue_type.name, rvalue_type.name)))
            return ErrorType()

        return bool_type

    @visitor.when(BoolBinaryNode)
    def visit(self, node):
        bool_type = self.context.get_type('Boolean')

        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if lvalue_type != BoolType() or rvalue_type != BoolType():
            self.errors.append(SemanticError(SemanticError.INVALID_OPERATION % (node.oper, lvalue_type.name, rvalue_type.name)))
            return ErrorType()

        return bool_type
    
    @visitor.when(ArithmeticExprNode)
    def visit(self, node):
        number_type = self.context.get_type('Number')

        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if lvalue_type != NumberType() or rvalue_type != NumberType():
            self.errors.append(SemanticError(SemanticError.INVALID_OPERATION % (node.oper, lvalue_type.name, rvalue_type.name)))
            return ErrorType()

        return number_type

    @visitor.when(StrBinaryNode)
    def visit(self, node):
        object_type = self.context.get_type('Object')

        lvalue_type = self.visit(node.lvalue)
        rvalue_type = self.visit(node.rvalue)

        if not lvalue_type.conforms_to(object_type) or not rvalue_type.conforms_to(object_type):
            self.errors.append(SemanticError(SemanticError.INVALID_OPERATION % (node.operator, lvalue_type.name, rvalue_type.name)))
            return ErrorType()

        return self.context.get_type('String')

    @visitor.when(NegNode)
    def visit(self, node):
        number_type = self.context.get_type('Number')
        operand_type = self.visit(node.operand)

        if operand_type != NumberType():
            self.errors.append(SemanticError(SemanticError.INVALID_UNARY_OPERATION % (node.oper, operand_type.name)))
            return ErrorType()

        return number_type

    @visitor.when(NotNode)
    def visit(self, node):
        bool_type = self.context.get_type('Boolean')
        operand_type = self.visit(node.operand)

        if operand_type != BoolType():
            self.errors.append(SemanticError(SemanticError.INVALID_UNARY_OPERATION % (node.oper, operand_type.name)))
            return ErrorType()

        return bool_type
    
    @visitor.when(VarNode)
    def visit(self, node):
        var = node.scope.find_variable(node.lex)

        if var is None:
            self.errors.append(SemanticError(SemanticError.VARIABLE_NOT_DEFINED % node.lex))
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