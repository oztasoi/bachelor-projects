# <span style="color:red">CMPE 493: Introduction to Information Retrieval Fall 2020</span>
# <span style="color:orange">Report for Assignment 3</span>

## <span style="color:green">Introduction: Libraria</span>
This project has been given to me to understand and comprehend recommendation systems and the dynamics behind its engine with data crawling.

## <span style="color:green">How To Run: </span>
To run the program, CLI is needed and no external library have been utilized to achieve the output without a significant loss of user experience.

Version & Platform: <span style="color:yellow">3.8.6 (64-bit)</span>

### - After then, run the recommendation API
```bash
python3 main.py
```

## <span style="color:orange">Processing the Genres and Its Effect:</span>

- I am using TF-IDF model to analyze the effects of genres, which are selected by the community of Goodreads.
- I do not infer layered genres, which are redirections to the parent genre, but I count their values within their parent genre votings as supporting votes.
- When I am calculating tf-idf values of genres, I am scaling each of the votes with the total number of votes given by the Goodreads community for that specific book. `--> check model.py, Line 355`
- After that, there may occur negative values by when log value is taken since the votes of that genre in genre dictionary may excess the number of the books, therefore I've multiplied those negative values with -1 to see their actual effect in my recommendation system.
- After that, I've merged my genre cosine similarity value of the book that I've used to calculate description cosine similarity value with a constant alpha.
- The value alpha is the ratio of the description cosine similarity in the final similarity value.
    - ### FUTURE WORK: It can be integrated into a simple linear regression structure by comparing the similarity of the same book with different alpha values to find the highest similarity values for one book. By doing this to all books, I can further see optimal ratio of for each book I've crawled from and find an average alpha value which satisfies most of the similarity queries within the acceptable tolerance range.

## <span style="color:orange">Parameters of the models I've used:</span>

### For Description Similarity:
- I've set the number of recommended books as a changing parameter decided by the user to increase analysis power to a new level.
- Also, my model can be dumped as a state image, which stores all necessary information, tf-idf values, corpus, dictionary and all benevolent data which helps analyzing and displaying the results.
- In this project, I'd like to see the results with a dataset which does not omit the mostly used words in English, aka Stopwords, thus I did not remove them in my dataset. Also, I did not impose any threshold values with the same reasoning explained previously.

### For Genre Similarity:
- All points explained in description similarity holds for genre similarity as well.
- In addition to the current features, I am normalizing genre votes by dividing each of them to the summation of all votes for one book to make the values lay onto the values between the same range with the description tf-idf values.

## <span style="color:orange">Supported Features:</span>
- I support many features in my Libraria app to be used in different applications of book recommendations.
- List of commands I support for now:
    - `help`: Displays help.
    - `load <file_path>`: Loads the list of books, which are described as book urls.
    - `query single <book_url>`: Queries the single book and display statistics and recommendations.
    - `query multiple <file_path>`: Queries each book url in the file and displays statistics and recommendations.
    - `recalibrate`: Starts to update the books that are processed in the Libraria with the current downloaded books.
    - `add <book_url>`: Adds the book to the library with the given book url.
    - `remove <book_url>`: Removes the book from the downloaded books and asks you to select if you want to recalibrate after removal.
    - `look <book_url>`: Displays the book to the screen and shows the contents of the book.
    - `exit`: Terminates the Libraria.

