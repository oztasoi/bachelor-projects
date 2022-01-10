import copy
import json
import math
from typing import final
import urllib.request

from utils import *
from datetime import datetime
from collections import defaultdict


class Library:
    def __init__(self, rel_count, isDev=True):
        '''
        - Initialization function of the library instance.
        It sets many dictionaries to be used in many purposes.
        P.S.: `ix` used as index and for map dictionaries,
        first indicator is always the key, and second is value.
        e.g. self.book_ix_url_map is a dict with indexes as keys,
        and urls as values.
        '''
        self.env_dev = isDev
        self.prod_dir = "./books"
        self.test_dir = "./test_books"
        self.relevant_count = rel_count
        self.total_number_of_books = 0
        self.last_state = None
        self.alpha = 0.5
        self.book_is_added = defaultdict(bool)
        self.book_ix_url_map = defaultdict(str)
        self.book_url_ix_map = defaultdict(int)
        self.book_ix_genre_map = defaultdict(str)
        self.book_genre_ix_map = defaultdict(int)
        self.desc_dict = defaultdict(int)
        self.desc_corpus = defaultdict(dict)
        self.desc_tf_idf = defaultdict(dict)
        self.genre_dict = defaultdict(int)
        self.genre_corpus = defaultdict(dict)
        self.genre_tf_idf = defaultdict(dict)
        self.last_query_scores = defaultdict(dict)

    def load_booklist(self, path):
        '''
        - Loads the given booklist by the user into the system and
        calculates their tf-idf values.
        '''
        url_list = read_book_urls(path)
        for url in url_list:
            downloaded_book = self.download_a_book(url)
            self.add_to_library(downloaded_book)
        print("\r\n--> Books in the given list has been added.")
        self.calculate_tf_idf()
        print("--> Calculations have been completed.")
        self.dump_resources()
        print("--> All resources have been dumped.")

    def dump_resources(self):
        '''
        - Exports the current state of the library to a file to be
        imported whenever necessary.
        '''
        fout = open("resources.json", "w")

        current_datetime = datetime.utcnow()

        resources = {}
        resources["rel_count"] = copy.deepcopy(self.relevant_count)
        resources["total_books"] = copy.deepcopy(self.total_number_of_books)
        resources["book_is_added"] = copy.deepcopy(self.book_is_added)
        resources["book_ix_url_map"] = copy.deepcopy(self.book_ix_url_map)
        resources["book_url_ix_map"] = copy.deepcopy(self.book_url_ix_map)
        resources["book_ix_genre_map"] = copy.deepcopy(self.book_ix_genre_map)
        resources["book_genre_ix_map"] = copy.deepcopy(self.book_genre_ix_map)
        resources["desc_dict"] = copy.deepcopy(self.desc_dict)
        resources["desc_corpus"] = copy.deepcopy(self.desc_corpus)
        resources["desc_tf_idf"] = copy.deepcopy(self.desc_tf_idf)
        resources["genre_dict"] = copy.deepcopy(self.genre_dict)
        resources["genre_corpus"] = copy.deepcopy(self.genre_corpus)
        resources["genre_tf_idf"] = copy.deepcopy(self.genre_tf_idf)
        resources["last_state"] = copy.deepcopy(str(current_datetime))
        resources["last_query"] = copy.deepcopy(self.last_query_scores)

        json.dump(resources, fout)
        fout.flush()
        fout.close()
        print(f"--> System screenshot is taken at {current_datetime}")
        del resources

    def load_resources(self):
        '''
        - Import a system state screenshot to the system whenever desired.
        '''
        fin = open("resources.json", "r")

        imported_resources = json.load(fin)
        fin.close()
        self.relevant_count = imported_resources["rel_count"]
        self.total_number_of_books = imported_resources["total_books"]
        self.book_is_added = imported_resources["book_is_added"]
        self.book_ix_url_map = imported_resources["book_ix_url_map"]
        self.book_url_ix_map = imported_resources["book_url_ix_map"]
        self.book_ix_genre_map = imported_resources["book_ix_genre_map"]
        self.book_genre_ix_map = imported_resources["book_genre_ix_map"]
        self.desc_dict = imported_resources["desc_dict"]
        self.desc_corpus = imported_resources["desc_corpus"]
        self.desc_tf_idf = imported_resources["desc_tf_idf"]
        self.genre_dict = imported_resources["genre_dict"]
        self.genre_corpus = imported_resources["genre_corpus"]
        self.genre_tf_idf = imported_resources["genre_tf_idf"]
        self.last_state = imported_resources["last_state"]
        self.last_query_scores = imported_resources["last_query"]

    def add_to_library(self, _book):
        '''
        - Adds a book to the library, which means many dictionaries
        e.g. corpus, dictionary and maps. If a book is not downloaded
        before, it also downloads it.
        '''
        if isinstance(_book, Book):
            book = _book
        else:
            if _book in set(self.book_url_ix_map.keys()):
                print("--> This book is already added.")
                return
            else:
                book = self.download_a_book(_book)

        desc = book.book_description
        genre = book.book_genre_info
        tokens = processed_string(desc)
        unique_words = set(tokens)
        word_counts = defaultdict(int)

        # Indicator of document frequency.
        for uniq in unique_words:
            self.desc_dict[uniq] += 1

        # Indicator of term frequency.
        for word in tokens:
            word_counts[word] += 1

        # Processes the genre information of the current book.
        self.add_genre_info(genre, book.book_ix)
        # Adds the book to the necessary maps to make it
        # available in future time.
        self.desc_corpus[book.book_ix] = word_counts
        self.book_url_ix_map[book.book_url] = book.book_ix
        self.book_ix_url_map[str(book.book_ix)] = book.book_url
        self.book_is_added[str(book.book_ix)] = True

    def add_genre_info(self, genre_dict, book_ix):
        '''
        - Extracts the genre information by firstly making them
        lowercase than calculating their term frequency and
        document frequency. It checks for same genre as different
        instances in the book and accumulates them.
        '''
        lowered_dict = {}
        for genre, genreval in genre_dict.items():
            key = str(genre).lower()
            lowered_dict[key] = genreval

        uniq_genres = set(list(lowered_dict.keys()))
        genre_counts = defaultdict(int)

        for uniq in uniq_genres:
            self.genre_dict[uniq] += lowered_dict[uniq]

        for genre in lowered_dict.keys():
            genre_counts[genre] += lowered_dict[genre]

        self.genre_corpus[book_ix] = genre_counts

    def compose_a_query(self, selection, data):
        '''
        - Understands the query and returns the appropriate answer to
        the console. It supports single book query and multiple book
        query. For multiple book query, put the links into a file and
        type the filepath into the console. For further information,
        check the `help` function or README-REPORT.md file in project.
        '''
        if selection == "single":
            relevance_results, book_ix = self.query_a_book(data)
            precision, cumulative_match_ratio = self.calculate_query_statistics(book_ix, relevance_results)
            query_result_obj = { book_ix: { "relevances": relevance_results, "precision": precision, "avg_pre": cumulative_match_ratio } }
            self.display_query_results(query_result_obj)
        elif selection == "multiple":
            lines = read_book_urls(data)
            urls = [fix_url(url) for url in lines]
            query_results_obj = {}

            for url in urls:
                relevance_results, book_ix = self.query_a_book(url)
                precision, cumulative_match_ratio = self.calculate_query_statistics(book_ix, relevance_results)
                query_result_obj = { "relevances": relevance_results, "precision": precision, "avg_pre": cumulative_match_ratio }
                query_results_obj[book_ix] = query_result_obj

            self.display_query_results(query_results_obj)
        else:
            print("Invalid query form. Try again!")

    def query_a_book(self, book_url):
        '''
        - It queries a book by comparing its cosine similarity values
        with all other books in the library and returns the best
        matches to the console. It calculates query norm and document norm,
        then does dot product of a query and document pair, then finds the
        angle between them and maps them between 0 and 1.

        - for those variables which include "desc" or "d" string means it is
        related with the description of the book.
        - for those variables which include "genre" or "g" string means it is
        related with the genre information of the book.
        '''
        if book_url in set(self.book_url_ix_map.keys()):
            query_book_ix = str(self.book_url_ix_map[book_url])
            query_book_desc = self.desc_tf_idf[query_book_ix]
            query_book_genre = self.genre_tf_idf[query_book_ix]
        else:
            # Add clean url
            raw_book = self.download_a_book(fix_url(book_url))
            query_book_ix = raw_book.book_ix
            query_book_desc, query_book_genre = self.process_a_book(raw_book)

        scores = defaultdict(float)

        # Query vector norm part.
        qvec_desc_norm = 0.0
        qvec_genre_norm = 0.0
        for wval in query_book_desc.values():
            qvec_desc_norm += wval ** 2
        qvec_desc_norm = qvec_desc_norm ** 0.5

        for gval in query_book_genre.values():
            qvec_genre_norm += gval ** 2
        qvec_genre_norm = qvec_genre_norm ** 0.5

        for (dbook_ix, book_tf_idf), (gbook_ix, genre_tf_idf) in zip(self.desc_corpus.items(), self.genre_corpus.items()):

            if dbook_ix == query_book_ix:
                continue

            # Document vector norm part.
            dvec_desc_norm = 0
            dvec_genre_norm = 0
            for wval in book_tf_idf.values():
                dvec_desc_norm += wval ** 2
            dvec_desc_norm = dvec_desc_norm ** 0.5

            for gval in genre_tf_idf.values():
                dvec_genre_norm += gval ** 2
            dvec_genre_norm = dvec_genre_norm ** 0.5

            qword_set = set(query_book_desc.keys())
            dword_set = set(book_tf_idf.keys())
            # Finds the intersecting description between the query and the document
            desc_intersection = qword_set.intersection(dword_set)

            qgenre_set = set(query_book_genre.keys())
            dgenre_set = set(genre_tf_idf.keys())
            # Finds the intersecting genres between the query and the document
            genre_intersection = qgenre_set.intersection(dgenre_set)

            # Does dot product as in TF-IDF formula
            desc_dot_product = 0
            for iword in list(desc_intersection):
                desc_dot_product += query_book_desc[iword] * book_tf_idf[iword]

            # Does dot product as in TF-IDF formula
            genre_dot_product = 0
            for igenre in list(genre_intersection):
                genre_dot_product += query_book_genre[igenre] * genre_tf_idf[igenre]

            # Finds the angle between the query and the document for description 
            try:
                book_desc_rel_score = desc_dot_product / ( qvec_desc_norm * dvec_desc_norm )
            except ZeroDivisionError:
                book_desc_rel_score = 0.0

            # Finds the angle between the query and the document for genre information 
            try:
                book_genre_rel_score = genre_dot_product / ( qvec_genre_norm * dvec_genre_norm )
            except ZeroDivisionError:
                book_genre_rel_score = 0.0

            # Merges description and genre information values into one value
            scores[str(dbook_ix)] = (self.alpha * book_desc_rel_score) + ((1 - self.alpha) * book_genre_rel_score)

        # Deletes if the queried book itself is inside the documents.
        try:
            del scores[str(query_book_ix)]
        except:
            pass
        try:
            del scores[int(query_book_ix)]
        except:
            pass

        # Sorts the scores in ascending order.
        scores = dict(sorted(scores.items(), key=lambda score: score[1], reverse=True))
        self.last_query_scores = { "book_url": book_url, "scores": scores }
        # Returns the results and book index
        return list(scores.keys())[:self.relevant_count], query_book_ix

    def calculate_query_statistics(self, book_ix, relevance_results):
        '''
        - Calculates the precision and average precision values in the query
        as explained by the reference in the description.
        Reference link: http://sdsawtelle.github.io/blog/output/mean-average-precision-MAP-for-recommender-systems.html
        P.S.: Cumulative match ratio is written as average precision.
        '''
        rel_url_list = self.scan_book(book_ix)
        total_accurate_match = 0
        cumulative_match_ratio = 0.0
        for ix, _book_ix in enumerate(relevance_results):
            if str(_book_ix) == str(book_ix):
                continue
            book_url = str(self.book_ix_url_map[str(_book_ix)]).strip()
            if book_url in set(rel_url_list):
                total_accurate_match += 1
                cumulative_match_ratio += (total_accurate_match / (ix + 1))

        try:
            precision = total_accurate_match / len(relevance_results)
        except ZeroDivisionError:
            precision = 0.0
        try:
            cumulative_match_ratio = cumulative_match_ratio / total_accurate_match
        except ZeroDivisionError:
            cumulative_match_ratio = 0.0

        return precision, cumulative_match_ratio

    def remove_from_library(self, book_url):
        '''
        - Removes a book from the current library state with all the
        embedded information into the corpus and dictionary. For a
        stable state, the user should execute `recalibrate` command to
        get all TF-IDF values to be calculated again.

        P.S.: It may still have bugs, but it will be fixed as a future
        plan.
        '''
        if book_url not in set(self.book_url_ix_map.keys()):
            print("--> You cannot remove a book which is not added.")
            return

        book_ix = self.book_url_ix_map[book_url]
        if self.env_dev:
            fin = open(f"{self.test_dir}/{book_ix}.json", "r")
        else:
            fin = open(f"{self.prod_dir}/{book_ix}.json", "r")
        book_info = json.load(fin)
        fin.close()
        unique_tokens = set(processed_string(book_info["book_description"]))
        
        # remove dictionary occurences --> decreases document frequency
        for uniq in unique_tokens:
            self.desc_dict[uniq] = self.desc_dict[uniq] - 1

        # remove term frequency dictionary in this book
        del self.desc_corpus[str(book_ix)]
        del self.book_url_ix_map[book_url]
        del self.book_ix_url_map[str(book_ix)]
        del self.book_is_added[str(book_ix)]

        print(f"--> Book with ID: {book_ix} is deleted. System is out of sync.")
        print(f"--> You should recalibrate. Last system state date-time: {self.last_state}")

    def read_a_book(self, book_url):
        '''
        - Displays all information related to the book provided by Goodreads
        website. One can read a book's description and see its authors if one
        desires such a thing.
        '''
        if book_url not in set(self.book_url_ix_map.keys()):
            print("--> You cannot read a book which is not in the library.")
            return
        book_ix = self.book_url_ix_map[book_url]

        if self.env_dev:
            fin = open(f"{self.test_dir}/{book_ix}.json")
        else:
            fin = open(f"{self.prod_dir}/{book_ix}.json")

        book = json.load(fin)
        fin.close()
        book_title = book["book_title"]
        book_description = book["book_description"]
        book_authors = book["book_authors"]
        book_genre_info = book["book_genre_info"]

        print(f"Book Title:\t\t\t{book_title}")
        print(f"Book Authors:\t\t\t{book_authors}")
        print(f"Book Description:\t\t{book_description}")
        print(f"Book Genres:\t\t\t{book_genre_info}")

    def process_a_book(self, raw_book):
        '''
        - Calculates TF-IDF values of a book which is not added
        to the library beforehand. It brings agility to the application.

        P.S.: It may have minor bugs even though I do not think so.
        It will be verified in a future work.
        '''
        tokens = processed_string(raw_book.book_description)
        word_counts = defaultdict(int)
        genre_counts = defaultdict(int)
        desc_tf_idf_dict = defaultdict(float)
        genre_tf_idf_dict = defaultdict(float)
        for word in tokens:
            word_counts[word] += 1

        for word, freq in word_counts.items():
            try:
                desc_tf_idf_dict[word] = freq * math.log10(len(self.desc_corpus.keys())/self.desc_dict[word])
            except:
                desc_tf_idf_dict[word] = 0

        # Lowers the genre names
        lowered_dict = {}
        genre_dict = raw_book.book_genre_info
        for genre, genreval in genre_dict.items():
            lgenre = str(genre).lower()
            lowered_dict[lgenre] = genreval

        for genre, genreval in lowered_dict.items():
            genre_counts[genre] += genreval

        for genre, votes in genre_counts.items():
            try:
                genre_tf_idf_dict[genre] = votes * math.log10(len(self.genre_corpus.keys())/self.genre_dict[genre])
            except:
                genre_tf_idf_dict[genre] = 0

        return desc_tf_idf_dict, genre_tf_idf_dict

    def calculate_tf_idf(self):
        '''
        - Calculates TF-IDF values of all books provided at the
        initial state of the library. It calculates description
        and genre information TF-IDF values and registers them
        into several dictionaries to be used in further queries.
        '''
        N_DESC = len(self.desc_corpus.keys())
        N_GENRE = len(self.genre_corpus.keys())
        for book_ix, word_counts in self.desc_corpus.items():
            tf_idf_dict = defaultdict(float)
            for word, freq in word_counts.items():
                tf_idf_dict[word] = freq * math.log10(N_DESC/self.desc_dict[word])
            self.desc_tf_idf[str(book_ix)] = tf_idf_dict

        for book_ix, genre_counts in self.genre_corpus.items():
            tf_idf_dict = defaultdict(float)
            genre_sum = sum(genre_counts.values())
            for genre, votes in genre_counts.items():
                val = (votes/genre_sum) * math.log10(N_GENRE/self.genre_dict[genre])
                if val < 0:
                    val = val * -1
                tf_idf_dict[genre] = val

            self.genre_tf_idf[str(book_ix)] = tf_idf_dict

    def scan_book(self, book_ix):
        '''
        - Scans a book to extract recommendations for those who
        likes reading this book.
        '''
        if self.env_dev:
            fin = open(f"{self.test_dir}/{book_ix}.json", "r")
        else:
            fin = open(f"{self.prod_dir}/{book_ix}.json", "r")
        book = json.load(fin)
        fin.close()
        recommendations = book["book_recommendation_info"]
        rec_url_list = []
        for rec_obj in dict(recommendations).values():
            rec_url_list.append(rec_obj["url"])
        return rec_url_list

    def download_a_book(self, url):
        '''
        - Downloads the book from Goodreads website and creates
        a Book() instance to be used in further operations.
        Also, it exports the book information in a folder to be
        read by users of the Libraria.
        '''
        # Download the book page
        result = urllib.request.urlopen(url).read().decode("utf-8")
        # Increase the total number of books
        self.total_number_of_books += 1
        book_info = Book(result, self.total_number_of_books, url)
        if self.env_dev:
            book_info.dump_dict_json(self.test_dir)
        else:
            book_info.dump_dict_json(self.prod_dir)
        print(f"\rLast accessed url: {url}", end=" ")
        return book_info

    def display_query_results(self, query_result_obj):
        '''
        - Displays query results such as precision and average
        precision of the query made by a user along with a ranking
        of recommended books by my algorithms.
        '''
        for book_ix, query_result in dict(query_result_obj).items():
            precision = query_result["precision"]
            avg_pre = query_result["avg_pre"]
            relevances = query_result["relevances"]
            try:
                print(f"Query results for book url: {self.book_ix_url_map[book_ix]}")
            except:
                if self.env_dev:
                    fin = open(f"test_books/{book_ix}.json", "r")
                else:
                    fin = open(f"books/{book_ix}.json", "r")

                book = json.load(fin)
                fin.close()

                book_url = book["book_url"]
                print(f"Query results for book url: {book_url}")

            print(f"\tPrecision: {precision}")
            print(f"\tAverage Precision: {avg_pre}")
            print(f"\tRecommended book urls:")
            for rel in relevances:
                book_url = self.book_ix_url_map[rel]
                print(f"\t\tBook ID: {rel}\t Book Url: {book_url}")

    def display_last_query_scores(self):
        '''
        - Shows last query cosine similarity scores to the user.
        It is mainly used as development purposes, but any user can
        check the query values.
        '''
        print(self.last_query_scores)

