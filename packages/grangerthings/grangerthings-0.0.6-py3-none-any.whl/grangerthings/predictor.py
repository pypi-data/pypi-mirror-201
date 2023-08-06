from .automata import GenerativeAutomaton, CrossedAutomaton, AutomataComposition
from .wordutils import max_word_length, all_words, word_to_id, next_id, cross_counts, _cross_count, cross_distribution, word_occurrence
from .quickhull import quickhull
import numpy as np
import copy
from random import Random
    
# For a given word generate an automaton that predicts the next symbol 
def make_auto_regressive_automaton(word, epsilon = 0.05, min_occurrences=0, _max_length = 3, sublanguage=[], tracer=None):
    model = make_cross_automaton(word, word, epsilon, min_occurrences, _max_length, morph_as_weight = True, sublanguage = sublanguage, tracer = tracer) 
    #model = GenerativeAutomaton(model.transitions, _alphabet_size = model.alphabet_size) 
    return model
    
# For a given word_a generate an automaton that predicts the next symbol for a given word_b
def make_cross_automaton(word_a, word_b, epsilon = 0.05, min_occurrences=0, _max_length = 3, morph_as_weight = False, sublanguage = [], tracer=None):
    alphabet_a_size = max(2, max(word_a) + 1)
    alphabet_b_size = max(2, max(word_b) + 1)
    max_length = _max_length
    if max_length < 0:
        max_length = max_word_length(alphabet_a_size, epsilon)
    _sublanguage = sublanguage
    if sublanguage == []: 
        _sublanguage = all_words(alphabet_a_size, max_length)
    counts = cross_counts(word_a, word_b, _sublanguage, alphabet_b_size)
    derivatives = [cross_distribution(word_a, word_b, w, alphabet_a_size, alphabet_b_size, counts) for w in _sublanguage] 
    occurrences = [sum(x) for x in counts] 
    hull = quickhull(derivatives, occurrences, epsilon, min_occurrences)
    chosen = max(hull, key = lambda candidate: occurrences[candidate]) # TODO: check if max is neccessary, perhaps any is sufficient
    states = create_cross_transitions(word_a, word_b, alphabet_a_size, alphabet_b_size, counts, _sublanguage[chosen], epsilon)
    transitions = [] 
    morph = [[0.0] * alphabet_b_size for i in range(len(states))]
    for state in states:
        morph[state['id']] = state['derivative']
        for symbol, t in state['transition'].items():
            weight = 1  
            if morph_as_weight: 
                weight = morph[state['id']][symbol]
            transitions.append((state['id'], symbol, weight, t['next']))
    if len(transitions) == 0: 
        return None 
    model = CrossedAutomaton(alphabet_a_size, transitions, alphabet_b_size, morph)
    state_meta = {s['id']: {'word': s['word'], 'count': word_occurrence(word_a, s['word'], word_b, alphabet_a_size, alphabet_b_size, occurrences)} for s in states}  
    trace(tracer, 'raw', model)
    model = model.extract_strongly_connected_automaton(state_meta) 
    trace(tracer, 'final', model)
    trace(tracer, 'alphabet_a', alphabet_a_size)
    trace(tracer, 'alphabet_b', alphabet_b_size)
    trace(tracer, 'max_length', max_length)
    trace(tracer, 'counts', counts)
    trace(tracer, 'derivatives', derivatives)
    trace(tracer, 'occurrences', occurrences)
    trace(tracer, 'hull', hull)
    trace(tracer, 'chosen', chosen)
    trace(tracer, 'state_meta', state_meta)
    return model 
    
def derivative_distance(a, b):
    diff = [a[i] - b[i] for i in range(len(a))]
    return sum([x*x for x in diff]) ** 0.5  

def create_cross_transitions(sample_a, sample_b, alphabet_a_size, alphabet_b_size, cross_counts, start_word, epsilon):
    #cross_distribution(sample_a, sample_b, word, alphabet_a, alphabet_b, cross_counts):
    init_derivative = cross_distribution(sample_a, sample_b, start_word, alphabet_a_size, alphabet_b_size, cross_counts)
    init_state = {'id': 0, 'derivative': init_derivative, 'word': start_word, 'transition': dict(), 'count': 0}
    states = [init_state]
    _create_cross_transitions(sample_a, sample_b, alphabet_a_size, alphabet_b_size, cross_counts, epsilon, states, [init_state]) 
    return states

