from lexer.regex_table  import table
from lexer.lexer import Lexer
from parser.hulk_grammar import G
from parser.parsing_tools import LR1Parser
from common.evaluation import evaluate_reverse_parse

def run_pipeline(file_path): 
    with open(file_path, 'r') as file:
        text = file.read()

    ### TOKENIZATION PHASE
    lexer = Lexer(table, G.EOF)
    tokens = lexer(text)
    

    print('✅ OK')

    ### PARSING PHASE
    parser = LR1Parser(G)

    ttypes = [token.token_type for token in tokens]

    out, oper = parser(ttypes)

    ast = evaluate_reverse_parse(out,oper,tokens)

    print('✅ OK') 
    # print(out)
    # print(oper)

if __name__ == "__main__":
    file_path = 'src/test.hulk' 
    result = run_pipeline(file_path)