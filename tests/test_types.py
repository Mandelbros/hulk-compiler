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

    def test_circular_inheritance(self):
        inp = ('''
                type A inherits B {
                    x = x + 5;
                }
                type B(x) inherits A(x^2) {
                    x = x + 5;
                }
                let x = 9 in new A(x);
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_inherits_params(self):
        inp = ('''
                type A inherits B {
                    x = x + 5;
                }
                type B(x) {
                    x = x + 5;
                }
                let x = 9 in new A(x);
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_hierarchy(self):
        inp = ('''
        type A(x) {
            x = x + 5;
        }
        type B(x) inherits A(x^2) {
            x = x + 5;
        }
        let x = 9 in new B(x);
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_pol_hierarchy(self):
        inp = ('''
        type A(x) {
            x = x + 5;
            sum(y) => self.x + y; 
        }
        type B(x) inherits A(x^2) {
            x = x + 5;
            sum(y) => self.x + y; 
        }
        let x = 9 in new B(x);
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_pol_hierarchy_2(self):
        inp = ('''
        type A(x) {
            x = x + 5;
            sum(y) => self.x + y; 
        }
        type B(x) inherits A(x^2) {
            x = x + 5;
            sum(y: Object) => 5; 
        }
        let x = 9 in new B(x);
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    """
    def test_for_loop(self):
        inp = 'for (x in range(0, 10)) print(x);'
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_for_translation(self):
        inp = '''
        let iterable = range(0, 10) in
            while (iterable.next())
            let x = iterable.current() in print(x);'''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_call_to_not_defined_function(self):
        inp = '''
        let iterable = t().next() in
            let x = iterable.current() in print(x);'''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_not_defined_ver(self):
        inp = '''
        let iterable = t.next() in
            let x = iterable.current() in print(x);'''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")
    """
    
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

    def test____(self):
        inp = ('''
                type A {
                    f() => 5;
                }
                type B inherits A {
                    f() => "hola";
                }
                let x = 9 in new A();
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_____(self):
        inp = ('''
                type A {
                    f(a: String) => 5;
                }
                type B inherits A {
                    f(b: Number) => "hola";
                }
                let x = 9 in new A();
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test_________(self):
        inp = ('''
                type A {
                    f(): String => 5;
                }
                let x = 9 in new A();
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test______(self):
        inp = ('''
                type A {
                    f(): Object => 5;
                }
                let x = new A() in x.f(2, 3);
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_______(self):
        inp = ('''
                type A(x) {
                    f(): Object => 5;
                }
                
                type A(x, y) {
                    f(): Object => 5;
                }
                
                let x = new A(), y = new A(2, 3) in x.f(2, 3);
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    """
    def test________(self):
        inp = ('''
                protocol A {
                    f(): Object;
                }

                protocol B extends A {
                    f(x: Number): Object;
                }

                5;
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test___(self):
        inp = ('''
                protocol A {
                    f(): Object;
                }

                protocol B extends A {
                    f(): Object;
                }

                5;
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))
    """

    def test__________(self):
        inp = ('''
                   type A(x) {
                       x = x + 5;
                   }
                   
                   function f(x) => new A(x);

                   5;
                   ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_inference(self):
        inp = ('''
                function f(x) => x;
                {
                    f(5);
                    let x: Object = 5 in f(x);
                }
                ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_inference__(self):
        inp = ('''
                   type Person(firstname, lastname) {
                        firstname = firstname;
                        lastname = lastname;
                    
                        name() => self.firstname @@ self.lastname;
                        hash() : Number {
                            5;
                        }
                    }
                    new Person("Juan", "Perez");
                   ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))
