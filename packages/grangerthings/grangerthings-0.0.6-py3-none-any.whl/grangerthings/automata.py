from random import Random
import math 
from typing import List, Dict
import numpy as np
import sys

        
# Generator based on state transitions where edges have a probability and symbol that they produce. 
class GenerativeAutomaton():
    def __init__(self, transitions, _alphabet_size = -1, seed = 1):
        self.transitions = transitions
        # transitions have form: (stateidx, symbol, probability weight, newstateidx)
        self.alphabet_size = _alphabet_size
        if _alphabet_size < 0: 
            self.alphabet_size = len({s for (_, s, _, _) in transitions})
        self.alphabet = list(range(self.alphabet_size))
        self.seed = seed 
        self.rng = Random(seed)
        
        self.nr_states = max([s for (s, _, _, _) in transitions]) + 1 
        self.edges = [[0] * self.alphabet_size for i in range(self.nr_states)] # state x symbol => next state 
        self.weights = [[.0] * self.alphabet_size for i in range(self.nr_states)] # state x symbol => probability
        for transition in transitions: 
            self.edges[transition[0]][transition[1]] = transition[3]
            self.weights[transition[0]][transition[1]] = transition[2]
        self.weights_as_matrix = np.array(self.weights) # Pi from the paper
        self.symbol_matrices = [] # Gamma_sigma from the paper 
        for symbol in self.alphabet: 
            self.symbol_matrices.append(np.array([[.0] * self.nr_states for i in range(self.nr_states)]))
            for state_a in range(self.nr_states):  
                self.symbol_matrices[symbol][state_a, self.edges[state_a][symbol]] = self.weights[state_a][symbol] 
        self.stationary_distribution = None
        self.cursor = 0
        
    def get_stationary_distribution(self):
        if self.stationary_distribution is not None: 
            return self.stationary_distribution
        self.stationary_distribution = self.compute_stationary_distribution()
        return self.stationary_distribution
        
    # Generate a symbol and move to the next state 
    def next(self):
        symbol = self.peak()
        self.cursor = self.edges[self.cursor][symbol]  
        return symbol
    
    # Generate a symbol 
    def peak(self): 
        weights = self.weights[self.cursor]
        if sum(weights) <= 0.0 + sys.float_info.epsilon:
            weights = [1 for i in weights]
        return self.rng.choices(self.alphabet, weights = weights, k = 1)[0]
    
    # Move the state cursor based on reading the word 
    def swallow(self, word):
        for symbol in word: 
            self.cursor = self.edges[self.cursor][symbol]  
        
    # Calculate the stationary distribution of the automaton. This is the eigen vector of the 
    # transition matrix. The transition matrix are the probabilities (regardless of used edge) 
    # to move from one state to another. 
    # solution from https://towardsdatascience.com/markov-chain-analysis-and-simulation-using-python-4507cee0b06e
    def compute_stationary_distribution(self):
        result = None 
        # state <-> state probabilities regardless of symbol 
        state_transition_matrix = [[.0] * self.nr_states for i in range(self.nr_states)]
        for a in range(self.nr_states):
            for s in self.alphabet:
                state_transition_matrix[a][self.edges[a][s]] += self.weights[a][s] 
        try: 
            P = np.array(state_transition_matrix)
            A = np.append(np.transpose(P)-np.identity(self.nr_states),[[1] * self.nr_states],axis=0)
            b = np.transpose(np.array([0]*self.nr_states + [1]))
            rank_coefficient = np.linalg.matrix_rank(np.append(A,np.transpose(b.reshape(1,self.nr_states + 1)), axis=1))
            rank_augmented = np.linalg.matrix_rank(A)
            if rank_coefficient == rank_augmented:  
                result = np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b)) 
        except Exception as X:  
            print(X)
        if not result is None:
            return result.tolist()
        # TODO: [potentially fixed now] find out why sometimes the eigenvector is not found
        # check literature for when the ranks of matrices do not match
        #print('Eigen vector not found, simulation fallback')
        #print(state_transition_matrix)
        k = 10000
        self.cursor = 0
        counts = [0] * self.nr_states
        for i in range(k): 
            self.next()
            counts[self.cursor] += 1
        self.cursor = 0
        vector = [counts[i] / k for i in range(self.nr_states - 1)]
        vector.append(1 - sum(vector))
        return vector
        
    # Extract a strongly connected component with the highest support, 
    # returns None if automaton is already strongly connected
    def extract_strongly_connected_automaton(self, state_counts):
        components = self.strongly_connected_components()
        if len(components) == 1:
            return self # already strongly connected  
        components = self.prune_connected_components(components)
        states, transitions = self.strongly_connected_transitions(state_counts, components)
        self.rename_transition_states(states, transitions)
        automaton = GenerativeAutomaton(transitions)
        return automaton
    
    def prune_connected_components(self, components):
        # Remove single state components, since they form bad automata anyway
        nondegenerate = [c for c in components if len(c) > 1] 
        # TODO: check if other types of components can be removed
        return components if len(nondegenerate) == 0 else nondegenerate
        
    def rename_transition_states(self, states, transitions):
        mapping = dict()
        for state in states: 
            mapping[state] = len(mapping)
        for i in range(len(transitions)):
            t = transitions[i]
            transitions[i] = (mapping[t[0]],t[1], t[2], mapping[t[3]])
        return mapping
    
    def strongly_connected_transitions(self, state_counts, components):  
        supports = [sum([state_counts[i]['count'] for i in component]) for component in components]
        choice = components[max(range(len(components)), key = lambda i: supports[i])]
        transitions = [] 
        for state in choice: 
            for symbol in self.alphabet:
                target = self.edges[state][symbol]
                # Target not in choice, TODO: this case is not discussed in paper, choose to reroute to nearest alternative in 'choice' instead
                if target not in choice:
                    a = self.weights[target]
                    nearest = state 
                    smallest_difference = float('inf')
                    for candidate in choice: 
                        b = self.weights[candidate]
                        diff = sum([x*x for x in [a[i] - b[i] for i in range(len(a))]])
                        if diff < smallest_difference:
                            smallest_difference = diff 
                            nearest = candidate
                    target = nearest
                transitions.append((state, symbol, self.weights[state][symbol], target))
        return choice, transitions
    
    # Get the states that form the strongly connected components
    def strongly_connected_components(self):
        numbering = [0] * self.nr_states
        lowlink = [0] * self.nr_states 
        components = [] 
        for next_state in range(self.nr_states):
            if numbering[next_state] == 0: 
                self._tarjan(next_state, numbering, lowlink, components, [], {'c': 0})
        return components
    
    # The standard algorithm by Tarjan to find the connected components
    def _tarjan(self, state, numbering, lowlink, components, stack, numbering_counter):
        numbering_counter['c'] += 1  
        numbering[state] = numbering_counter['c']
        lowlink[state] = numbering_counter['c']
        #print('A '+str(state)+" n="+str(numbering[state])+" ll="+str(lowlink[state]))
        stack.append(state)
        # TODO: if edges probabilities are 0 then should they count as an edge? 
        # Note that filtering them out is not straightforward as edges of cross automata 
        # always have a 0-weight. Solution might be to assign 1 for all cross automata 
        # transitions rather than 0. 
        for symbol in [s for s in self.alphabet]:
            child = self.edges[state][symbol]
            #print(str(state)+" => "+str(child))
            # tree arc 
            if numbering[child] == 0: 
                self._tarjan(child, numbering, lowlink, components, stack, numbering_counter)
                lowlink[state] = min(lowlink[state], lowlink[child])
                #print('B '+str(state)+" n="+str(numbering[state])+" ll="+str(lowlink[state]))
            # frond or cross link
            elif numbering[child] < numbering[state] and child in stack: 
                lowlink[state] = min(lowlink[state], numbering[child])
                #print('C '+str(state)+" n="+str(numbering[state])+" ll="+str(lowlink[state]))
        # check if state is root of strongly connected component 
        if lowlink[state] == numbering[state]:
            component = set() 
            #print([str((x, numbering[x])) for x in stack])
            while stack:
                vertex = stack.pop()
                if numbering[vertex] >= numbering[state]: 
                    component.add(vertex)
                else: 
                    stack.append(vertex)
                    break
            components.append(component)
            
    def serialize_str(self):
        string = ''
        for stateA in range(self.nr_states): 
            for symbol in self.alphabet:
                stateB = self.edges[stateA][symbol]
                weight = self.weights[stateA][symbol]
                string += str(stateA) + ', ' + str(symbol) + ', ' + str(weight) + ', ' + str(stateB) + '\n'
        return string 
        
    def __str__(self):
        string = '' 
        for stateA in range(self.nr_states): 
            for symbol in self.alphabet:
                stateB = self.edges[stateA][symbol]
                weight = self.weights[stateA][symbol]
                string += 'q'+str(stateA) + ' -(' + str(symbol) + ', ' +str(weight) + ')-> ' + 'q'+str(stateB) +'\n' 
        string += 'alphabet = ' + str(self.alphabet) +' '
        string += ' stationary distribution = ' + str(self.get_stationary_distribution())
        return string 