def _create_cross_transitions(sample_a, sample_b, alphabet_a_size, alphabet_b_size, cross_counts, epsilon, states, open_states):
    #TODO: handle case where counts is too low or probability reaches 0's 
    if not open_states:
        return 
    new_states = []
    for state in open_states:
        for symbol in range(alphabet_a_size):
            word = state['word'] + [symbol]
            l = [0] * alphabet_b_size
            _cross_count(sample_a, word, sample_b, l)
            word_occurrence = sum(l) 
            derivative = cross_distribution(sample_a, sample_b, word, alphabet_a_size, alphabet_b_size, cross_counts)
            if sum(derivative) <= .95: # filter out non-occurring derivatives
                continue
            found = False 
            for peer in states:
                if derivative_distance(derivative, peer['derivative']) <= epsilon:
                    state['transition'][symbol] = {'next': peer['id'], 'p': 0, 'ctr': 0}
                    found = True
                    break 
            if not found:
                new_state = {'id': len(states), 'derivative': derivative, 'word': word, 'transition': dict(), 'count': 0}
                states.append(new_state)
                new_states.append(new_state)
                state['transition'][symbol] = {'next': new_state['id'], 'p': 0, 'ctr': 0}
    _create_cross_transitions(sample_a, sample_b, alphabet_a_size, alphabet_b_size, cross_counts, epsilon, states, new_states)    

def make_granger_network(words, names, epsilon=0.05, timeshift=1, minimal_dependence = 0.3, max_length = 3, min_occurrences=1, tracer=None, print_progress=False): 
    sublanguages = {}
    pfsa_lists = [list() for i in range(len(words))] # word-index X delay => pfsa
    alphabet_sizes = []
    auto_predictors = []
    
    nr_pfsa = float(len(words)*timeshift)
    nr_xpfsa = float(len(words)*len(words)*timeshift)
    progress = 0.0
    
    for i in range(len(words)):
        word = words[i]
        alphabet_size = max(word) + 1
        alphabet_sizes.append(alphabet_size)
        if alphabet_size not in sublanguages:  
            sublanguages[alphabet_size] = all_words(alphabet_size, max_length) 
        sublanguage = sublanguages[alphabet_size]  
        for time in range(timeshift):
            word = words[i] if time == 0 else words[i][:-time] 
            # PFSA per word-delay 
            # TODO: if delay is insignificant given word length, then you could use the same PFSA per delay
            automaton = make_auto_regressive_automaton(word, epsilon, min_occurrences, max_length, sublanguage)
            pfsa_lists[i].append(automaton) 
            new_progress = float(100*(i*timeshift+time+1)) / nr_pfsa 
            if print_progress and int(new_progress) > int(progress):
                print(int(new_progress))
            progress = new_progress  
    progress = 0.0
    granger = {}
    for i in range(len(words)): 
        alphabet_a_size = alphabet_sizes[i]
        sublanguage = sublanguages[alphabet_a_size]
        for j in range(len(words)):  
            for time in range(timeshift):
                # XPFSA
                word_a = words[i] if time == 0 else words[i][:-time]
                word_b = words[j][time:]
                pfsa = pfsa_lists[i][time] 
                xpfsa = make_cross_automaton(word_a, word_b, epsilon, min_occurrences, max_length, sublanguage=sublanguage) 
                new_progress = float(100*( i*len(words)*timeshift + j*timeshift + 1 )) / nr_xpfsa
                if print_progress and int(new_progress) > int(progress):
                    print(int(new_progress))
                progress = new_progress
                # Predictor 
                dependence_coefficient = xpfsa.dependence_coefficient(word_a, word_b)  
                if i == j and time == 0: 
                    automata_composition = AutomataComposition(pfsa_lists[i][time], xpfsa)
                    auto_predictors.append({'source': names[i], 'delay': 0, 'predictor':predictor_json(automata_composition, 0.0, xpfsa)}) 
                if dependence_coefficient <= minimal_dependence: 
                    continue 
                automata_composition = AutomataComposition(pfsa_lists[i][time], xpfsa)
                if names[j] not in granger: 
                    granger[names[j]] = []
                granger[names[j]].append({
                    'source': names[i],
                    'predictor': predictor_json(automata_composition, dependence_coefficient, xpfsa),
                    'delay': time
                })
    for i in range(len(words)):
        if names[i] not in granger: 
            # If there are no incoming automata, then use the auto predictor based on the prior distribution as predictor
            auto_predictors[i]['predictor']['dependence_coefficient'] = 0.000001
            granger[names[i]] = list()
        granger[names[i]].append(auto_predictors[i])
    return granger           

