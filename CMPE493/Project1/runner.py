import sys
from damerau import damerauLevenshtein
from levenshtein import levenshtein

def main():
    _word1 = sys.argv[1] # first word
    _word2 = sys.argv[2] # second word

    print("*" * 80) # visual upgrade
    # Damerau-Levenshtein Edit Distance
    damerauLevenshtein(_word1, _word2)
    print("*" * 80) # visual upgrade
    # Levenshtein Edit Distance
    levenshtein(_word1, _word2)
    print("*" * 80) # visual upgrade

main()
