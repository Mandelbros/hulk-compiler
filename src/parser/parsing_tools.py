from common.pycompiler import Item
from common.state import State, multiline_formatter
from common.utils import compute_firsts, compute_local_first
from common.utils import ContainerSet
import dill

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False, rebuild=True, save=False):
        self.G = G
        self.verbose = verbose
        self.action = None
        self.goto = None

        if rebuild:
            self.action = {}
            self.goto = {}
            self._build_parsing_table()
            
            if save:
                with open('cache/parser_action_table.pkl', 'wb') as table_pkl:
                    dill.dump(self.action, table_pkl)
                with open('cache/parser_goto_table.pkl', 'wb') as table_pkl:
                    dill.dump(self.goto, table_pkl)
        else:
            try:
                with open('cache/parser_action_table.pkl', 'rb') as table_pkl:
                    self.action = dill.load(table_pkl)
                with open('cache/parser_goto_table.pkl', 'rb') as table_pkl:
                    self.goto = dill.load(table_pkl)
            except:
                pass    #ERROR, Lexer automaton file not found                      #error


    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []
        operations = []

        BORRAME = 0

        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])

            if (state, lookahead) not in self.action:
                print((state, lookahead))
                print("Error. Aborting...")                                          # !ERROR!
                # for i in range(0,cursor+1):
                #     print(w[i])
                # print(output)
                # print(operations)
                # for (x,y) in self.action:
                #     if(x==state):
                #         print(x,y)
                return None

            action, tag = self.action[state, lookahead]

            if action == self.SHIFT:
                cursor += 1
                stack.append(tag)

                operations.append(self.SHIFT)
            elif action == self.REDUCE:
                head, body = tag
                for _ in body:
                    stack.pop()

                state = stack[-1]
                goto = self.goto[state, head]

                stack.append(goto)

                operations.append(self.REDUCE)
                output.append(tag)
            elif action == self.OK:
                return output, operations
            else:
                raise Exception('Invalid action!!!')                                # !ERROR!

def expand(item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()

    for preview in item.Preview():
        lookaheads.update(compute_local_first(firsts, preview))

    assert not lookaheads.contains_epsilon

    return [Item(p, 0, lookaheads) for p in next_symbol.productions]

def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()}

def closure_lr1(items, firsts):
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()

        for item in closure:
            new_items.extend(expand(item, firsts))

        changed = closure.update(new_items)

    return compress(closure)

def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'            # !ERROR!
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)

def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'                 # !ERROR!

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)
    automaton = State(frozenset(closure), True)

    pending = [start]
    visited = {start: automaton}

    while pending:
        current = pending.pop()
        current_state = visited[current]

        for symbol in G.terminals + G.nonTerminals:
            items = current_state.state
            kernel = goto_lr1(items, symbol, just_kernel=True)

            if not kernel:
                continue
            try:
                next_state = visited[kernel]
            except:
                closure = goto_lr1(items, symbol, firsts)
                next_state = visited[kernel] = State(frozenset(closure), True)
                pending.append(kernel)

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton

class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for look in item.lookaheads:
                            self._register(self.action, (idx, look), (self.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    if (next_symbol.IsTerminal or next_symbol == G.EOF) and node.has_transition(next_symbol.Name):
                        self._register(self.action, (idx, next_symbol), (self.SHIFT, node[next_symbol.Name][0].idx))
                    if next_symbol.IsNonTerminal and node.has_transition(next_symbol.Name):
                        self._register(self.goto, (idx, next_symbol), node[next_symbol.Name][0].idx)

    @staticmethod
    def _register(table, key, value):  
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'             # !ERROR!
        table[key] = value