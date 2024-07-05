from src.semantics.hulk_ast import ProgramNode, TypeDefNode, ProtoDefNode
import src.common.visitor as visitor
from src.common.semantic import SemanticError, Context, BoolType, NumberType, StringType, ErrorType

class TypeCollector(object):
    def __init__(self, errors = []):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()  # Initialize the context for type and function information

        # Define built-in types
        object_type = self.context.create_type('Object')
        bool_type = self.context.create_type('Boolean')
        bool_type.set_parent(object_type)
        number_type = self.context.create_type('Number')
        number_type.set_parent(object_type)
        string_type = self.context.create_type('String')
        string_type.set_parent(object_type) 

        self.context.types['Boolean'] = BoolType()
        self.context.types['Number'] = NumberType()
        self.context.types['String'] = StringType()

        # Define built-in functions
        self.context.create_function('sin', ['angle'], [number_type], number_type)
        self.context.create_function('cos', ['angle'], [number_type], number_type)
        self.context.create_function('print', ['value'], [object_type], string_type)
        self.context.create_function('sqrt', ['value'], [number_type], number_type)
        self.context.create_function('exp', ['value'], [number_type], number_type)
        self.context.create_function('log', ['value1', 'value2'], [number_type, number_type], number_type)
        self.context.create_function('rand', [], [], number_type)

        # Define built-in protocols
        iterable_protocol = self.context.create_protocol('Iterable')
        iterable_protocol.define_method('next', [], [], bool_type)
        iterable_protocol.define_method('current', [], [], object_type)

        # Visit each type and function definition in the program
        for definition in node.def_list:
            self.visit(definition)

        return self.context, self.errors

    @visitor.when(TypeDefNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)  # Try to create a new type in the context
        except SemanticError as e:
            self.context.types[node.id] = ErrorType()
            self.errors.append(e)  # Append any semantic errors encountered to the errors list

    @visitor.when(ProtoDefNode)
    def visit(self, node):
        try:
            self.context.create_protocol(node.id) # Try to create a new protocol in the context
        except SemanticError as e:
            self.context.protocols[node.id] = ErrorType()
            self.errors.append(e)  # Append any semantic errors encountered to the errors list