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

class TestHulkSimpleInference(unittest.TestCase):
    def test_string_literal(self):
        inp = 'let x = "Hello, World!" in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_number_literal(self):
        inp = 'let x = 42 in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_boolean_literal(self):
        inp = 'let x = true, y = false in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 errors, but got {len(errors)}")

    def test_redef_var(self):
        inp = 'let x = 4, x = x + 5 in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_simple_type_instance(self):
        inp = '''
        type A { }
        
        let x = new A() in x;
        '''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_arithmetic_operation(self):
        inp = 'let x = 42 + 42, y = 4 * 7 in x + y;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_boolean_operation(self):
        inp = 'let a = false, b = 4 > 5, c = 8 == 8 in a | b | c;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_string_operation(self):
        inp = 'let x="Hello", y = "World" in x @@ y;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_invalid_arithmetic(self):
        inp = 'let x = 42 + "Hello, World!" in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_invalid_boolean_operation(self):
        inp = 'let x = 4 | false in x;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_invalid_assigment_operation(self):
        inp = 'let x = 4 in x := false;'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_i(self):
        inp = 'let x = 4, x = x + 1, x = x + 7 in x;'
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")
