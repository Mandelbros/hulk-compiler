import unittest
from src.lexer.lexer import HulkLexer
from src.parser.hulk_parser import HulkParser 
from src.common.evaluation import evaluate_reverse_parse
from src.semantics.semantic_check_pipeline import semantic_check_pipeline
from src.codegen.hulk_transpiler import hulk_code_generator
import subprocess

lexer = HulkLexer()
parser = HulkParser()

def run_code(input: str, debug=False):
    tokens, errors = lexer(input)
    assert not errors 
    
    out, oper, errors = parser(tokens)
    assert not errors

    ast = evaluate_reverse_parse(out, oper, tokens)
    ast, errors, context, scope = semantic_check_pipeline(ast, debug)
    assert not errors
    
    hulk_code_generator(ast, context)
    
    result_compile = subprocess.run(["gcc", "-o", "out", "src/lib/core.c", "out.c", "-lm"], check=True)
    result_run = subprocess.run(["./out"], capture_output=True, text=True, check=True)

    return result_run.stdout

class TestCodeGen(unittest.TestCase):
    def test_codegen_type(self):
        inp = ('''
            type Animal(name, age){
                name = name;
                age = age;

                name() => self.name;
                age() => self.age;
            }

            type Dog(race, name, age) inherits Animal(name, age){
                race = race;

                ladra(name, age){
                    let phrase = "esta ladrando" in {
                        name @@ age @@ phrase;
                    };
                }
            }

            type Cat(race, name, age) inherits Animal(name, age){
                race = race;

                maulla(){
                    let phrase = "esta maullando como un" in {
                        self.name() @@ self.age() @@ phrase @@ self.race;
                    };
                }
            }

            let test_dog = new Dog("sato", "balto", 7), test_cat = new Cat("siames", "Lucas", 4) in {
                print (test_cat.maulla());
                print (test_dog.ladra("alex", 22));
            }
        ''')
        out_text = run_code(inp, False)
        expected_output = 'Lucas 4.000000 esta maullando como un siames\nalex 22.000000 esta ladrando\n'
        self.assertEqual(out_text, expected_output, 'expected: \n'+expected_output+'\nbut got instead:\n'+out_text)

    def test_codegen_override(self):
        inp = ('''
            type Person(name) {
                name = name;

                hello() => print("Hello" @@ self.name @@ "!!!");
            }

            type Student(name: String, age: Number) inherits Person(name) {
                name = name;
                age = age;

                hello() => print("Hi" @@ self.name @@ self.print_age());

                print_age() => ", you have" @@ self.age @@ "years old";
            }

            let s = new Student("Alex", 23) in s.hello();
        ''')
        out_text = run_code(inp, False)
        expected_output = 'Hi Alex , you have 23.000000 years old\n'
        self.assertEqual(out_text, expected_output, 'expected: \n'+expected_output+'\nbut got instead:\n'+out_text)

    def test_codegen_is(self):
        inp = ('''
            type Bird {
            }

            type Plane {
            }

            type Superman {
            }

            let x = new Superman() in
                print(
                    if (x is Bird) "It's bird!"
                    elif (x is Plane) "It's a plane!"
                    else "No, it's Superman!"
                );
        ''')
        out_text = run_code(inp, False)
        expected_output = 'No, it\'s Superman!\n'
        self.assertEqual(out_text, expected_output)

    def test_codegen_protocol(self):
        inp = ('''
             type Animal (name, age){
                name = name;
                age = age;

                name() => self.name;
                age() => self.age;
                move(origin:String, destination:String):String{
                    let from = "se movio desde", to = "hacia" in {
                        from @@ origin @@ to @@ destination;
                    }; 
                }
                lay_down(place:String):String {
                    let at = "se acosto en" in {
                        at @@ place;
                    };
                }
            }

            function test_move (parameter){
                let ans = parameter.move("la sala", "el cuarto") in ans;
            }

            function test_lay_down (parameter){
                let ans = parameter.lay_down("su cama") in ans;
            }

            let test_protocol = new Animal("Jerry", 10) in {
                print(test_protocol.name() @@ test_move(test_protocol));
                print(test_protocol.name() @@ test_lay_down(test_protocol));
            }
        ''')
        out_text = run_code(inp, False)
        expected_output = 'Jerry se movio desde la sala hacia el cuarto\nJerry se acosto en su cama\n'
        self.assertEqual(out_text, expected_output)
 
 
 