class Book:
    def __init__(self, book_page_data, ix, url):
        '''
        - Book() class instance initialization function.
        Stores book index, url, title, authors, description, genre info
        and recommended books by Goodreads to be used in further operations.
        '''
        self.book_ix = ix
        self.book_url = url
        self.book_title = get_book_title(book_page_data)
        self.book_authors = get_book_authors(book_page_data)
        self.book_description = get_book_description(book_page_data)
        self.book_genre_info = get_genre_info(book_page_data)
        self.book_recommendation_info = get_recommended_books(book_page_data)

    def dump_dict(self):
        '''
        - Dumps the Book() instance to a dict object to be written into a file
        '''
        return {
            "book_id": self.book_ix,
            "book_url": self.book_url,
            "book_title": self.book_title,
            "book_authors": self.book_authors,
            "book_description": self.book_description,
            "book_genre_info": self.book_genre_info,
            "book_recommendation_info": self.book_recommendation_info
        }

    def dump_dict_json(self, path):
        '''
        - Exports a Book() instance to a JSON file to be used in further operations.
        '''
        book_dict = self.dump_dict()
        fjsonout = open(f"{path}/{self.book_ix}.json", "w")
        fjsonout.write(json.dumps(book_dict))
        fjsonout.flush()
        fjsonout.close()