# Generator based on state transitions where each state has a probability distribution over a secondary alphabet 
# which is used to generate a stream. A primary alphabet is used to transition between states of this automaton.
class CrossedAutomaton(GenerativeAutomaton):
    def __init__(self, primary_alphabet_size, transitions, secondary_alphabet_size, morph, seed = 1):
        super().__init__(transitions, _alphabet_size = primary_alphabet_size, seed=seed)
        self.secondary_alphabet = list(range(secondary_alphabet_size))
        self.morph = morph
        self.weights_as_matrix = np.array(self.morph) # override Pi with morph function
            
    # Generate a next symbol pair and move the state cursor 
    def crossed_next(self): 
        symbol_a, symbol_b = self.crossed_peak()
        self.cursor = self.edges[self.cursor][symbol_a]  
        return symbol_a, symbol_b 
        
    # Generate a next symbol pair 
    def crossed_peak(self):
        weights = self.morph[self.cursor]
        if sum(weights) <= 0.0 + sys.float_info.epsilon:
            weights = [1 for i in weights]
        return super().peak(), self.rng.choices(self.secondary_alphabet, weights=weights, k=1)[0]  
        
    # Read a word and count for each state how often it was visited
    def stream_run(self, word):
        self.cursor = 0
        result = [0] * self.nr_states
        result[self.cursor] += 1
        for symbol in word: 
            self.cursor = self.edges[self.cursor][symbol]  
            result[self.cursor] += 1
        sum_result = sum(result) 
        result = [result[i] / sum_result for i in range(self.nr_states)]
        result[-1] = 1 - sum(result[:-1])
        return result 
        
    def extract_strongly_connected_automaton(self, state_counts):
        components = self.strongly_connected_components()
        if len(components) == 1:
            return self # already strongly connected 
        components = self.prune_connected_components(components)
        states, transitions = self.strongly_connected_transitions(state_counts, components) 
        mapping = self.rename_transition_states(states, transitions)
        new_morph = [[]] * len(states)
        for state in states: 
            new_morph[mapping[state]] = self.morph[state]
        automaton = CrossedAutomaton(self.alphabet_size, transitions, len(self.secondary_alphabet), new_morph)
        return automaton
        
    # Determine the Granger causality magnitude between word_a and word_b as learned by this automaton
    def dependence_coefficient(self, word_a, word_b):
        b_occurrences = [0] * len(self.secondary_alphabet)
        for s in word_b: 
            b_occurrences[s] += 1
        sum_b_occurrences = sum(b_occurrences)
        b_occurrences = [b_occurrences[i] / sum_b_occurrences for i in range(len(b_occurrences))]
        def log2(x):
            if x > 0: 
                return math.log2(x)
            return 0
        denominator = sum([b_occurrences[i] * log2(b_occurrences[i]) for i in range(len(self.secondary_alphabet))])
        numerator = 0 
        stream_run = self.stream_run(word_a)
        for s in range(self.nr_states):
            morph = self.morph[s] 
            numerator += stream_run[s] * sum([x * log2(x) for x in morph])
        #print(str(numerator) + ' '+ str(denominator))
        if denominator == 0.0:
            denominator = 1
            numerator = 1
        # The  '1-' minus part is not in algorithm 2 but is part of lemma 16
        return 1 - (numerator / denominator)
        
    def serialize_str(self):
        string = super().serialize_str()
        for i in range(self.nr_states):
            string += str(i) 
            for j in range(len(self.morph[i])):
                string += ', ' + str(j) + ':' +str(self.morph[i][j])
            string += '\n'
        return string 
        
    def __str__(self):
        string = super().__str__()
        string += '\n' + 'secondary alphabet = ' + str(self.secondary_alphabet)
        string += '\n'+'morph = {' + '\n'
        for i in range(self.nr_states):
            string += '\t q' + str(i) + ': ' + str(self.morph[i]) + '\n'
        string += '}'
        return string 
        
