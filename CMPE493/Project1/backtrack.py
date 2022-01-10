from termcolor import colored
import copy

def eventPrint(operations, alg):
    print("{} edit distance actions are listed below:".format(alg))
    print("Total action count = {}\n".format(len(operations)))

    for op in operations:
        print("\t- {}".format(op))
    print()


def backtrack(alg, dataMatrix, dim1, dim2, word1, word2, result):

    ops = [] # Events which are either an insertion, a deletion, a substitution, or a replacement.
    pathMatrix = copy.deepcopy(dataMatrix) # To store the colored path, I've hold a path matrix.
    currentPoint = dataMatrix[dim1][dim2]
    cLat, cLon = dim1, dim2 # cLat and cLon are currentLatitude and currentLongitude
    while True:
        if cLat == 0 and cLon == 0: # Exit condition
            pathMatrix[cLat][cLon] = colored(dataMatrix[0][0], "cyan", attrs=["bold"])
            break
        if cLat > 0 and cLon > 0:
            diag = dataMatrix[cLat-1][cLon-1] # Diagonal value of current position
            insertion = dataMatrix[cLat][cLon-1] # Upper value of current position
            deletion = dataMatrix[cLat-1][cLon] # Left value of current position
            # If algorithm is Damerau-Levenshtein, "substitution" event can happen.
            if alg == "Damerau-Levenshtein":
                # check for primary conditions
                if dataMatrix[cLat - 2][cLon - 2] < min(diag, insertion, deletion):
                    # check for remaining conditions
                    # word1[cLat - 1] != word2[cLon - 1] and 
                    # word1[cLat - 1] == word2[cLon - 2] and 
                    # word1[cLat - 2] == word2[cLon - 1] is 
                    # a condition for subsequent unique two 
                    # characters that occurs at a reversed 
                    # pattern at each word. e.g. "ab" and "ba" 
                    if cLat > 2 and cLon > 2 and word1[cLat - 1] != word2[cLon - 1] and word1[cLat - 1] == word2[cLon - 2] and word1[cLat - 2] == word2[cLon - 1]:
                        ops.append("substitution between {} and {}".format(colored(word1[cLat-1], "red", attrs=["bold"]), colored(word2[cLon-1], "red", attrs=["bold"])))
                        pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"]) # setting the path as colored
                        pathMatrix[cLat-1][cLon-1] = colored(dataMatrix[cLat-1][cLon-1], "cyan", attrs=["bold"]) # setting the path as colored
                        currentPoint = dataMatrix[cLat - 2][cLon - 2] # setting new position with new latitude and longitude
                        cLat, cLon = cLat - 2, cLon - 2 # setting new latitude and longitude
                        continue
            # it checks the replacement
            # first since it brings the 
            # current position more
            # closer than the other two 
            # events.
            if diag < currentPoint:
                ops.append("replacement of {} with {}".format(colored(word1[cLat-1], "red", attrs=["bold"]), colored(word2[cLon-1], "red", attrs=["bold"])))
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                currentPoint = diag # setting the new value
                cLat, cLon = cLat-1, cLon-1 # setting the new position
                continue
            # if replacement isn't valid,
            # it checks insertion and deletion
            # subsequently.
            if insertion < currentPoint:
                ops.append("insertion of {}".format(colored(word2[cLon-1], "red", attrs=["bold"])))
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                currentPoint = insertion # setting the new value
                cLat, cLon = cLat, cLon - 1 # setting the new position
                continue
            # check for deletion operation
            if deletion < currentPoint:
                ops.append("deletion of {}".format(colored(word1[cLat-1], "red", attrs=["bold"])))
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                currentPoint = deletion # setting the new value
                cLat, cLon = cLat - 1, cLon # setting the new position
                continue
            # if all operations are invalid,
            # it checks for equality option
            # where at this position, both words
            # have the same letter. If so, it 
            # continues from the diagonal,
            # but no operations are done since 
            # it is meaningless to apply cost on 
            # an operation where character ¶ 
            # turns into character ¶.
            if diag == currentPoint:
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                cLat, cLon = cLat - 1, cLon -1 # setting the new position
                continue
        else:
            # if the algorithm reaches out the borders
            # these control statements are designed to
            # direct the position to the final position of
            # the algorithm, which is the starting point of
            # the edit distance table, [0,0]
            if cLat == 0:
                # if latitude is 0, it means no character
                # to insert, thus only deletion is available.
                ops.append("insertion of {}".format(colored(word2[cLon-1], "red", attrs=["bold"])))
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                cLon = cLon - 1 # setting the new longitude
            else:
                # if latitude is not 0, it means longitude is 0
                # since the code doesn't enter the exit condition block 
                # and it can only be a insertion operation.
                ops.append("deletion of {}".format(colored(word1[cLat-1], "red", attrs=["bold"])))
                pathMatrix[cLat][cLon] = colored(dataMatrix[cLat][cLon], "cyan", attrs=["bold"])
                cLat = cLat - 1 # setting the new latitude

    # printing the output of the task
    print("{} edit distance between {} and {} = {}\n".format(
        colored(alg, "yellow", attrs=["bold"]), 
        colored(word1, "green", attrs=["reverse"]), 
        colored(word2, "green", attrs=["reverse"]), 
        colored(result, "red", attrs=["bold"])
    ))

    # since backtracking stores the events in a reversed manner,
    # a reversal of the eventlist would be the corrent sequence of events.
    ops.reverse()
    # printing the events
    eventPrint(ops, alg)

    print("The {} Edit Distance Table:\n".format(colored(alg, "red", attrs=["bold"])))

    # visually enhanced edit distance table is printed here.
    maxDim = len(str(dim1 * dim2))
    for lat in range(dim1):
        for lon in range(dim2):
            # calculates the length of 
            # the greatest integer in 
            # the table and organizes 
            # the table based on that information.
            print(pathMatrix[lat+1][lon+1], end=" "*(maxDim - len(str(dataMatrix[lat][lon]))))
        print()
    print()
