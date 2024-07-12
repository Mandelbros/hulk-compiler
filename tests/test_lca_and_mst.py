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

class TestHulkLoops(unittest.TestCase):
    # todo
    # def test_(self):
    #     inp = ('''
    #             function x() => if (true) 1 else 2;
    #             function x() => if (true) new A() elif(true) new B() else new C();
    #             type A {}
    #             type B inherits A {}
    #             type C inherits B {}
    #             5;
    #             ''')
    #     ast, errors, context, scope = run_code(inp, True)
    #     self.assertEqual(1, len(errors))

    def test_lca_types(self):
        inp = ('''
                function x() => if (true) 1 else 2;
                function y() => if (true) new A() elif(true) new B() else new C();
                type A {}
                type B inherits A {}
                type C inherits B {}
                5;
                ''')
        # return type of x must be A
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_lca_protocols(self):
        inp = ('''
                    function x(x: A, y: B, z: C) => if (true) x elif(true) y else z;
                    protocol A {
                        f (): Number;
                    }
                    protocol B extends A {
                        g (): Number;
                    }
                    protocol C {
                        f (): Number;
                        g (): Number;
                    }
                    5;
                ''')
        # return type of x must be A
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_lca_object(self):
        inp = ('''
                    function x(x: A, y: B, z: C) => if (true) x elif(true) y else z;
                    protocol A {
                        f (): Number;
                    }
                    protocol B extends A {
                        g (): Number;
                    }
                    protocol C {
                        h (): Number;
                        g (): Number;
                    }
                    5;
                ''')
        # return type of x must be Object
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    """
    def test_lca_types_and_protocols(self):
        inp = ('''
                    function x(x: Iterable, y: Range, z: Number[]) => if (true) x elif(true) y else z;
                    5;
                ''')
        # return type of x must be Iterable
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))
    def test_lca_error(self):
        inp = ('''
            function x(x: Iterable, y: Range, z: Number[]) => if (true) x + y elif(true) y else z;
            let x = [9], y = range(1, 10) in x({x}, {y}, {x}).length;
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_lca_auto(self):
        inp = ('''
                function x(x, y: Range, z: Number[]) => if (true) x elif(true) y else z;
                let x = [9], y = range(1, 10) in x(x, y, x).length;
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_most_spec_types(self):
        inp = ('''
                function f(x) => if (true) x[9] + 7 else x[2];
                5;
        ''')
        # x must be Number[]
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_most_spec_types_error(self):
        inp = ('''
                function f(x) => if (true) x[9] + 7 else x + 8;
                5;
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_most_spec_types_1(self):
        inp = ('''
                function f(x) => if (true) x[9] + 7 else x[2] @ 42;
                5;
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))
    """

    def test_lca_protocols_1(self):
        inp = ('''
                function f(x: Iterable, y: A) => if (true) x else y;
                protocol A {
                    next(): Boolean;
                    current(): Boolean;
                }
                5;
        ''')
        # f return type must be Iterable
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    """
    def test_most_spec_types_protocols(self):
        inp = ('''
            function f(x) => g(x, x);
            function g(x: Iterable, y) => if (true) x else y[9] + 4;
            5;
        ''')
        # x must be Number[]
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))
    """