from common.pycompiler import Grammar, Item, Symbol
from common.state import State, lr0_formatter, multiline_formatter
from common.utils import compute_firsts, compute_local_first, compute_follows
from common.utils import ContainerSet

def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [start_item]
    visited = {start_item: automaton}

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue

        new_transitions = []
        new_transitions_eps = []
        next_symbol = current_item.NextSymbol
        next_item = current_item.NextItem()

        if next_item not in visited:
            pending.append(next_item)
            visited[next_item] = State(next_item, final=True)

        new_transitions.append(next_item)

        if next_symbol.IsNonTerminal:
            for production in next_symbol.productions:
                new_item = Item(production, 0)

                if new_item not in visited:
                    pending.append(new_item)
                    visited[new_item] = State(new_item, final=True)

                new_transitions_eps.append(new_item)

        current_state = visited[current_item]

        for t in new_transitions:
            current_state.add_transition(next_symbol.Name, visited[t])

        for t in new_transitions_eps:
            current_state.add_epsilon_transition(visited[t])

    return automaton

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()

    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w):
        stack = [0]
        cursor = 0
        output = []
        operations = []

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

class SLR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(self.action, (idx, G.EOF), (self.OK, None))
                    else:
                        for symbol in follows[item.production.Left]:
                            self._register(self.action, (idx, symbol), (self.REDUCE, item.production))
                else:
                    next_symbol = item.NextSymbol
                    next_state = node[next_symbol.Name][0].idx
                    if next_symbol.IsTerminal or next_symbol == G.EOF:
                        self._register(self.action, (idx, next_symbol), (self.SHIFT, next_state))
                    if next_symbol.IsNonTerminal:
                        self._register(self.goto, (idx, next_symbol), next_state)

    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'                  # !ERROR!
        table[key] = value

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