def predictor_json(automata_composition, dependence_coefficient, xpfsa):
    return {
            'init_distribution': automata_composition.projection.get_stationary_distribution(),
            'dependence_coefficient': dependence_coefficient,
            'symbol_matrices': [l.tolist() for l in automata_composition.projection.symbol_matrices],
            'crossed_probabilities': xpfsa.weights_as_matrix.tolist()
        } 
        
def predictor_from_json(json):   
    return {
        'init_distribution': [float(i) for i in json['init_distribution']],
        'dependence_coefficient': float(json['dependence_coefficient']),
        'symbol_matrices': [ [ [float(i) for i in c] for c in m] for m in json['symbol_matrices'] ],
        'crossed_probabilities': [ [float(i) for i in l] for l in json['crossed_probabilities'] ]
    } 
    
def local_prediction(observed_word, predictor, tracer):
    state_distribution = predictor['init_distribution']
    trace(tracer, 'trace', list())
    for symbol in observed_word: 
        new_state_distribution = np.dot(state_distribution, predictor['symbol_matrices'][symbol])
        if sum(new_state_distribution) == 0.0:
            continue
        state_distribution = new_state_distribution / sum(new_state_distribution) 
        if tracer != None:
            tracer['trace'].append({
                'symbol': symbol,
                'matrix': predictor['symbol_matrices'][symbol],
                'result': copy.deepcopy(state_distribution).tolist()
            })
    prediction = np.dot(state_distribution, predictor['crossed_probabilities']).tolist()
    trace(tracer, 'prediction', prediction)
    trace(tracer, 'init', predictor['init_distribution'])
    trace(tracer, 'morph', predictor['crossed_probabilities']) 
    return prediction
    
def trace_predictor_creation(word_a, word_b, epsilon = 0.05, min_occurrences=0, max_length=3):
    trace_pfsa = dict()
    pfsa = make_auto_regressive_automaton(word_a, epsilon, min_occurrences, max_length, tracer=trace_pfsa)
    trace_xpfsa = dict()
    xpfsa = make_cross_automaton(word_a, word_b, epsilon, min_occurrences, max_length, tracer=trace_xpfsa)
    dependence_coefficient = xpfsa.dependence_coefficient(word_a, word_b)  
    composition = AutomataComposition(pfsa, xpfsa)
    predictor = predictor_json(composition, dependence_coefficient, xpfsa)
    return predictor, {
        'pfsa': trace_pfsa, 
        'xpfsa': trace_xpfsa,
        'dependence_coefficient': dependence_coefficient,
        'composition': composition.composition.serialize_str(),
        'projection': composition.projection.serialize_str(),
        'projection_stationary_distribution': composition.projection.get_stationary_distribution(),
        'xpfsa_weight_matrix': xpfsa.weights_as_matrix.tolist(),
        'symbol_matrices': [l.tolist() for l in composition.projection.symbol_matrices]
    } 
    
def trace(dict, key, value):
    if dict == None: 
        return  
    if key == 'hull':
        dict[key] = list(value)
        return 
    if key == 'raw' or key == 'final':
        dict[key] = value.serialize_str()
        return
    dict[key] = value    
        
def generate(granger, length, seed = 1): 
    words = {s: list() for s in granger}
    _predict(granger, words, generate_length = length, seed=seed)
    return words 
    
def predict(granger, observations, stepwise = False, tracer = None):
    return _predict(granger, observations, stepwise = stepwise, tracer = tracer)

