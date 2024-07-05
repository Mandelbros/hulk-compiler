import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    WRONG_SIGNATURE = 'Method \'%s\' already defined in an ancestor with a different signature.'
    SELF_IS_READONLY = 'Variable "self" is read-only.'
    INCOMPATIBLE_TYPES = 'Cannot convert \'%s\' into \'%s\'.'
    VARIABLE_NOT_DEFINED = 'Variable \'%s\' is not defined.'
    INVALID_OPERATION = 'Operation \'%s\' is not defined between \'%s\' and \'%s\'.'
    INVALID_UNARY_OPERATION = 'Operation \'%s\' is not defined for \'%s\'.'
    INCONSISTENT_USE = 'Inconsistent use of \'%s\', with infered types of \'%s\' and \'%s\'.'
    DIF_EXPECTED_ARGUMENTS = 'Expected %s arguments, but got %s in \'%s\'.'
    BASE_OUTSIDE_METHOD = 'Cannot use "base" outside of a method.'
    ATTR_ACCESS_FROM_NON_SELF = 'Cannot access an attribute from a non-self object'
    PARENT_TYPE_SET = 'Parent type is already set for \'%s\'.'
    FUNCTION_NOT_DEFINED = 'Function \'%s\' is not defined.'
    PROTOCOL_NOT_DEFINED = 'Protocol \'%s\' is not defined.'
    TYPE_NOT_DEFINED = 'Type \'%s\' is not defined.'
    ATTR_NOT_DEFINED = 'Attribute \'%s\' is not defined in \'%s\'.'
    METHOD_NOT_DEFINED = 'Method \'%s\' is not defined in \'%s\'.'
    PROTOCOL_ALREADY_DEFINED = 'Protocol with the same name (\'%s\') already in context.'
    TYPE_ALREADY_DEFINED = 'Type with the same name (\'%s\') already in context.'
    FUNCTION_ALREADY_DEFINED = 'Function with the same name (\'%s\') already in context.'
    ATTR_ALREADY_DEFINED = 'Attribute \'%s\' is already defined in \'%s\'.'
    METHOD_ALREADY_DEFINED = 'Method \'%s\' is already defined in \'%s\'.'
    PARAM_ALREADY_DEFINED = 'Parameter \'%s\' is already declared'
    CANNOT_INFER_PARAM_TYPE = 'Cannot infer type of parameter \'%s\' in \'%s\'. Please specify it.'
    CANNOT_INFER_ATTR_TYPE = 'Cannot infer type of attribute \'%s\'. Please specify it.'
    CANNOT_INFER_RETURN_TYPE = 'Cannot infer return type of \'%s\'. Please specify it.'
    CANNOT_INFER_VAR_TYPE = 'Cannot infer type of variable \'%s\'. Please specify it.'
    FORBIDDEN_INHERITANCE = 'Type \'%s\' is inheriting from forbidden type \'%s\''
    CIRCULAR_DEPENDENCY_INHERITANCE = 'Circular dependency inheritance \'%s\' : \'%s\' : ... : \'%s\''

    def __init__(self, name, pos = None):
        self.name = name
        self.pos = pos  # (row, column)

    def __str__(self):
        if self.pos:
            #return f'{self.name} {self.pos}'
            return f'{self.name} (After column {self.pos[1]} of line {self.pos[0]})'
        return f'{self.name}'

    def __repr__(self):
        return str(self)

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def inference_errors(self):
        errors = []

        if isinstance(self.type, AutoType):
            errors.append(SemanticError(SemanticError.CANNOT_INFER_ATTR_TYPE % self.name))
            self.type = ErrorType()

        return errors

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_ids, param_types, return_type):
        self.name = name
        self.param_ids = param_ids
        self.param_types = param_types
        self.param_vars = []
        self.return_type = return_type

    def matches_signature(self, other):
        # Check same names, covariance of return types and same amount of params
        if self.name != other.name or not self.return_type.conforms_to(other.return_type) or len(self.param_types) != len(other.param_types):
            return False
        for i in range(len(self.param_types)):
            # Check contravariance of param types
            if not other.param_types[i].conforms_to(self.param_types[i]):
                return False
        return True

    def inference_errors(self):
        errors = []

        for i in range(len(self.param_types)):
            param_type = self.param_types[i]
            if isinstance(param_type, AutoType) and not isinstance(param_type, ErrorType):
                param_id = self.param_ids[i]
                errors.append(SemanticError(SemanticError.CANNOT_INFER_PARAM_TYPE % (param_id, self.name)))
                self.param_types[i] = ErrorType()

        if isinstance(self.return_type, AutoType):
            errors.append(SemanticError(SemanticError.CANNOT_INFER_RETURN_TYPE % self.name))
            self.return_type = ErrorType()
        return errors

    def __str__(self):
        params = ', '.join(f'{n} : {t.name}' for n,t in zip(self.param_ids, self.param_types))
        return f'[method] {self.name}({params}) : {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Protocol:
    def __init__(self, name):
        self.name = name
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(SemanticError.PARENT_TYPE_SET % (self.name))
        self.parent = parent

    def get_method(self, name):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(SemanticError.METHOD_NOT_DEFINED % (name, self.name))
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(SemanticError.METHOD_NOT_DEFINED % (name, self.name))

    def define_method(self, name, param_ids, param_types, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(SemanticError.METHOD_ALREADY_DEFINED % (name, self.name))

        method = Method(name, param_ids, param_types, return_type)
        self.methods.append(method)
        return method

    def conforms_to(self, other):
        if other == ObjectType():
            return True
        if isinstance(other, Type):
            return False
        if self == other or (self.parent is not None and self.parent.conforms_to(
            other)):
            return True
        if isinstance(other, Protocol):
            for method_sign in other.methods:
                try:
                    method = self.get_method(method_sign.name)
                except SemanticError:
                    return False
                if not method.matches_signature(method_sign):
                    return False
            return True
        return False

    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else f' extends {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.methods else ''
        output += '\n\t'.join(str(method_sign) for method_sign in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class Type:
    def __init__(self, name:str):
        self.name = name
        self.param_ids = []
        self.param_types = []
        self.param_vars = []
        self.attributes = []
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(SemanticError.PARENT_TYPE_SET % (self.name))
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            raise SemanticError(SemanticError.ATTR_NOT_DEFINED % (name, self.name))

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(SemanticError.ATTR_ALREADY_DEFINED % (name, self.name))

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(SemanticError.METHOD_NOT_DEFINED % (name, self.name))
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(SemanticError.METHOD_NOT_DEFINED % (name, self.name))

    def define_method(self, name:str, param_ids:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(SemanticError.METHOD_ALREADY_DEFINED % (name, self.name))

        method = Method(name, param_ids, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain
    
    def get_params(self):
        if (self.param_ids == [] or self.param_types == []) and self.parent is not None:
            param_ids, param_types = self.parent.get_params()
        else:
            param_ids = self.param_ids
            param_types = self.param_types
        return param_ids, param_types

    def conforms_to(self, other):
        if isinstance(other, Type):
            return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)
        if isinstance(other, Protocol):
            for method_sign in other.methods:
                try:
                    method = self.get_method(method_sign.name)
                except SemanticError:
                    return False
                if not method.matches_signature(method_sign):
                    return False
            return True
        return False

    def inference_errors(self):
        if isinstance(self, ErrorType):
            return []
        
        errors = []

        for attr in self.attributes:
            errors.extend(attr.inference_errors())

        for method in self.methods:
            errors.extend(method.inference_errors())

        for i in range(len(self.param_types)):
            param_type = self.param_types[i]
            if isinstance(param_type, AutoType):
                param_id = self.param_ids[i]
                errors.append(SemanticError(SemanticError.CANNOT_INFER_PARAM_TYPE % (param_id, self.name)))
                self.param_types[i] = ErrorType()
        return errors
    
    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}('
        params = '' if not self.param_ids else ', '.join(
            [f"{param_id} : {param_type.name}" for param_id, param_type in zip(self.param_ids, self.param_types)])
        output += params + ')'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class AutoType(Type):
    def __init__(self):
        Type.__init__(self, '<auto>')

    def __eq__(self, other):
        return isinstance(other, AutoType) or other.name == self.name
    
class SelfType(Type):
    def __init__(self, referred_type = None):
        super().__init__('self')
        self.referred_type = referred_type

    def get_attribute(self, name):
        if self.referred_type:
            return self.referred_type.get_attribute(name)

        return super().get_attribute(name)

    def __eq__(self, other):
        return isinstance(other, SelfType) or other.name == self.name
    
class ObjectType(Type):
    def __init__(self) -> None:
        super().__init__('Object')

    def __eq__(self, other):
        return isinstance(other, ObjectType) or other.name == self.name

class BoolType(Type):
    def __init__(self):
        super().__init__('Boolean')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, BoolType) or other.name == self.name

class NumberType(Type):
    def __init__(self) -> None:
        super().__init__('Number')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, NumberType) or other.name == self.name
    
class StringType(Type):
    def __init__(self):
        super().__init__('String')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, StringType) or other.name == self.name

