from common.utils import Token
from common.evaluation import evaluate_reverse_parse
from common.automata import nfa_to_dfa, automata_minimization
from regex_grammar import G, symbol
from parser.parsing_tools import SLR1Parser

parser = SLR1Parser(G) 

class Regex():
    def __init__(self, exp):
        self.exp = exp
        self.automaton = self.regex_automaton()
        pass
    
    def regex_tokenizer(text, G, skip_whitespaces=True):
        tokens = []

        fixed_tokens = {lex: Token(lex,G[lex]) for lex in '| * ( ) symbol ε + - ? [ ]'.split()}
        
        is_symbol_set = is_escape = False
        for char in text:
            if skip_whitespaces and char.isspace():
                continue
            
            if is_escape:
                token = Token(char, symbol)

                tokens.append(token)
                is_escape = False
                continue

            if char == ']':
                is_symbol_set = False            
            elif is_symbol_set:
                if char != '-':
                    tokens.append(Token(char, symbol))
                    continue
            elif char == '[':
                is_symbol_set = True
            elif char == '\\':
                is_escape = True
                continue

            try:
                token = fixed_tokens[char]
            except KeyError:
                token = Token(char, symbol)
            tokens.append(token)
            
        tokens.append(Token('$', G.EOF))
        return tokens

    def regex_automaton(self):
        re_tokens = self.regex_tokenizer()
        token_types = [t.token_type for t in re_tokens]
        parse, operations = parser(token_types)
        re_ast = evaluate_reverse_parse(parse, operations, re_tokens)
        re_nfa = re_ast.evaluate()
        return automata_minimization(nfa_to_dfa(re_nfa))
        
    