# <span style="color:red">CMPE 493: Introduction to Information Retrieval Fall 2020</span>
# <span style="color:orange">Report for Assignment 2</span>

## <span style="color:green">Introduction: </span>
This project has been given to me to understand and comprehend single word search in a dataset and a prefix search within the given data set.

## <span style="color:green">How To Run: </span>
To run the program, CLI is needed and one external library have been utilized to achieve the output with a greater user experience.

Version & Platform: <span style="color:yellow">3.8.6 (64-bit)</span>

## <span style="color:red">BEWARE:</span> The program takes ~4.5 seconds for 1000 articles. Waiting interval is approximately 100-105 seconds for preprocessing. The loading bar will guide your perspective through the preprocessing.

## <span style="color:orange">An example usage of the running sequence:</span>
### - First, preprocess the data:
### OPTIONAL: If you put reuters21578 directory in a different location than the same location with the code, specify it in environment variables as follows and start preprocessing.
```bash
export REUTERS_DIR="<path_to_reuters21578_dir>
```

```bash
python3 prep.py
```

### - After then, run the inquiry tool
```bash
python3 query.py
```

## <span style="color:orange">Steps of preprocessing:</span>

- Firstly, I've created many functions in `utils.py` file to help me process the data set.
- After the implementation of the utility functions, I've started to create my `regular expressions` to retrieve the necessary data in the data set.
- Then, I've retrieved each `REUTER` article via `ARTICLE_REGEX` in `constants.py` and stored them in a list.
- Furthermore, article ID retrieval, title data retrieval, body data retrieval operations are executed consecutively.
- Henceforth, I've unfolded and trimmed the title and body data separately, before I've merged those two into one pure data list and tokenized the pure data.
- Thus, I've applied case-folding, stopword-removal, punctuation-removal and one more tokenization operation to retrieve the string tokens within the previously punctuated data.
- Finally, I've filled my inverted index dictionary and trie dictionary with the final form of the data.
- When every article is processed, I've dumped the inverted index dictionary and trie dictionary into separate JSON files to use in inquiries.

## <span style="color:orange">Data Structure I've Used for Inverted Index:</span>

- I've used a dictionary to hold both the document ids and frequency of the word in that document.
- My inverted index documentation is examplified as below:
    - { `<word1>`: { `docId1`: freq, `docId2`: freq, ... }, `<word2>`: { `docId`: freq }, `docId2`: freq, ... }, ... }
- My inverted index structure is implemented as follows:
    -
    ```python
    inv_dict = {}
    def indexification(content, new_id):
    '''
    Creates a dictionary where first layer keys
    are all of the occuring words in whole articles
    and second layer keys are all of the occuring 
    article ids of that word, and its value is the
    frequency of that word in that article.
    - ess is my own abbreviation of essence as word.
    '''
    for ess in content:
        if ess not in inv_dict.keys():
            inv_dict[ess] = { new_id: 1 }
        else:
            if new_id not in inv_dict[ess].keys():
                currentState = inv_dict[ess]
                currentState[new_id] = 1
                inv_dict[ess] = currentState
            else:
                inv_dict[ess][new_id] += 1
    ```

## <span style="color:orange">Data Structure I've Used for Trie:</span>

- I've used a dictionary to hold the characters of the words as one trie node and each key of the dictionary represents the next child that can be reached from the current node.
- My trie is implemented as follows:
    - 
    ```python
    trie = {}
    def triefication(content):
    '''
    Creates a dictionary of recursive dictionaries
    where each key is a char and its value is either
    an empty dict when that key character is the last
    character of a word or a dict which contains chars
    as keys and their values as key-value pairs.
    - ess is my own abbreviation of essence as word.
    '''
    for ess in content:
        current_pos = trie
        for char in ess:
            if char not in current_pos.keys():
                current_pos[char] = {}
            current_pos = current_pos[char]
    ```
