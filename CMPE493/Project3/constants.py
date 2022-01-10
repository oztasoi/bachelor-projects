'''
url: head -> link href="https://www.goodreads.com/en/book/show/([\w|\W]+)?".*?>
book title: div class="leftContainer" -> div id="metacol" -> h1 id="bookTitle"
    - regex: <div class\=\"leftContainer\".*>[\w\W]+<div id\=\"metacol\".*>[\w\W]+<h1 id\=\"bookTitle\".*>([\w\W]+)?<\/h1>[\w\W]+<\/div>[\w\W]+<\/div>
book authors: div class="leftContainer" -> div id="metacol" -> div id="bookAuthors" -> span itemprop="author" -> div class="authorName__container" -> span itemprop="name"
    - regex: <div class\=\'authorName__container\'>([\w\W]+?)<\/div>
book description: div class="leftContainer" -> div id="metacol" -> div id="descriptionContainer" -> div id="description" -> span id="freeText" -> all <br>s
    - regex: <div class\=\"leftContainer\".*>[\w\W]+<div id\=\"metacol\".*>[\w\W]+<div id\=\"descriptionContainer\".*>[\w\W]+<div id\=\"description\".*>[\w\W]+<span id\=\"freeText\d*\".*>([\w\W]+)?<\/span>[\w\W]+<\/div>[\w\W]+<\/div>[\w\W]+<\/div>[\w\W]+<\/div>
genres: div class="rightContainer" -> div class="bigBoxContent containerWithHeaderContent" -> div class="left" -> a class="actionLinkLite bookPageGenreLink" between tags
    - regex: <div class\=\"bigBoxContent containerWithHeaderContent\".*?>([\w\W]+?)<\/div>
url of all recommended books: div class="carouselRow" -> ul
    - regex: <div class\=\"rightContainer\".*?>[\w\W]*?<div class\=\'carouselRow\'.*?>([\w\W]+?)<\/div>[\w\W]*?<\/div>
'''

BOOK_TITLE_REGEX = "<div class\=\"leftContainer\".*>[\w\W]+<div id\=\"metacol\".*>[\w\W]+<h1 id\=\"bookTitle\".*>([\w\W]+)?<\/h1>[\w\W]+<\/div>[\w\W]+<\/div>"
BOOK_AUTHORS_REGEX = "<div class\=\'authorName__container\'>([\w\W]+?)<\/div>"
AUTHOR_NAME_REGEX = "<span.*?>([^\(\)]+?)<\/span>"
BOOK_DESCRIPTION_REGEX = "<div class\=\"leftContainer\".*>[\w\W]*?<div id\=\"metacol\".*>[\w\W]*?<div id\=\"descriptionContainer\".*>[\w\W]*?<div id\=\"description\".*>[\w\W]*?<span id\=\"freeTextContainer\d*\".*?>([\w\W]+?)<\/span>[\w\W]+?<span id\=\"freeText\d*\".*?>([\w\W]+?)<\/span>[\w\W]*?<\/div>[\w\W]*?<\/div>[\w\W]*?<\/div>[\w\W]*?<\/div>"
DESCRIPTION_TOKEN_REGEX = "<br \/>"
GENRE_NAME_REGEX = "<div class\=\"left\".*?>[\w\W]*?<a.*?>([\w\W]+?)<\/a>[\w\W]*?<\/div>"
GENRE_VOTE_REGEX = "<div class\=\"right\".*?>[\w\W]*?<a.*?>([\w\W]+?) users<\/a>[\w\W]*?<\/div>"
RECOMMENDED_BOOKS_REGEX = "<div class='carouselRow'.*?>\n<ul>([\w\W]+?)<\/ul>\n<\/div>"
BOOK_URL_NAME_REGEX = "<a href\=\"([\w\W]+?)\"><img alt\=\"([\w\W]+?)\" src\=\".*?\" \/>"

TAG_REGEX_LIST = ["<a[\w\W]+?>[\w\W]+?<\/a>"]
# To remove any unnecessary unicode characters before tf-idf analysis, I've 
# used the regex below.
UNICODE_CHARACTER_REGEX = u"(\u2018|\u2019|\u2014)"
# To remove any unwanted html tag inside description or title, I've used the
# regex below to remove them.
XML_TAG_REGEX = ["<[\w\W]+?>"]
# To remove punctuations inside the documents which are encoded as HTML values,
# I've used the regex below to omit them.
HTML_PUNCTUATION_REGEX = "&[#\w]+?;"
