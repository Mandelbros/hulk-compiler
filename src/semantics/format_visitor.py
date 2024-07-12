from src.semantics.hulk_ast import *
import src.common.visitor as visitor

class FormatVisitor(object):
    def __init__(self, add_positions = True):
        self.add_positions = add_positions

    def add_pos(self, ans, node):
        if self.add_positions and node.pos:
            #return f'{ans} (row = {node.pos[0]}, col = {node.pos[1]})'
            return f'{ans} {node.pos}'
        else:
            return ans

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ProgramNode [<def> ... <def> <expr>;]'
        definitions = '\n'.join(self.visit(definition, tabs + 1) for definition in node.def_list)
        expression = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{definitions}\n{expression}'

    @visitor.when(TypeDefNode)
    def visit(self, node, tabs=0):
        if node.param_types == []:
            params = ''
        else:
            params = '(' + ', '.join([f'{node.param_ids[i]}' + f': {node.param_types[i]}' if node.param_types[i] != [] else '' for i in range(len(node.param_ids))]) + ')'

        if node.parent_type:
            parent = f" inherits {node.parent_type}"
            if node.parent_params:
                parent = parent + '(<expr>, <expr>, ..., <expr>)'
        else:
            parent = ""

        ans = '\t' * tabs + f'\\__ TypeDefNode: type {node.id}{params}{parent} -> <body>'
        parent_params = '\n' + '\n'.join(
            [self.visit(arg, tabs + 1) for arg in node.parent_params]) if node.parent_params else ""
        attributes = '\n'.join([self.visit(attr, tabs + 1) for attr in node.attr_list])
        methods = '\n'.join([self.visit(method, tabs + 1) for method in node.method_list])
        return f'{self.add_pos(ans, node)}{parent_params}\n{attributes}\n{methods}'
    
    @visitor.when(ProtoDefNode)
    def visit(self, node, tabs=0):
        method_signs = '\n'.join(self.visit(definition, tabs + 1) for definition in node.method_list)
        parent_type = f": {node.parent_type}" if node.parent_type else ""
        ans = '\t' * tabs + f'\\__ ProtoDefNode: protocol {node.id}{parent_type} -> <body>'
        return f'{self.add_pos(ans, node)}\n{method_signs}'

    @visitor.when(MethodSignDefNode)
    def visit(self, node, tabs=0):
        params = ', '.join([f'{node.param_ids[i]}' + f': {node.param_types[i]}' for i in range(len(node.param_ids))])
        ans = '\t' * tabs + f'\\__ MethodSignDefNode: {node.id}({params}):{node.ret_type}'
        return f'{self.add_pos(ans, node)}'

    @visitor.when(AttrDefNode)
    def visit(self, node, tabs=0):
        type_ = f": {node.type_}" if node.type_ is not None else ""
        ans = '\t' * tabs + f'\\__ AttrDefNode: {node.id}{type_} = <expr>'
        body = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{body}'
    
    @visitor.when(MethodDefNode)
    def visit(self, node, tabs=0):
        params = ', '.join(
            [f'{node.param_ids[i]}' + f': {node.param_types[i]}' if node.param_types[i] is not None else '' for i in
             range(len(node.param_ids))])
        ans = '\t' * tabs + f'\\__ MethodDefNode: {node.id}({params}) -> <expr>'
        body = self.visit(node.body_expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{body}'

    @visitor.when(FuncDefNode)
    def visit(self, node, tabs=0):
        params = ', '.join(
            [f'{node.param_ids[i]}' + f': {node.param_types[i]}' if node.param_types[i] is not None else '' for i in
             range(len(node.param_ids))])
        ans = '\t' * tabs + f'\\__ FuncDefNode: def {node.id}({params}) -> <expr>'
        body = self.visit(node.body_expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{body}'
    
    @visitor.when(ExprBlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ExprBlockNode [<expr>; ... <expr>;]'
        expr_list = '\n'.join(self.visit(expr, tabs + 1) for expr in node.expr_list)
        return f'{self.add_pos(ans, node)}\n{expr_list}'
    
    @visitor.when(LetInNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ LetInNode: let [<var>, ..., <var>] in <expr>'
        vars = '\n'.join(self.visit(var, tabs + 1) for var in node.var_defs)
        expr = self.visit(node.body, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{vars}\n{expr}'

    @visitor.when(VarDefNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ VarDefNode: {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{expr}'

    @visitor.when(DestructiveAssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ DestructiveAssignNode: <var> := <expr>'
        var = self.visit(node.var, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{var}\n{expr}'
    
    @visitor.when(AttrAssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ AttrAssignNode: <id>.<attr> := <expr>'
        id = self.visit(node.id, tabs + 1)
        attr = self.visit(node.attr, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{id}\n{attr}\n{expr}'
    
    @visitor.when(IfElseNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ IfElseNode:'

        conditions = [self.visit(if_stmt[0], tabs + 1) for if_stmt in node.if_stmts]
        expressions = [self.visit(if_stmt[1], tabs + 1) for if_stmt in node.if_stmts]

        if_cond, if_expr = conditions[0], expressions[0]
        if_clause = '\t' * tabs + f'if(<cond>) <expr>\n{if_cond}\n{if_expr}'

        elif_clauses = []
        for i in range(1, len(conditions)):
            elif_clauses.append('\t' * tabs + f'elif(<cond>) <expr>\n{conditions[i]}\n{expressions[i]}')

        elif_clauses = '\n'.join(elif_clauses) if elif_clauses else ''
        if len(elif_clauses) > 0:
            elif_clauses = '\n' + elif_clauses

        else_clause = '\t' * tabs + f'else <expr>\n{self.visit(node.else_expr, tabs + 1)}'

        return f'{self.add_pos(ans, node)}\n{if_clause}{elif_clauses}\n{else_clause}'

    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ WhileNode: while(<cond>) <expr>'
        cond = self.visit(node.cond, tabs + 1)
        body_expr = self.visit(node.body_expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{cond}\n{body_expr}'

    @visitor.when(ForNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ ForNode: for({node.var} in <iter>) <expr>'
        iter = self.visit(node.iter, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{iter}\n{expr}'
    
    @visitor.when(InstantiationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ InstantiationNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{self.add_pos(ans, node)}\n{args}'

    @visitor.when(IsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ IsNode: <expr> is {node.type_}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{expr}'

    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ AsNode: <expr> as {node.type_}'
        expr = self.visit(node.expr, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{expr}'
    
    @visitor.when(AttrCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ AttrCallNode: <expr>.{node.attr}'
        obj = self.visit(node.obj, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{obj}'

    @visitor.when(MethodCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ MethodCallNode: <expr>.{node.method_id}(<expr>, ..., <expr>)'
        obj = self.visit(node.prev_expr, tabs + 1)
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{self.add_pos(ans, node)}\n{obj}\n{args}'
    
    @visitor.when(FuncCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ FuncCallNode: {node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{self.add_pos(ans, node)}\n{args}'

    @visitor.when(BaseCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ BaseCallNode: base(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{self.add_pos(ans, node)}\n{args}'
    
    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ <expr> {node.__class__.__name__} <expr>'
        lvalue = self.visit(node.lvalue, tabs + 1)
        rvalue = self.visit(node.rvalue, tabs + 1)
        return f'{self.add_pos(ans, node)}\n{lvalue}\n{rvalue}'

    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        return self.add_pos('\t' * tabs + f'\\__ {node.__class__.__name__}: {node.operand}', node)

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return self.add_pos('\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}', node)