from common.utils import Token
from common.state import State
from lexer.regex import Regex
import dill

class Lexer:
    def __init__(self, table, eof, rebuild=True):
        self.eof = eof
        self.regexs = None
        self.automaton = None

        if rebuild:
            self.regexs = self._build_regexs(table)
            self.automaton = self._build_automaton()

            with open('cache/lexer_automaton.pkl', 'wb') as automaton_pkl:
                dill.dump(self.automaton, automaton_pkl)
        else:
            try:
                with open('cache/lexer_automaton.pkl', 'rb') as automaton_pkl:
                    self.automaton = dill.load(automaton_pkl)
            except:
                pass  # ERROR, Lexer automaton file not found

    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            re_automaton = State.from_nfa(Regex(regex).automaton)
            for node in re_automaton:
                if node.final:
                    node.tag = (token_type, n)
            regexs.append(re_automaton)

        return regexs

    def _build_automaton(self):
        start = State('start')
        for re_automaton in self.regexs:
            start.add_epsilon_transition(re_automaton)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:
            if not state.has_transition(symbol):
                break
            else:
                state = state[symbol][0]
                lex += symbol
                if state.final:
                    final, final_lex = state, lex

        return final, final_lex

    def _tokenize(self, text):
        row, col = 1, 1 

        while text != '':
            while text and text[0].isspace():
                if text[0] == '\n':
                    row += 1
                    col = 1
                else:
                    col += 1
                text = text[1:]

            if not text:
                break

            final_state, final_lex = self._walk(text)

            if len(final_lex) == 0:
                print("error. aborting")
                return  # ERROR

            bst, ttype = float('inf'), None
            for st in final_state.state:
                if st.tag and st.tag[1] < bst:
                    bst, ttype = st.tag[1], st.tag[0]

            yield final_lex, ttype, row, col

            col += len(final_lex)  
            text = text[len(final_lex):]

        yield '$', self.eof, row, col

    def __call__(self, text):
        return [Token(lex, ttype, row, col) for lex, ttype, row, col in self._tokenize(text)]
