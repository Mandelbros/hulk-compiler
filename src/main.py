from lexer.regex_table  import table
from lexer.lexer import Lexer
from parser.hulk_grammar import G
from parser.parsing_tools import LR1Parser
from common.evaluation import evaluate_reverse_parse
from semantics.semantic_check_pipeline import semantic_check_pipeline

def run_pipeline(file_path): 
    with open(file_path, 'r') as file:
        text = file.read()

    ### TOKENIZATION PHASE
    lexer = Lexer(table, G.EOF)
    tokens = lexer(text)
    

    print('✅ OK')

    # return

    ### PARSING PHASE
    parser = LR1Parser(G)

    ttypes = [token.token_type for token in tokens]

    out, oper = parser(ttypes)

    ast = evaluate_reverse_parse(out,oper,tokens)

    print('✅ OK') 
    # print(out)
    # print(oper)

    ast, errors, context = semantic_check_pipeline(ast, True)

    if len(errors) == 0:
        print('✅ OK')
    else:
        print("❌ OKn't") 
        print(errors)

if __name__ == "__main__":
    file_path = 'src/test.hulk' 
    result = run_pipeline(file_path)