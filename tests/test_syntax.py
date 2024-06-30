import unittest
 
from src.lexer.lexer import HulkLexer
from src.parser.hulk_parser import HulkParser 

lexer = HulkLexer()
parser = HulkParser()

def run_code(inp: str):
    tokens, errors = lexer(inp)
    assert not errors 
     
    return parser(tokens)


class TestHulkSyntax(unittest.TestCase):
    def test_1(self):
        inp = ('''
        42;
        ''')
        derivation, operations, errors = run_code(inp)
        self.assertEqual(0, len(errors), f"Expects 0 error, but got {len(errors)}")


    def test_2(self):
        inp = ('''
        42;
        43;
        ''')
        derivation, operations, errors = run_code(inp)
        self.assertNotEqual(0, len(errors), f"Expects more than 0 errors, but got {len(errors)}")
 