from src.semantics.format_visitor import FormatVisitor
from src.semantics.type_collector import TypeCollector
from src.semantics.type_builder import TypeBuilder
from src.semantics.scope_builder import ScopeBuilder
from src.semantics.type_inferer import TypeInferer
from src.semantics.type_checker import TypeChecker

def semantic_check_pipeline(ast, debug = False):
    if debug:
        print('============== VISUALIZING AST ==============')
        formatter = FormatVisitor(add_positions = True)
        tree = formatter.visit(ast)
        print(tree)

    if debug:
        print('============== COLLECTING TYPES ==============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if debug:
        print('Context:')
        print(context)
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        
    if debug:
        print('============== BUILDING TYPES ==============')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if debug:
        print('Context:')
        print(context)
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')

    if debug:
        print('============== BUILDING SCOPES ==============')
    scope_builder = ScopeBuilder(context, errors)
    scope = scope_builder.visit(ast)
    if debug:
        print('Context:')
        print(context)
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')

    if debug:
        print('============== INFERING TYPES ==============')
    type_inferer = TypeInferer(context, errors)
    type_inferer.visit(ast)
    errors.extend(context.inference_errors())
    errors.extend(scope.inference_errors())
    if debug:
        print('Context:')
        print(context)
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')

    if debug:
        print('============== CHECKING TYPES ==============')
    type_checker = TypeChecker(context, errors)
    type_checker.visit(ast)
    if debug:
        print('Context:')
        print(context)
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')

    return ast, errors, context, scope