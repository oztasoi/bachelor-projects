import os

'''
Constants that are used in the project.
REUTERS_DIR => path of the directory where reuters21578 folder exists
ENCODING => encoding of the article files
NEWID_REGEX => regular expression to find article ids
ARTICLE_REGES => regular expression to find articles in the article files
TITLE_REGES => regular expression to find the title in an article
BODY_REGES => regular expression to find the body in an article
TITLE_TAGS => List of enclosing tags that surrounds title information
BODY_TAGS => List of enclosing tags that surrounds body information
'''
REUTERS_DIR = os.getenv("REUTERS_DIR") or "."
ENCODING = "latin-1"

NEWID_REGEX = 'NEWID="(\d+)"'
ARTICLE_REGEX = '<REUTERS.*>(\w|\W)+?<\/REUTERS>'
BODY_REGEX = '<BODY>([\w\W]+?)<\/BODY>'
TITLE_REGEX = '<TITLE>([\w\W]+?)<\/TITLE>'

TITLE_TAGS = ["<TITLE>", "</TITLE>"]
BODY_TAGS = ["<BODY>", "</BODY>"]