class Function:
    def __init__(self, name, param_ids, param_types, return_type):
        self.name = name
        self.param_ids = param_ids
        self.param_types = param_types
        self.param_vars = []
        self.return_type = return_type

    def inference_errors(self):
        errors = []

        for i in range(len(self.param_types)):
            param_type = self.param_types[i]
            if isinstance(param_type, AutoType):
                param_id = self.param_ids[i]
                errors.append(SemanticError(SemanticError.CANNOT_INFER_PARAM_TYPE % (param_id, self.name)))
                self.param_types[i] = ErrorType()

        if isinstance(self.return_type, AutoType):
            errors.append(SemanticError(SemanticError.CANNOT_INFER_RETURN_TYPE % self.name))
            self.return_type = ErrorType()
        return errors

    def __str__(self):
        params = ', '.join(f'{n} : {t.name}' for n, t in zip(self.param_ids, self.param_types))
        return '\n' + f'function {self.name}({params}) : {self.return_type.name};' + '\n'

    def __eq__(self, other):
        return other.name == self.name and other.return_type == self.return_type and other.param_types == self.param_types

class Context:
    def __init__(self):
        self.protocols = {}
        self.types = {}
        self.functions = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(SemanticError.TYPE_ALREADY_DEFINED % (name))
        if name in self.protocols:
            raise SemanticError(SemanticError.PROTOCOL_ALREADY_DEFINED % (name))
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str, params_len = None):
        try:
            type_ = self.types[name]
            if isinstance(type_, ErrorType) and params_len:
                type_ = ErrorType()
                type_.param_ids = ['<error>'] * params_len
                type_.param_types = [ErrorType()] * params_len
            return type_
        except KeyError:
            raise SemanticError(SemanticError.TYPE_NOT_DEFINED % (name))
        
    def create_function(self, name: str, param_ids: list, param_types: list, return_type):
        if name in self.functions:
            raise SemanticError(SemanticError.FUNCTION_ALREADY_DEFINED % (name))
        function = self.functions[name] = Function(name, param_ids, param_types, return_type)
        return function

    def get_function(self, name: str):
        try:
            return self.functions[name]
        except KeyError:
            raise SemanticError(SemanticError.FUNCTION_NOT_DEFINED % (name))
        
    def create_protocol(self, name):
        if name in self.types:
            raise SemanticError(SemanticError.TYPE_ALREADY_DEFINED % (name))
        if name in self.protocols:
            raise SemanticError(SemanticError.PROTOCOL_ALREADY_DEFINED % (name))
        protocol = self.protocols[name] = Protocol(name)
        return protocol
    
    def get_protocol(self, name):
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(SemanticError.PROTOCOL_NOT_DEFINED % (name))
        
    def get_type_or_protocol(self, name):
        try:
            return self.get_type(name)
        except SemanticError:
            return self.get_protocol(name)
        
    def inference_errors(self):
        errors = []

        for type_name in self.types:
            errors.extend(self.types[type_name].inference_errors())

        for func_name in self.functions:
            errors.extend(self.functions[func_name].inference_errors())

        return errors

    def __str__(self):
        return ('{\n\t' + '\n\t'.join(y for x in self.protocols.values() for y in str(x).split('\n')) +
                '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) +
                '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) + '\n}')

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype, is_param = False):
        self.name = name
        self.type = vtype
        self.infered_types = []
        self.is_param = is_param

    def inference_errors(self):
        if self.type == AutoType() and self.is_param:
            self.type = ErrorType()
            return []

        errors = []
        if isinstance(self.type, AutoType):
            self.type = ErrorType()
            errors.append(SemanticError(SemanticError.CANNOT_INFER_VAR_TYPE % self.name))

        return errors

    def __str__(self):
        return f'{self.name} : {self.type.name} infered:{[infered.name for infered in self.infered_types]}'

    def __repr__(self):
        return str(self)

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype, is_param = False):
        info = VariableInfo(vname, vtype, is_param)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index = None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None
        
    def get_variables(self, all = False):
        vars = [x for x in self.locals]

        if all and self.parent is not None:
            vars.extend(self.parent.get_variables(True))

        return vars

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
    
    def inference_errors(self):
        errors = []

        for var in self.locals:
            errors.extend(var.inference_errors())

        for child_scope in self.children:
            errors.extend(child_scope.inference_errors())

        return errors

def get_most_specialized_type(types, var_name):
    if not types:
        return ErrorType()
    for type_ in types:
        if isinstance(type, ErrorType):
            return ErrorType()
    for type_ in types:
        if isinstance(type, AutoType):
            return AutoType()
    most_specialized = types[0]
    for type_ in types:
        if type_.conforms_to(most_specialized):
            most_specialized = type_
        elif not most_specialized.conforms_to(type_):
            raise SemanticError(SemanticError.INCONSISTENT_USE % (var_name, most_specialized.name, type_.name))
    return most_specialized

def get_lowest_common_ancestor(type1, type2):
    if type1 is None or type2 is None:
        return ObjectType()
    if type1.conforms_to(type2):
        return type2
    if type2.conforms_to(type1):
        return type1
    return get_lowest_common_ancestor(type1.parent, type2.parent)

def get_list_lowest_common_ancestor(types):
    if not types:
        return ErrorType()
    for type_ in types:
        if isinstance(type_, ErrorType):
            return ErrorType()
    for type_ in types:
        if isinstance(type_, AutoType):
            return AutoType()
    lca = types[0]
    for typex in types:
        lca = get_lowest_common_ancestor(lca, typex)
    return lca