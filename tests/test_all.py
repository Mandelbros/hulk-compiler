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

class TestHulkAll(unittest.TestCase):

    def test_all_1(self):
        inp = (''' 
                type Person(){
                    name = "John";
                    age = 25;
                    
                    printName(){
                        print(name);
                    }
                }
                
                let x = new Person() in x.printNam();
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(2, len(errors))

    def test___(self):
        inp = (''' 
                type Person(){
                    name = "John";
                    age = 25;

                    printName(){
                        print(self.name);
                    }
                }

                let x = new Person() in x.printName();
        ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test____(self):
        inp = (''' 
                       type Person(){
                            name = "John";
                            age = 25;
                            
                           printName(){
                                print(name);
                            }
                        }
                        
                        let x = new Person() in if (x.name == "Jane") print("Jane") else print("John");
               ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(2, len(errors))

    def test_____(self):
        inp = (''' 
                       type Person(){
                            name = "John";
                            age = 25;

                           printName(){
                                print(self.name);
                            }
                        }

                        let x = new Person() in if ("Jane" == "Hola") print("Jane") else print("John");
               ''')
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_lcm(self):
        inp = '''
            function gcd(a, b) => if (a % b == 0) b else gcd(b, a % b);
            function lcm(a, b) => a * b / gcd(a,b);
            lcm(13,15);
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_lcm_1(self):
        inp = '''
           function gcd(a,b): Number => if (a % b == 0) b else gcd(b, a % b);
           function lcm(a,b) => a * b / gcd(a,b);
           lcm(13,15);
       '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_recursive_gcd(self):
        inp = '''
               function gcd(a,b) => if (a % b == 0) b else gcd(b, a % b);
               gcd(13,15);
               '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_recursive_gcd1(self):
        inp = '''
               function gcd(a,b): Number => if (a % b == 0) b else gcd(b, a % b);
               gcd(13,15);
               '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_(self):
        inp = '''
                 type D {
                    getc() => while(false) 5;      
                }
                                   
                if(let a = new D() in true)
                    print(a.getc())
                else
                    1;
                  '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test__(self):
        inp = '''
                    type D {
                        getc() => while(false) 5;
                        equals() => true;
                    }
                                       
                    let a = new D() in
                        print(a.getc());
                     '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test______(self):
        inp = '''
            type A inherits B {
                x = x;
                y = y;
            }
            type B (x, y) {
                x = x + y;
            }
            5;
        '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(0, len(errors))

    def test_____(self):
        inp = '''
               type A inherits B {
                   x = x;
                   y = y;
               }
               type B (x, y) inherits A {
                   x = x + y;
               }
               5;
           '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test_________(self):
        inp = '''
                type A inherits B {
                    x = x;
                    y = y;
                }
                
                type B inherits C {
                    x = x;
                    y = y;
                }
                
                type C (x, y) {
                    x = x + y | y;
                    y = y;
                }
                
                5;
            '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))

    def test___________(self):
        inp = '''
                type C (x, y) {
                    x = x + y;
                    y = y | y;
                }
                5;
            '''
        ast, errors, context, scope = run_code(inp, True)
        self.assertEqual(1, len(errors))
