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

class TestHulkConditionals(unittest.TestCase):

    def test_simple_conditional(self):
        inp = ('''
        let a = 42 in let mod = a % 3 in
                print(
                    if (mod == 0) "Magic"
                    elif (mod % 3 == 1) "Woke"
                    else "Dumb"
        );
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_lca(self):
        inp = '''
        let mod = 0, x = 
        if (mod == 0) new Object() 
        elif (mod % 3 == 1) "Woke" 
        else "Dumb"
        in x;
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_lca_(self):
        inp = '''
        let mod = 0, x = 
        if (mod == 0) true
        elif (mod % 3 == 1) 6
        else "Dumb"
        in x;
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_dont_defined_var(self):
        inp = '''
        let x = print(if (mod == 0) "Magic" elif (mod % 3 == 1) "Woke" else "Dumb") in x;
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(2, len(errors), f"Expects 2 error, but got {len(errors)}")

    def test_for_loop(self):
        inp = 'for (x in range(0, 10)) print(x);'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_for_translation(self):
        inp = '''
        let iterable = range(0, 10) in
            while (iterable.next())
            let x = iterable.current() in print(x);'''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test(self):
        type_test = """
        type A(q : Number, r : Number) {
        f : Number = q;
        p : Number = r;

        getsum(s: Number) : Number => self.f + self.p + s;
        }

        function operate(x : Number, y : Object) : String {
            print((x + (y as Number)) as Object);
        }

        let a : Number = 6 in
        let b : Number = a * 7, c : Object = b in
        print(operate(a, b));
        """

        assert run_code(type_test, True)
