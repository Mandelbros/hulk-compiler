from src.semantics.hulk_ast import ProgramNode, TypeDefNode, FuncDefNode, MethodDefNode, AttrDefNode
from src.common.semantic import SemanticError, ErrorType, AutoType
import src.common.visitor as visitor

class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None  # Keep track of the current type being defined
        self.errors = errors

    def get_param_ids_and_types(self, node):
        if node.param_ids is None or node.param_types is None:
            return None, None

        param_ids = []
        param_types = []

        # For every parameter
        for i in range(len(node.param_ids)):
            param_id = node.param_ids[i]
            param_type = node.param_types[i]

            if param_id in param_ids:
                # Duplicate parameter identifier
                self.errors.append(SemanticError(f'Parameter {param_id} is already declared'))
                index = param_ids.index(param_id)
                param_types[index] = ErrorType()
            else:
                # Resolve parameter type
                if param_type is None:
                    param_type = AutoType()
                else:
                    try:
                        param_type = self.context.get_type(param_type)
                    except SemanticError as e:
                        self.errors.append(e)
                        param_type = ErrorType()
                param_types.append(param_type)
                param_ids.append(param_id)

        return param_ids, param_types

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for definition in node.def_list:
            self.visit(definition)

    @visitor.when(TypeDefNode)
    def visit(self, node):
        # Set the current type being processed
        self.current_type = self.context.get_type(node.id)

        # Handle parent type
        if node.parent_type == []:
            node.parent_type = None
        self.current_type.param_ids, self.current_type.param_types = self.get_param_ids_and_types(node)

        # Check for forbidden inheritance
        if node.parent_type in ['Number', 'Boolean', 'String']:
            self.errors.append(SemanticError(f'Type {node.id} is inheriting from forbidden type {node.parent}'))
        elif node.parent_type is not None:
            # Handle circular dependency and resolve parent type
            try:
                parent = self.context.get_type(node.parent_type)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(SemanticError(f'Circular dependency inheritance {self.current_type.name} : {node.parent} : ... : {current.name}'))
                        parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as e:
                self.errors.append(e)
                parent = ErrorType()

            try:
                self.current_type.set_parent(parent)
            except SemanticError as e:
                self.errors.append(e)
        else:
            # Default inheritance from Object type
            object_type = self.context.get_type('Object')
            self.current_type.set_parent(object_type)

        # Process attributes and methods
        for attr in node.attr_list:
            self.visit(attr)
        for method in node.method_list:
            self.visit(method)

    @visitor.when(FuncDefNode)
    def visit(self, node):
        param_ids, param_types = self.get_param_ids_and_types(node)

        # Resolve the return type
        if node.ret_type is None:
            return_type = AutoType()
        else:
            try:
                return_type = self.context.get_type(node.ret_type)
            except SemanticError as e:
                self.errors.append(e)
                return_type = ErrorType()

        # Create the new function
        try:
            self.context.create_function(node.id, param_ids, param_types, return_type)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(AttrDefNode)
    def visit(self, node):
        # Resolve the type
        if node.type_ is None:
            attribute_type = AutoType()
        else:
            try:
                attribute_type = self.context.get_type(node.type_)
            except SemanticError as e:
                self.errors.append(e)
                attribute_type = ErrorType()
        # Add the new attribute to the current type
        try:
            self.current_type.define_attribute(node.id, attribute_type)
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(MethodDefNode)
    def visit(self, node):
        param_ids, param_types = self.get_param_ids_and_types(node)

        # Resolve return type
        if node.ret_type is None:
            return_type = AutoType()
        else:
            try:
                return_type = self.context.get_type(node.ret_type)
            except SemanticError as e:
                self.errors.append(e)
                return_type = ErrorType()

        # Add the new method to the current type
        try:
            self.current_type.define_method(node.id, param_ids, param_types, return_type)
        except SemanticError as e:
            self.errors.append(e)
