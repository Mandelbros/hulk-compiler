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

    def test_while_loop_in_let_in(self):
        inp = ('''let a = 42 in let mod = a % 3 in
                print(
                    if (mod == 0) "Magic"
                    elif (mod % 3 == 1) "Woke"
                    else "Dumb"
        );''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_while_in_method(self):
        inp = '''
        function gcd(a, b) => 
            while (a > 0) 
                let m = a % b in {
                b := a;
                a := m;
            }; 
        5;
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_while_in_method_(self):
        inp = '''
           function gcd(a, b) => while (a > 0) let m = a % b in 6; 
           gcd(10, 5);'''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_for_loop(self):
        inp = '''
        function gcd(a: Number, b: Number): Number {
            if (a % b == 0) b else gcd(b, a % b);
        }
        gcd(10, 5);
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_for_translation(self):
        inp = '''
        let iterable = range(0, 10) in
            while (iterable.next())
            let x = iterable.current() in print(x);
            '''
        ast, errors, context, scope = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test_(self):
        inp = '''
        type C (cc : Number) {
            x = cc;
        }
    
        type B inherits C {
            f : Number = cc * cc / cc;
            g : String = "qwerty";
                                   
            getsum(s: Number) : String => print(self.f);
        }
    
        type A(q : Number, r : Number) inherits B (q * r + 5) {
            f : Number = q;
            p : Number = r;
                           
            getsum(s: Number) : String => print(self.f);
        }
    
        function operate(x : Number, y : Object) : String {
            print((x + (y as Number)) as Object);
        }
                           
        function lambda(a : A) {
            print(a);
        }
                           
        let a : Number = 6 in let b : Number = a * 7, c : Object = b in lambda(new A(a, b));
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test(self):
        inp = """
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
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test10(self):
        inp = '''
         function IsPrime(n) => 
         let a = false in for(i in range(2,sqrt(n)))
            if(n % i == 0) a := true else a;
        IsPrime(23);
        '''

        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test11(self):
        inp = '''
         print(
            if (5 == 6)
                let a = 3 in print(a + 9)
            elif (6 == 6)
                let a = 2 in print(a)
            else
            print(6)
            );
        '''

        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test1(self):
        inp = '''
        let x = new Person() in x.printNam();
        '''

        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors), f"Expects 1 error, but got {len(errors)}")

    def test12(self):
        inp = '''
                type Person(){
                   name = "John";
                   age = 25;

                  printName(){
                       print(name);
                   }
               }

               let x = new Person() in if (x.name == "Jane") print("Jane") else print("John");
               '''

        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(2, len(errors), f"Expects 2 error, but got {len(errors)}")
 
    def test13(self):
        inp = '''
               function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
               fact(3);
               '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")

    def test14(self):
        inp = '''
               function fact(x) => let f = 1 in for (i in x + 3) f := f * i;
               fact(3);
               '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(2, len(errors), f"Expects 2 error, but got {len(errors)}")