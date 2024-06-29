from parser.hulk_grammar import G as hulk_grammar
from parser.parsing_tools import LR1Parser, ParserError
from common.utils import Token
from common.errors import HulkParserError
from typing import List
import dill

class HulkParser(LR1Parser):
    def __init__(self, rebuild=False, save=False, verbose=False):
        self.verbose = verbose
        if rebuild:
            super().__init__(hulk_grammar)
        else:
            try:
                with open('cache/parser_action_table.pkl', 'rb') as action_pkl:
                    self.action = dill.load(action_pkl)
                with open('cache/parser_goto_table.pkl', 'rb') as goto_pkl:
                    self.goto = dill.load(goto_pkl)
            except:
                super().__init__(hulk_grammar) 

        if save:
            with open('cache/parser_action_table.pkl', 'wb') as action_pkl:
                dill.dump(self.action, action_pkl)
            with open('cache/parser_goto_table.pkl', 'wb') as goto_pkl:
                dill.dump(self.goto, goto_pkl)

    def __call__(self, tokens: List[Token]):
        try:
            ttypes = [token.token_type for token in tokens]
            out, oper = super().__call__(ttypes)
            return out, oper, []
        except ParserError as e:
            error_token = tokens[e.token_ind]
            error_text = HulkParserError.PARSING_ERROR % error_token.lex
            return None, None, [HulkParserError(error_text, error_token.row, error_token.col)]