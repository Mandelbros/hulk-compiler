from src.semantics.hulk_ast import *
import src.common.visitor as visitor
from src.common.semantic import Context 
from typing import Dict, List
from src.codegen.transpiler_scope import TranspilerScope
import math

class HulkTranspiler(object):
    def __init__(self, type_builder_context: Context):
        self.def_list: List[str] = []
        self.func_list: List[TranspilerScope] = []
        self.type_id_map: Dict[str, int] = {}
        self.type_builder_context: Context = type_builder_context

    def add_definition(self, code: str):
        self.def_list.append(code)

    def add_function(self) -> TranspilerScope:
        new_context = TranspilerScope()
        self.func_list.append(new_context)
        return new_context

    def get_code(self) -> str:
        def_code = '\n\n'.join(d for d in self.def_list)
        func_code = '\n\n'.join(f.get_code() for f in self.func_list)
        return f'#include "src/lib/core.h"\n\n{def_code}\n\n{func_code}'

    def gen_hierarchy_graph(self) -> List[str]:
        adjacency_list:List[List] = []
        context = TranspilerScope()
        context.indent = 1

        for k in self.type_builder_context.types.keys():
            adjacency_list.append([])
            self.type_id_map[k] = len(self.type_id_map)

        for k in self.type_builder_context.protocols.keys():
            adjacency_list.append([])
            self.type_id_map[k] = len(self.type_id_map)

        for type_name, type_ in self.type_builder_context.types.items():
            if type_.parent is not None:
                adjacency_list[self.type_id_map[type_name]].append(self.type_id_map[type_.parent.name])

            for proto_name, proto_ in self.type_builder_context.protocols.items(): 
                if type_.conforms_to(proto_):                                                          
                    adjacency_list[self.type_id_map[type_name]].append(self.type_id_map[proto_name])

        context.new_line(f'hierarchy_graph = malloc(sizeof(int*) * {len(adjacency_list)});')

        for i in range(len(adjacency_list)):
            context.new_line(f'hierarchy_graph[{i}] = malloc(sizeof(int) * {len(adjacency_list[i]) + 1});')
            context.new_line(f'hierarchy_graph[{i}][0] = {len(adjacency_list[i])};')

            for j in range(len(adjacency_list[i])):
                context.new_line(f'hierarchy_graph[{i}][{j+1}] = {adjacency_list[i][j]};')

        return context.c_code


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)                  
    def visit(self, node: ProgramNode):
        graph = self.gen_hierarchy_graph()

        for def_ in node.def_list:
            self.visit(def_) 

        main_context = self.add_function()

        main_context.new_line('int **hierarchy_graph = NULL;\n')
        main_context.new_line('int main()')
        main_context.new_line('{') 
        main_context.new_line('srand(time(NULL));')

        main_context.c_code += graph

        main_context.push_var(main_context.new_var())
        self.visit(node.expr, main_context)

        main_context.new_line('}')

    @visitor.when(FuncDefNode)
    def visit(self, node: FuncDefNode):
        context = self.add_function()

        definition = f'Object *_{node.id}({", ".join(f"Object *{context.define_var(p)}" for p in node.param_ids)});'
        self.add_definition(definition)

        context.new_line(definition[:-1])
        context.new_line('{')

        return_v = context.new_var()
        context.push_var(return_v)
        self.visit(node.body_expr, context)

        context.new_line(f'return {return_v};')
        context.new_line('}')

    @visitor.when(TypeDefNode)
    def visit(self, node: TypeDefNode):
        functions = self.type_builder_context.get_type(
            node.id).all_methods()           

        build_context = self.add_function()
        attr_context = self.add_function()

        definition_c = f'Object *make_{node.id}({", ".join(f"Object *{build_context.define_var(p)}" for p in node.param_ids)});'

        ct = attr_context.new_var()
        definition_a = f'void attr_{node.id}(Object *{ct}{", " if len(node.param_ids)!=0 else ""}{", ".join(f"Object *{attr_context.define_var(p)}" for p in node.param_ids)});'

        self.add_definition(definition_c)
        self.add_definition(definition_a)

        attr_context.new_line(definition_a[:-1])
        attr_context.new_line('{')

        for i in node.attr_list: 
            v = attr_context.new_var()
            attr_context.push_var(v)
            self.visit(i.expr, attr_context)

            attr_context.new_line(f'__add_member({ct}, "p_{i.id}", {v});')

        if node.parent_type != None:         #it has inheritance?
            if node.parent_params:              #the inheritance has args?
                parameters_ih = []

                for p in node.parent_params: 
                    v = attr_context.new_var()
                    attr_context.push_var(v)
                    self.visit(p, attr_context)

                    parameters_ih.append(v)

                attr_context.new_line(f'attr_{node.parent_type}({ct}{"" if len(parameters_ih)==0 else ", "}{", ".join(parameters_ih)});')
            else:
                attr_context.new_line(f'attr_{node.parent_type}({ct});')

        attr_context.new_line('}')


        #builder method
        build_context.new_line(definition_c[:-1])
        build_context.new_line('{')

        ct = build_context.new_var()
        build_context.new_line(f'Object *{ct} = __create_object();')

        for f, t in functions:
            build_context.new_line(f'__add_member({ct}, "f_{f.name}", *type_{t.name}_{f.name});')

        t = self.type_builder_context.get_type(node.id)
        build_context.new_line(f'__add_member({ct}, "type", "{t.name}");')

        q = build_context.new_var()
        build_context.new_line(f'int *{q} =  malloc(sizeof(int));')
        build_context.new_line(f'*{q} =  {self.type_id_map[t.name]};')

        build_context.new_line(f'__add_member({ct}, "type_ind", {q});')

        build_context.new_line(f'attr_{node.id}({ct}{", " if len(node.param_ids)!=0 else ""}{", ".join(build_context.get_var(p) for p in node.param_ids)});')

        build_context.new_line(f'return {ct};')
        build_context.new_line('}')

        for i in node.method_list:
            self.visit(i, node.id)

    @visitor.when(MethodDefNode)
    def visit(self, node: MethodDefNode, type_name: str):
        context = self.add_function()

        self_v = context.define_var('self')

        base_type = self.type_builder_context.get_type(type_name).lowest_ancestor_with_method(node.id).name

        context.define_base(f'type_{base_type}_{node.id}')

        definition = f'Object *type_{type_name}_{node.id}(Object *{self_v}{", " if len(node.param_ids)!=0 else ""}{", ".join(f"Object *{context.define_var(p)}" for p in node.param_ids)});'
        self.add_definition(definition)

        context.new_line(definition[:-1])
        context.new_line('{')

        return_v = context.new_var()
        context.push_var(return_v)
        self.visit(node.body_expr, context)

        context.define_base('')

        context.new_line(f'return {return_v};')
        context.new_line('}')

    @visitor.when(ExprBlockNode)
    def visit(self, node: ExprBlockNode, context: TranspilerScope):
        for expr in node.expr_list[:-1]:
            expr_v = context.new_var()
            context.push_var(expr_v)
            self.visit(expr, context)

        self.visit(node.expr_list[-1], context)

    @visitor.when(LetInNode)            #
    def visit(self, node: LetInNode, context: TranspilerScope):
        for var_def in node.var_defs:
            var_value = context.new_var()
            context.push_var(var_value)
            self.visit(var_def.expr, context)

            context = context.child()                                   ####
            var_name = context.define_var(var_def.id)
            context.new_line(f'Object *{var_name} = {var_value};')

        self.visit(node.body, context)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, context: TranspilerScope):
        return_v = context.pop_var()
        context.new_line(f'Object *{return_v};')

        vc = context.new_var()

        cond_v = context.new_var()
        context.push_var(cond_v)
        self.visit(node.cond, context)

        context.new_line(f'Object *{vc} = {cond_v};')
        context.new_line(f'while(__to_bool({vc}))')
        context.new_line('{')

        body_expr_v = context.new_var()
        context.push_var(body_expr_v)
        self.visit(node.body_expr, context)

        context.new_line(f'{return_v} = {body_expr_v};')

        cond_v = context.new_var()
        context.push_var(cond_v)
        self.visit(node.cond, context)

        context.new_line(f'{vc} = {cond_v};')

        context.new_line('}')

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode, context: TranspilerScope):
        return_v = context.pop_var()
        context.new_line(f'Object *{return_v};')

        for i, (if_cond, if_expr) in enumerate(node.if_stmts):
            cond_v = context.new_var()
            context.push_var(cond_v)
            self.visit(if_cond, context)

            context.new_line(f'if (__to_bool({cond_v}))')
            context.new_line('{')

            body_v = context.new_var()
            context.push_var(body_v)
            self.visit(if_expr, context)

            context.new_line(f'{return_v} = {body_v};')
            context.new_line('}')
            context.new_line('else')
            context.new_line('{')

            if i == len(node.if_stmts)-1:
                body_v = context.new_var()
                context.push_var(body_v)
                self.visit(node.else_expr, context)

                context.new_line(f'{return_v} = {body_v};')

        for _ in node.if_stmts:
            context.new_line('}')

    @visitor.when(DestructiveAssignNode)
    def visit(self, node: DestructiveAssignNode, context: TranspilerScope):
        dvar_v = context.get_var(node.var.lex)

        expr_v = context.new_var()
        context.push_var(expr_v)
        self.visit(node.expr, context)

        context.new_line(f'{dvar_v} = {expr_v};')
        context.new_line(f'Object *{context.pop_var()} = {expr_v};')

    @visitor.when(AttrAssignNode)
    def visit(self, node: AttrAssignNode, context: TranspilerScope):
        expr_v = context.new_var()
        context.push_var(expr_v)
        self.visit(node.expr, context)

        context.new_line(f'__remove_member({context.get_var("self")}, "p_{node.attr}");')
        context.new_line(f'__add_member({context.get_var("self")}, "p_{node.attr}", {expr_v});')
        context.new_line(f'Object *{context.pop_var()} = {expr_v};')
    
    @visitor.when(InstantiationNode)
    def visit(self, node: InstantiationNode, context: TranspilerScope):
        args = []

        for arg in node.args:
            aux = context.new_var()
            context.push_var(aux)
            args.append(aux)
            self.visit(arg, context)

        args_str = ', '.join(args)

        context.new_line(f'Object *{context.pop_var()} = make_{node.id}({args_str});')

    @visitor.when(FuncCallNode)
    def visit(self, node: FuncCallNode, context: TranspilerScope):
        args = []

        for arg in node.args:
            arg_v = context.new_var()
            context.push_var(arg_v)
            args.append(arg_v)

            self.visit(arg, context)

        args_str = ', '.join(args)
        
        func_prefix = '___builtin_' if node.id in ['sin','cos','sqrt','log','rand','print','range','exp'] else '_'

        context.new_line(f'Object *{context.pop_var()} = {func_prefix}{node.id}({args_str});')
        
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, context: TranspilerScope):
        v = context.new_var()
        context.push_var(v)
        self.visit(node.prev_expr, context)

        f = context.new_var()
        context.new_line(f'Object *(*{f})({", ".join("Object *" for _ in range(len(node.args)+1))}) = __find_member({v}, "f_{node.method_id}");')

        args = []

        for arg in node.args:
            arg_v = context.new_var()
            context.push_var(arg_v)
            args.append(arg_v)
            self.visit(arg, context)

        args_str = f'{v}{", "if len(node.args)!=0 else ""}{", ".join(args)}'

        context.new_line(f'Object *{context.pop_var()} = {f}({args_str});')

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, context: TranspilerScope):
        args = []

        for arg_expr in node.args:
            arg_v = context.new_var()
            context.push_var(arg_v)
            args.append(arg_v)

            self.visit(arg_expr, context)

        args_str= ', '.join(args)

        context.new_line(f'Object *{context.pop_var()} = {context.base}({context.get_var("self")}{"" if len(args_str)==0 else ", "}{args_str});')

    @visitor.when(AttrCallNode)
    def visit(self, node: AttrCallNode, context: TranspilerScope):
        context.new_line(f'Object *{context.pop_var()} = __find_member({context.get_var("self")}, "p_{node.attr}");')

    @visitor.when(IsNode)
    def visit(self, node: IsNode, context: TranspilerScope):
        expr_v = context.new_var()
        context.push_var(expr_v)
        self.visit(node.expr, context)

        ind = context.new_var()
        context.new_line(f'int *{ind} = __find_member({expr_v}, "type_ind");')

        t = node.type_
        context.new_line(f'Object *{context.pop_var()} = __make_bool(__search_type(*{ind}, {self.type_id_map[t]}));')

    @visitor.when(AsNode)
    def visit(self, node: AsNode, context: TranspilerScope):
        self.visit(node.expr, context)
    
    @visitor.when(VarNode)
    def visit(self, node: VarNode, context: TranspilerScope):
        v_value = ''
        if node.lex == 'E':
            v_value = f'__make_number({math.e})'
        elif node.lex == 'PI':
            v_value = f'__make_number({math.pi})'
        else:
            v_value = context.get_var(node.lex)

        context.new_line(f'Object *{context.pop_var()} = {v_value};')

       
    @visitor.when(AddNode)              
    def visit(self, node: AddNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __add_number({lvalue}, {rvalue});')
        
    @visitor.when(SubNode)              
    def visit(self, node: SubNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __sub_number({lvalue}, {rvalue});')
    
    @visitor.when(MulNode)             
    def visit(self, node: MulNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __mul_number({lvalue}, {rvalue});')
        
    @visitor.when(DivNode)             
    def visit(self, node: DivNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __div_number({lvalue}, {rvalue});')
        
    @visitor.when(ModNode)              
    def visit(self, node: ModNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __mod_number({lvalue}, {rvalue});')
        
    @visitor.when(PowNode)              
    def visit(self, node: PowNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __pow_number({lvalue}, {rvalue});')
        
    @visitor.when(NegNode)              
    def visit(self, node: NegNode, context: TranspilerScope):
        val = context.new_var()
        context.push_var(val)
        self.visit(node.operand, context)

        context.new_line(f'Object *{context.pop_var()} = __sub_number(__make_number(0), {val});')
 

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __eq({lvalue}, {rvalue});')

    @visitor.when(NotEqualNode)
    def visit(self, node: NotEqualNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __not_bool(__eq({lvalue}, {rvalue}));')

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)
  
        context.new_line(f'Object *{context.pop_var()} = __eq(__comp({lvalue}, {rvalue}), __make_number(-1));')

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)
 
        context.new_line(f'Object *{context.pop_var()} = __eq(__comp({lvalue}, {rvalue}), __make_number(1));')
        
    @visitor.when(LessOrEqualNode)
    def visit(self, node: LessOrEqualNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context) 

        context.new_line(f'Object *{context.pop_var()} = __not_bool(__eq(__comp({lvalue}, {rvalue}), __make_number(1)));')
        
    @visitor.when(GreaterOrEqualNode)
    def visit(self, node: GreaterOrEqualNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)
   
        context.new_line(f'Object *{context.pop_var()} = __not_bool(__eq(__comp({lvalue}, {rvalue}), __make_number(-1)));')

    @visitor.when(OrNode)
    def visit(self, node: OrNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __or_bool({lvalue}, {rvalue});')

    @visitor.when(AndNode)
    def visit(self, node: AndNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)

        context.new_line(f'Object *{context.pop_var()} = __and_bool({lvalue}, {rvalue});')
            
    @visitor.when(NotNode)
    def visit(self, node: NotNode, context: TranspilerScope):
        val = context.new_var()
        context.push_var(val)
        self.visit(node.operand, context)
 
        context.new_line(f'Object *{context.pop_var()} = __not_bool({val});')

    @visitor.when(ConcatNode)           
    def visit(self, node: ConcatNode, context: TranspilerScope):
        lvalue = context.new_var()
        context.push_var(lvalue)
        self.visit(node.lvalue, context)

        rvalue = context.new_var()
        context.push_var(rvalue)
        self.visit(node.rvalue, context)
 
        context.new_line(f'Object *{context.pop_var()} = __concat_string({lvalue}, {rvalue});')
        

    @visitor.when(ConstNumNode)         
    def visit(self, node: ConstNumNode, context: TranspilerScope):        
        context.new_line(f'Object *{context.pop_var()} = __make_number({node.lex});')
        
    @visitor.when(ConstStrNode)         
    def visit(self, node: ConstStrNode, context: TranspilerScope):
        context.new_line(f'Object *{context.pop_var()} = __make_string("{node.lex[1:-1]}");')
        
    @visitor.when(ConstBoolNode)        
    def visit(self, node: ConstBoolNode, context: TranspilerScope):
        context.new_line(f'Object *{context.pop_var()} = __make_bool({1 if node.lex == 'True' else 0});')


def hulk_code_generator(ast: Node, type_builder_context: Context):
    transpiler = HulkTranspiler(type_builder_context)

    transpiler.visit(ast)
    c_code = transpiler.get_code()

    f = open('out.c', 'w')
    f.write(c_code)
    f.close()
