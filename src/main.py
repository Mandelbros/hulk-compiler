import sys
from pathlib import Path
from lexer.lexer import Lexer
from parser.hulk_parser import HulkParser
from common.evaluation import evaluate_reverse_parse
from semantics.semantic_check_pipeline import semantic_check_pipeline
from termcolor import colored

def prompt_error(message):
    print(colored(message, 'red'))

def run_pipeline(input_path, output_file): 
    with open(input_path, 'r') as file:
        text = file.read()

    ### TOKENIZATION PHASE
    lexer = Lexer(rebuild=True, save=True)
    tokens = lexer(text)

    tokens, lexer_errors = lexer(text)

    if lexer_errors:
        for err in lexer_errors:
            prompt_error(err)
        return

    print('✅ LEXER - OK')

    ### PARSING PHASE
    parser = HulkParser(rebuild=True, save=True)
    out, oper, parser_errors = parser(tokens)

    if parser_errors:
        for err in parser_errors:
            prompt_error(err)
        return

    ast = evaluate_reverse_parse(out,oper,tokens)

    print('✅ PARSER - OK') 

    ### SEMANTIC CHECK
    ast, errors, context = semantic_check_pipeline(ast, True)

    if len(errors) == 0:
        print('✅ OK')
    else:
        print("❌ OKn't") 
        print(errors)

    ### CODEGEN

if __name__ == "__main__":  
    input_path = Path(sys.argv[1]) 
    output_file = Path(f'{input_path.stem}.c')
    run_pipeline(input_path, output_file)