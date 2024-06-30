from src.semantics.type_collector import TypeCollector
from src.semantics.type_builder import TypeBuilder

def semantic_check_pipeline(ast, debug=False):
    if debug:
        print('============== COLLECTING TYPES ==============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        
    if debug:
        print('============== BUILDING TYPES ==============')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)

    # in progress...
    return ast, errors, context