def _predict(granger, observations, stepwise = False, tracer = None, generate_length = -1, seed = 1):
    states = dict()
    for source in granger: 
        states[source] = dict() 
        for edge in granger[source]: 
            if edge['source'] not in states[source]:
                states[source][edge['source']] = dict()
            states[source][edge['source']][edge['delay']] = list(edge['predictor']['init_distribution'])
    predictions = []
    
    # slide over all the observations 
    time_max = generate_length if generate_length >= 0 else len(next(iter(observations.values())))
    rng = Random(seed)
    alphabet = []
    for time in range(-1, time_max):
        # go through all predictors to feed the next symbol 
        for source in granger: 
            for edge in granger[source]: 
                # ignore the auto-predictors 
                if edge['predictor']['dependence_coefficient'] == 0: 
                    continue 
                delay = edge['delay']
                # only feed the symbol if you are sufficiently far 
                if time - delay >= 0: 
                    symbol = observations[edge['source']][time - delay]
                    current = states[source][edge['source']][delay]
                    new_distribution = np.dot(current, edge['predictor']['symbol_matrices'][symbol])
                    if sum(new_distribution) == 0.0:
                        continue
                    states[source][edge['source']][delay] = new_distribution / sum(new_distribution)
        if stepwise: # If stepwise, collect all the in-between predictions 
            predictions.append(_local_predictions(granger, states, tracer))
        # For generation; generate the next symbol for each source 
        if generate_length >= 0: 
            local_predictions = _local_predictions(granger, states)
            for source in granger:                 
                if len(alphabet) == 0: 
                    alphabet = list(range(len(local_predictions[source])))
                symbol = rng.choices(alphabet, weights = local_predictions[source], k = 1)[0]
                observations[source].append(symbol)
    # collect final prediction    
    if stepwise: 
        return predictions
    return _local_predictions(granger, states)
        
def _local_predictions(granger, states, tracer=None):
    prediction = dict()
    if tracer != None: 
        if not 'local_trace' in tracer: 
            trace(tracer, 'local_trace', {s: list() for s in granger})
        
    for source in granger: 
        inputs = [] 
        total_weight = sum(float(i['predictor']['dependence_coefficient']) for i in granger[source])
        prediction[source] = []
        for edge in granger[source]: 
            state_distribution = states[source][edge['source']][edge['delay']]
            local_prediction = np.dot(state_distribution, edge['predictor']['crossed_probabilities']).tolist()
            if len(prediction[source]) == 0: 
                prediction[source] = [0] * len(local_prediction)
            normalized_weight = edge['predictor']['dependence_coefficient'] / total_weight
            for i in range(len(local_prediction)): 
                prediction[source][i] += normalized_weight * local_prediction[i]
            if tracer != None: 
                inputs.append({
                    'source': edge['source'],
                    'delay': edge['delay'],
                    'weight': edge['predictor']['dependence_coefficient'],
                    'weight_normalized': normalized_weight,
                    'prediction': local_prediction
                })
        prediction[source][-1] = 1 - sum(prediction[source][:-1]) # to fix rounding errors
        if tracer != None: 
            tracer['local_trace'][source].append({
                'final': prediction[source], 
                'input': inputs
            }) 
    return prediction

def prune(granger, minimal_dependence = -1000): 
    pruned = dict() 
    for source, edges in granger.items():
        pruned[source] = list() 
        for edge in edges:
            # Ignore low predictive edges 
            if edge['predictor']['dependence_coefficient'] < minimal_dependence: 
                continue 
            # Ignore automata with a single state, these cannot add value, but may result
            # from the automaton construction algorithm 
            if len(edge['predictor']['init_distribution']) == 1: 
                continue 
            # Note that an edge of probability 1 practically indicates that either the automaton 
            # is effectively single state or the algorithm didn't find a proper model 
            if 1.0 in edge['predictor']['init_distribution']:
                continue 
            pruned[source].append(edge)
        # If there is no automaton left, then use the auto-predictor 
        if len(pruned[source]) == 0: 
            edge = edges[-1]
            edge['predictor']['dependence_coefficient'] = 0.000001
            pruned[source].append(edge)
    return pruned 
