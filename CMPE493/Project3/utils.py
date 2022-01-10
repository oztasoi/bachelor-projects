import re
import string
import unicodedata
from constants import *

def fix_url(url):
    '''
    - To avoid unmatching urls, this ensures
    the integrity of the url which belongs to
    Goodreads website.
    '''
    if "en/" in url:
        return str(url).strip()
    common_part = "https://www.goodreads.com/"
    tokens = str(url).split(common_part)
    return common_part + "en/" + tokens[1].strip()

def read_book_urls(path):
    '''
    - Reads book urls from a file and fixes them
    by checking whether or not they have "en/" within
    them and adds if necessary.
    '''
    f = open(path, "r")
    url_list = f.readlines()
    f.close()
    url_list = [fix_url(url) for url in url_list]
    return url_list

def omit_xml_tags(_string):
    '''
    - Omits XML/HTML tags inside a string given as
    parameter.
    '''
    current_form = _string
    for regx in XML_TAG_REGEX:
        current_form = re.sub(regx, " ", current_form)
    return current_form

def find_mbedded_links(_string):
    '''
    - Omits embedded links inside a string given as
    parameter.
    '''
    current_form = _string
    for regx in TAG_REGEX_LIST:
        current_form = re.sub(regx, " ", current_form)
    return current_form

def omit_unicode_chars(_string):
    '''
    - Omits unicode encoded characters in a string
    given as parameter.
    '''
    current_form = _string
    current_form = re.sub(f"{UNICODE_CHARACTER_REGEX}", " ", current_form)
    return current_form

def omit_html_punctuation(_string):
    '''
    - Omits HTML punctuation characters ina string
    given as parameter.
    '''
    return re.sub(HTML_PUNCTUATION_REGEX, " ", _string)

def omit_unnecessary_characters(_string):
    '''
    - Combines HTML and Unicode character omitting
    operation into one sequence.
    '''
    current_form = omit_html_punctuation(_string)
    final_form = omit_unicode_chars(current_form)
    return final_form

def get_book_title(book_page_data):
    '''
    - Extracts the title information from a book page data
    given as HTML by searching the `BOOK_TITLE_REGEX` pattern.
    It also does refining.
    '''
    match_list = re.finditer(BOOK_TITLE_REGEX, book_page_data)
    for match in match_list:
        raw_title = match.group(1).strip()
        raw_title = omit_unnecessary_characters(raw_title)
        return raw_title

def get_book_authors(book_page_data):
    '''
    - Extracts the author information from a book page data
    given as HTML by searching the `BOOK_AUTHORS_REGEX` pattern.
    '''
    match_list = re.finditer(BOOK_AUTHORS_REGEX, book_page_data)
    author_list = []
    for match in match_list:
        name_match_list = re.finditer(AUTHOR_NAME_REGEX, str(match.group(1)))
        for name in name_match_list:
            author_list.append(name.group(1).strip())
    return author_list

def get_book_description(book_page_data):
    '''
    - Extracts the description from a book page data
    given as HTML by searching the `BOOK_DESCRIPTION_REGEX` pattern.
    It also does refining of punctuations, special characters,
    XML/HTML tags and more along with extracting the maximum 
    information possible.
    '''
    match_list = re.findall(BOOK_DESCRIPTION_REGEX, book_page_data)
    description_list = []
    try:
        for match in list(match_list[0]):
            raw_description = match.strip()
            raw_description = omit_xml_tags(raw_description)
            raw_description = find_mbedded_links(raw_description)
            raw_description = omit_unnecessary_characters(raw_description)
            description_list.append(raw_description)
        if description_list[0][:10] not in description_list[1]:
            return description_list[0]
        else:
            return description_list[1]
    except:
        return ""

def get_genre_info(book_page_data):
    '''
    - Extracts the genre information from a book page data
    given as HTML by searching the `GENRE_NAME_REGEX` and
    `GENRE_VOTE_REGEX` pattern.
    '''
    name_match_list = re.findall(GENRE_NAME_REGEX, book_page_data)
    vote_match_list = re.findall(GENRE_VOTE_REGEX, book_page_data)
    genre_vote_obj = {}
    for name, vote in zip(name_match_list, vote_match_list):
        if name in genre_vote_obj.keys():
            genre_vote_obj[name] += int(vote.replace(",", ""))
        else:
            genre_vote_obj[name] = int(vote.replace(",", ""))
    return genre_vote_obj

def get_recommended_books(book_page_data):
    '''
    - Extracts the recommendation information done by Goodreads
    itself from a book page data given as HTML by searching the
    `RECOMMENDED_BOOKS_REGEX` pattern. It also does refining with
    `BOOK_URL_NAME_REGEX`.
    '''
    raw_recommended_books = re.findall(RECOMMENDED_BOOKS_REGEX, book_page_data)[0]
    recommmended_book_list = re.findall(BOOK_URL_NAME_REGEX, raw_recommended_books)
    recommended_book_urls = list(zip(*recommmended_book_list))[0]
    recommended_book_names = list(zip(*recommmended_book_list))[1]
    recommended_book_info_obj = {}
    for ix, (url, name) in enumerate(zip(recommended_book_urls, recommended_book_names)):
        name = omit_unnecessary_characters(name)
        recommended_book_info_obj[ix] = { "name": name, "url": fix_url(url) }
    return recommended_book_info_obj

def clearPunc(_string):
    '''
    - Clears any punctuation if necessary.
    '''
    non_punc_string = str(_string).translate(str.maketrans(string.punctuation, " "*len(string.punctuation)))
    return non_punc_string

def processed_string(_string):
    '''
    - Splits the given string with respect to whitespace
    and make them lowercase while stripping any remaining
    whitespaces.
    '''
    current_form = clearPunc(_string)
    tokens = str(current_form).split()
    trimmed_tokens = []
    for token in tokens:
        trimmed_tokens.append(str(token).strip().lower())
    return trimmed_tokens
