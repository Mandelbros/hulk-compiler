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

class TestHulkTypeInference(unittest.TestCase):
    def test_type_params_inference(self):
        inp = '''
            type A(x) {
                x = x + 5;
            }
            let x = 9 in new A(x);
        '''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_function_params_inference(self):
        inp = '''
            function a(x, y, z) {
                x | y & z;
            }
            let x = false in x;
            '''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_get_most_specialized(self):
        inp = '''
            function a(x, y, z) {
                x | y;
                y @ z;
            }
            let x = false in x;
            '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_invalid_type_params(self):
        inp = '''
            function a(x, y, z) {
                x | y;
                y + z;
            }
            let x = false in x;
            '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_type_params_inference_with_func_call(self):
        inp = '''
            function sum(x, y) {
                x + y;
            }
            
            type A(x) {
                x = sum(x, x + 5);
            }
            
            let x = 9 in new A(x);
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_(self):
        inp = '''
           type A(q, r) {
            f = q;
            p = r;
                       
            getsum(s: Number) => self.f + self.p + s;
        }

        function operate(x : Number, y : Object) {
            print(x + (y as Number));
        }
                       
        let a : Number = 6, b : Number = a * 7, c : Object = b in print(operate(a, b));
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(4, len(errors), f"Expects 4 error, but got {len(errors)}")
