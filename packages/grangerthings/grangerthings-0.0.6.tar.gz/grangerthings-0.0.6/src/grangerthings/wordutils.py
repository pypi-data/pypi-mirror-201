import math
from typing import List

def max_word_length(alphabet_size: int, epsilon: float) -> int:
    """ 
    Returns a suggested maximum subword length given the alphabet symbols and precision parameter epsilon.
    :param alphabet_size: Number of unique symbols in the alphabet.
    :param epsilon: Precision parameter.
    """ 
    return math.ceil(math.log(1 / epsilon, alphabet_size))
    
def all_words(alphabet_size: int, max_length: int) -> List[List[int]]: 
    """
    Returns a list containing all words given the size of the alphabet with a length up to and including the provided maximum length. 
    :param alphabet_size: Number of unique symbols in the alphabet.
    :param max_length: Maximum length of the returned subwords. 
    """
    return _all_words(list(range(alphabet_size)), max_length, 1, [[]], [[]]) 
    
def _all_words(alphabet: List[int], max_length: int, current_length: int, acc: List[List[int]], last_round: List[List[int]]) -> List[List[int]]:
    """
    Generates the words by first generating words of length 0, then length 1, etc, in a recursive manner.
    """
    if max_length < current_length:
        return acc
    acc_expansion = [] 
    for symbol in alphabet: 
        for word in last_round: 
            acc_expansion.append(list(word)+[symbol])
    return _all_words(alphabet, max_length, current_length + 1, acc + acc_expansion, acc_expansion)

def word_to_id(word: List[int], alphabet_size: int) -> int: 
    """
    Converts a word to a unique identifier for a given alphabet size.
    :param alphabet_size: Number of unique symbols in the alphabet.
    :param word: Word.
    """ 
    word_len = len(word)
    id = (((alphabet_size ** word_len) - alphabet_size) / (alphabet_size - 1)) + 1
    for i in range(len(word)): 
        id += word[i] * (alphabet_size ** i)
    return int(id) 

def next_id(id: int, word_length: int, alphabet_size: int, symbol: int) -> int:
    """
    For a given id of a word, determine the id of the word if the provided symbol would be appended.
    :param id: Current id. 
    :param word_length: Length of the word.
    :param symbol: Symbol to be appended.
    :param alphabet_size: Number of unique symbols in the alphabet.
    """
    x = alphabet_size ** (word_length+1)
    x -= alphabet_size ** word_length 
    # TODO: extract word length from id 
    return int(id + x + symbol * (alphabet_size ** word_length))
    
def cross_counts(word_a: List[int], word_b: List[int], language_a: List[List[int]], alphabet_b_size: int) -> List[List[int]]:
    """
    For each word in language_a check for each occurrence in word_a what the follow-up symbols are in word_b. The returned map has type: WordID X Symbol => Int returning how often after the word with index i the given symbol s occurs.
    :param word_a: Origin word.
    :param word_b: Word to determine distributions of given word_a subwords.
    :param language_a: Language over alphabet of word_a to count the distribution over alphabet_b for per subword in the language.
    :param alphabet_b_size: Number of unique symbols in the alphabet from which word_b is generated. 
    """
    counts = [] 
    for subword in language_a:
        counts.append([0] * alphabet_b_size)
        _cross_count(word_a, subword, word_b, counts[-1])
    return counts 
    
def _cross_count(word_a: List[int], subword: List[int], word_b: List[int], counts: List[int]):
    """
    Modified knuth morris pratt for cross counting
    :param word_a: Origin word.
    :param subword: A subword of word_a.
    :param word_b: Word to determine distributions of given word_a subwords. 
    :param counts: Accumulator of counting results.
    """
    if not subword: 
        for s in range(len(counts)):
            counts[s] = word_b.count(s)
        return
    word_cursor = 0
    sub_cursor = 0
    kmt_table = _kmt_table(subword)
    while word_cursor < (len(word_a)-1): # +1 because you look-ahead in word b 
        if subword[sub_cursor] == word_a[word_cursor]:
            word_cursor += 1
            sub_cursor += 1
            if sub_cursor == len(subword): 
                counts[word_b[word_cursor]] += 1
                sub_cursor = kmt_table[sub_cursor]
        else:
            sub_cursor = kmt_table[sub_cursor] 
            if sub_cursor < 0: 
                word_cursor += 1
                sub_cursor += 1 

def word_occurrence(word_a, subword, word_b, alphabet_a_size, alphabet_b_size, cache):
    id = word_to_id(subword, alphabet_a_size)
    if id < len(cache):
        return cache[id]
    counts = [0] * alphabet_b_size
    _cross_count(word_a, subword, word_b, counts)
    return sum(counts)
    
def _kmt_table(word: List[int]) -> List[int]:
    """
    The knuth-morris-pratt table helps with 'sliding' the cursor from which to match strings during the execution of the kmt algorithm. 
    :param word: The word for which to make the KMT table.
    """
    table = [0] * (len(word)+1)
    table[0] = -1
    cursor = 1
    candidate = 0
    while cursor < len(word):
        if word[cursor] == word[candidate]:
            table[cursor] = table[candidate]
        else:
            table[cursor] = candidate
            while candidate >= 0 and word[cursor] != word[candidate]:
                candidate = table[candidate]
        cursor += 1
        candidate += 1
    table[cursor] = candidate
    return table

def cross_distribution(word_a: List[int], word_b: List[int], subword: List[int], alphabet_a_size: int, alphabet_b_size: int, cached_cross_counts: List[List[int]] = []) -> List[float]: 
    """
    For two given sample words and a sublanguage word, return the probability distribution over the alphabet induced by the subword (it's symbolic derivative). Cached counting from cross_count can be provided to speed up.  
    :param word_a: Origin word.
    :param word_b: Word to determine distributions of given word_a subwords. 
    :param subword: A subword of word_a.
    :param cached_cross_counts: Cache of counting results.
    :param alphabet_a_size: Number of unique symbols in the alphabet from which word_a is generated. 
    :param alphabet_b_size: Number of unique symbols in the alphabet from which word_b is generated. 
    """
    id = word_to_id(subword, alphabet_a_size)
    counts = None 
    if id >= len(cached_cross_counts):
        counts = [0] * alphabet_b_size
        _cross_count(word_a, subword, word_b, counts)
    else: 
        counts = cached_cross_counts[id]
    localsum = sum(counts)
    if localsum == 0:
        return [0] * alphabet_b_size
    counts = [counts[s] / localsum for s in range(0, alphabet_b_size - 1)] 
    counts.append(1 - sum(counts))
    return counts