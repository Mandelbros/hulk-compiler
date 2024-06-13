from common.utils import Token
from common.state import State
from regex import Regex

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
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
        while text != '':
            final_state, final_lex = self._walk(text)

            if len(final_lex) == 0:
                return #################################### ERROR
            
            bst = -1
            ttype = None
            for st in final_state.state:
                if st.tag != None:
                    if bst == -1:
                        bst = st.tag[1]
                        ttype = st.tag[0]
                    elif st.tag[1] < bst:
                        bst = st.tag[1]
                        ttype = st.tag[0] 
                
            yield final_lex, ttype
            text = text[len(final_lex) : ]
            
        
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]