import pydot
from common.utils import ContainerSet, DisjointSet

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current][symbol][0]
            return True
        except KeyError:
            return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        for symbol in string:
            if not self._move(symbol):
                return False
        return self.current in self.finals
                
def move(automaton, states, symbol):
    moves = set()
    for state in states:
        assert state in automaton.transitions, 'Invalid state'
        try:
            res = automaton.transitions[state][symbol]
            for dest in res:
                moves.add(dest)
        except KeyError:
            pass
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        for dest in automaton.epsilon_transitions(state):
            closure.add(dest)
            pending.append(dest)
                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        for symbol in automaton.vocabulary:
            dests = move(automaton, state, symbol)
            dests = epsilon_closure(automaton, dests)
            id = -1
            for i in range(len(states)):
                if dests == states[i]:
                    id = i
                    break
            if len(dests):
                if id != -1:
                    new_state = states[id]
                else:
                    new_state = ContainerSet(*dests)
                    new_state.id = len(states)
                    new_state.is_final = any(s in automaton.finals for s in new_state)
                    states.append(new_state)
                    pending.append(new_state)
                
                transitions[state.id, symbol] = new_state.id
            '''
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                # Your code here
                pass'''
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2, symbol)] = [dest + d2 for dest in destinations]
    
    transitions[(start, '')] = [a1.start + d1, a2.start + d2]
    
    for f in a1.finals:
        transitions[(f + d1, '')] = [final]

    for f in a2.finals:
        transitions[(f + d2, '')] = [final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = [dest + d1 for dest in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2, symbol)] = [dest + d2 for dest in destinations]
    
    for f in a1.finals:
        transitions[(f + d1, '')] = [a2.start + d2]

    for f in a2.finals:
        transitions[(f + d2, '')] = [final]
            
    states = a1.states + a2.states + 1
    finals = { final }
    
    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = [dest + d1 for dest in destinations]
    
    transitions[(start, '')] = [a1.start + d1, final]
    
    for f in a1.finals:
        try:
            transitions[(f + d1, '')] += [start]
        except KeyError:
            transitions[(f + d1, '')] = [start]
            
    states = a1.states +  2
    finals = { final }
    
    return NFA(states, finals, transitions, start)


def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        transitions = automaton.transitions[member.value]
        labels = ((transitions[symbol][0] if symbol in transitions else None) for symbol in vocabulary)
        key = tuple((partition[node].representative if node in partition.nodes else None) for node in labels)
        try:
            split[key].append(member.value)
        except KeyError:
            split[key] = [member.value]

    return [ group for group in split.values()]
            
def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    ## partition = { NON-FINALS | FINALS }
    partition.merge(automaton.finals)
    partition.merge(q for q in range(automaton.states) if q not in automaton.finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        for group in partition.groups:
            distinguished = distinguish_states(group, automaton, partition)
            for subgroup in distinguished:
                new_partition.merge(subgroup)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    
    states = [s for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            representative = partition[destinations[0]].representative
            j = states.index(representative)
            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = j
    
    start = states.index(partition[automaton.start].representative)
    finals = [i for i, state in enumerate(states) if state.value in automaton.finals]

    return DFA(len(states), finals, transitions, start)