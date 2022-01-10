from backtrack import backtrack

ALG = "Damerau-Levenshtein"

def damerauLevenshteinDistance(_word1, _word2):
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
            # If the letters at the current positions are the same,
            # it is costless to edit one word from another.
            if word1[i] == word2[j]: subsCost = 0
            else: subsCost = 1

            # retrieving the minimum cost of 
            # insertion, replacement and deletion
            lvData[i][j] = min(lvData[i-1][j] + 1, lvData[i][j-1] + 1, lvData[i-1][j-1] + subsCost)
            # if a sequence of two letters are 
            # repeating at the same position 
            # but in a reversed manner of each
            # it is a substitution operation
            # and its cost would be only 1
            # rather than 2, and that's a
            # valid choice to minimize the
            # edit distance.
            if i > 1 and j > 1 and word1[i] == word2[j-1] and word1[i-1] == word2[j]:
                lvData[i][j] = min(lvData[i][j], lvData[i-2][j-2] + 1)

    return (dim1, dim2), lvData, lvData[dim1 - 1][dim2 - 1]


def damerauLevenshtein(_word1, _word2):
    (dim1, dim2), data, result = damerauLevenshteinDistance(_word1, _word2)

    # call for backtracking
    backtrack(ALG, data, dim1-1, dim2-1, _word1, _word2, result)