# Helper class for combining an auto-regressive automaton with a crossed automaton, by projecting the auto-regressive 
# automaton on the crossed automaton.  
# Inside the class a composition automaton is made that is used to produce a projection 
# automaton (details in causality networks paper). 
# The projection is used to determine given a short suffix of an observed word the probability distribution over the 
# states of the crossed automaton. This distribution is multiplied with the morph matrix of the crossed automaton to 
# produce the predicted next symbols for the alphabet of the auto-regressive automaton. 
class AutomataComposition():
    def __init__(self, model_a, model_b):
        self.a = model_a 
        self.b = model_b 
        alphabet_size = max(len(model_a.alphabet), len(model_b.alphabet))
        state_id = lambda x, y: y * model_a.nr_states + x
        get_y = lambda id: math.floor(id / model_a.nr_states)
        comp_transitions = [] 
        for x in range(model_a.nr_states):
            for y in range(model_b.nr_states):
                id = state_id(x, y)
                for symbol in model_a.alphabet: 
                    weight = model_a.weights[x][symbol]
                    next_a = model_a.edges[x][symbol]
                    next_b = model_b.edges[y][symbol]
                    comp_transitions.append((id, symbol, weight, state_id(next_a, next_b)))
        self.composition = GenerativeAutomaton(comp_transitions, _alphabet_size = alphabet_size)
        stationary = self.composition.get_stationary_distribution()
        proj_transitions = [] 
        for y in range(model_b.nr_states):
            for symbol in model_b.alphabet: 
                next = model_b.edges[y][symbol]
                weight = 0 
                cumulative_stationary = 0
                for t in [t for t in comp_transitions if get_y(t[0]) == y and t[1] == symbol]:
                    weight += t[2] * stationary[t[0]]
                    cumulative_stationary += stationary[t[0]]
                if weight > 0 and cumulative_stationary > 0: 
                    weight /= cumulative_stationary
                else:
                    weight = 0
                proj_transitions.append((y, symbol, weight, next))
        if isinstance(model_b, CrossedAutomaton):
            self.projection = CrossedAutomaton(alphabet_size, proj_transitions, len(model_b.morph[0]), model_b.morph)
        else:
            self.projection = GenerativeAutomaton(proj_transitions, _alphabet_size = alphabet_size)
