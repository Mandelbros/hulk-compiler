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
    return ast, errors, context

class TestHulkBase(unittest.TestCase):
    def test_cannot_use_base_outside_of_a_method(self):
        inp = ('''
        let a = base(a, b, c) in a;
        ''')
        ast, errors, context = run_code(inp, True)
        self.assertEqual(4, len(errors), f"Expects 4 error, but got {len(errors)}")

    # def test_cannot_declare_a_function(self):
    #     inp = ('''
    #     function base(a) => a + 8;
    #     let a = base(6, 7, 8) in a;
    #     ''')
    #     ast, errors, context, scope = run_code(inp, True)
    #     self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_valid_base_call(self):
        inp = '''
            type B {
                f(a, b) => a + b;
           }
           
           type A inherits B {
                f(a, b) => base(a, b) + base(a,b);
           }
           
           let x = 5 in x;
        '''
        ast, errors, context = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_base_call_with_bad_args(self):
        inp = '''
            type B {
                f(a, b) => a + b;
           }

           type A inherits B {
                f(a, b) => base(a) + base(a,b);
           }

           let x = 5 in x;
        '''
        ast, errors, context = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_1(self):
        inp = '''
           type A (x, y) {
                p = y + 9;
                r = x + y;
                getc() => 5;
            }

            type B inherits A {
                p = y;
                getc() => 2;
            }

            type C (x, y, z) inherits B (x + y, y + z) {

            }

            type D inherits C {
                d = x^2;
                getc() => base() + 5;
            }

            let a = new D(2, 3, 4) in print(a.getc());
        '''
        ast, errors, context = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_2(self):
        inp = '''
              type B {
                  f(a, b) => a + b;
             }

             type A inherits B {
                  f(a, b) => base(a, b) + base(a,b);
             }

             let x = new A() in x.f(4,5);
          '''
        ast, errors, context = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")
