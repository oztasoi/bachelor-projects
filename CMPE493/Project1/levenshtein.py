from backtrack import backtrack

ALG = "Levenshtein"

def levenshteinDistance(_word1, _word2):
    word1 = " " + _word1 # Add the empty string to adjust
    word2 = " " + _word2 # Add the empty string to adjust
    dim1 = len(word1)
    dim2 = len(word2)

    # Create the edit table and init each value with 0
    lvData = [ [ 0 for i in range(dim2) ] for j in range(dim1) ] 

    # Add initial values of the table for word1
    for i in range(dim1):
        lvData[i][0] = i

    # Add initial values of the table for word2
    for j in range(dim2):
        lvData[0][j] = j

    # Complexity is O(dim1 * dim2), multiplication of the lenghts of both words
    for i in range(1, dim1):
        for j in range(1, dim2):
            # If the characters are the same, there's no cost.
            if word1[i] == word2[j]: 
                lvData[i][j] = lvData[i-1][j-1]
            # If not, the cost is one more than its precalculated 3 formation,
            # which are an insertion, a deletion or a substitution events.
            else:
                lvCost = 1 + min(lvData[i-1][j-1], lvData[i-1][j], lvData[i][j-1])
                lvData[i][j] = lvCost

    return (dim1, dim2), lvData, lvData[dim1 - 1][dim2 - 1]


def levenshtein(_word1, _word2):
    (dim1, dim2), data, result = levenshteinDistance(_word1, _word2)

    # call for backtracking
    backtrack(ALG, data, dim1-1, dim2-1, _word1, _word2, result)
