

def quickhull(derivatives, occurrences, epsilon = 0, min_occurrences = 0):
    if not derivatives:
        return set()
    if len(derivatives) == 1:
        return {0}
    # TODO: check for 2d case if all points should be returned
    extremes = dimensional_extremes(derivatives, occurrences, epsilon, min_occurrences)
    dimensions = len(derivatives[0])
    if dimensions == 2: # In 2d case the polytope is a line, hence only the extremes are needed
        return extremes
    # If there is a suffiently occurring extreme point, then return that instead 
    
    # Create non-degenerate d-simplex, normally you need a d+1-simplex but since the derivatives form a 
    # hyperplane you only need a d-simplex for the convex hull
    
    #TODO: finish, now temporary
    return extremes
    
# Get indices of words in the language that are extreme derivatives 
# for any of the symbols, using epsilon leniency. 
def dimensional_extremes(derivatives, occurrences, epsilon = 0, min_occurrences = 0):
    if not derivatives: 
        return set()
    if len(derivatives) == 1: 
        return {0}
    dimensions = len(derivatives[0]) # size of alphabet  
    if dimensions == 2: # make use of the fact that in 2d case only x needs to be checked 
        dimensions = 1
    # extremes (min-max) per dimension 
    mins = [[float('inf')] * dimensions for i in range(dimensions)]
    maxs = [[float('-inf')] * dimensions for i in range(dimensions)]
    # epsilon-close points to extremes 
    mins_epsilon = [set() for i in range(dimensions)] 
    maxs_epsilon = [set() for i in range(dimensions)] 
    for idx in range(len(derivatives)): 
        if occurrences[idx] < min_occurrences:
            continue
        point = derivatives[idx] 
        for dimension in range(dimensions): 
            if point[dimension] < mins[dimension][dimension]:
                mins[dimension] = point
                mins_epsilon[dimension] = _filter_close(idx, point, mins_epsilon[dimension], dimension, derivatives, epsilon)
            elif abs(point[dimension] - mins[dimension][dimension]) <= epsilon:
                mins_epsilon[dimension].add(idx)
            if point[dimension] > maxs[dimension][dimension]:
                maxs[dimension] = point
                maxs_epsilon[dimension] = _filter_close(idx, point, maxs_epsilon[dimension], dimension, derivatives, epsilon)
            elif abs(point[dimension] - maxs[dimension][dimension]) <= epsilon:
                maxs_epsilon[dimension].add(idx)
    return set().union(*mins_epsilon).union(*maxs_epsilon)

def _filter_close(idx_a, point_a, indices, dimension, derivatives, epsilon = 0):
    result = set() 
    result.add(idx_a)
    for idx_b in indices: 
        point_b = derivatives[idx_b]
        if abs(point_a[dimension] - point_b[dimension]) <= epsilon: 
            result.add(idx_b)
    return result 