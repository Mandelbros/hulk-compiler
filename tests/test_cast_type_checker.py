import unittest
from src.lexer.lexer import HulkLexer
from src.parser.hulk_parser import HulkParser 
from src.common.evaluation import evaluate_reverse_parse
from src.semantics.semantic_check_pipeline import semantic_check_pipeline

lexer = HulkLexer()
parser = HulkParser()

def run_code(input: str, debug=False):
    tokens, errors = lexer(input)
    assert not errors 
    
    out, oper, errors = parser(tokens)
    assert not errors

    ast = evaluate_reverse_parse(out, oper, tokens)
    ast, errors, context, scope = semantic_check_pipeline(ast, debug)
    return ast, errors, context, scope

class TestHulkCastTypeInference(unittest.TestCase):
    def test_num_object_dynamic_type_checking(self):
        inp = 'let a = 4 + 5 is Object in a;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_num_str_dynamic_type_checking(self):
        inp = 'let a = 92 is String in a;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_object_num_dynamic_type_checking(self):
        inp = 'let a = new Object(), b = a is Number in b;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_string_bool_downcast(self):
        inp = '''
        type A {}
        let a = "Hola" as A in a;
        '''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")
