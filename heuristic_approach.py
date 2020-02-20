import pdb
import os
from pprint import pprint

class Book:
    def __init__(self, book_id, score):
        self.book_id = book_id
        self.score = score

class Library:
    def __init__(self):
        self.library_dict = {}

    def assign_library_content(self, library_id, num_books, signup_time, max_books_to_ship, books, total_days):
        self.library_dict[library_id] = [num_books, signup_time, max_books_to_ship, books]
        total_score = sum(book.score for book in books)
        scoring_value = ((((total_score * 1.0) / num_books) * max_books_to_ship) * 1.0 / signup_time)
        self.library_dict[library_id].append(scoring_value)

class Output:
    def __init__(self):
        self.result = {}

    def generate_output(self, library_id, book_ids):
        self.result[library_id] = book_ids


def solve(library_dict, total_days):
    # sort them by library sign up time

    sorted_library_dict = sorted(library_dict.items(), key = lambda value: value[1][-1], reverse = True)

    book_bucket = [[] for day in range(total_days)]
    visited_books = {}
    days_remaining = total_days
    o = Output()
    result = []

    for library_id, value in sorted_library_dict:
        num_books, signup_time, max_books_to_ship, books, scoring_value = value
        if days_remaining < signup_time: break
        day_bucket = book_bucket[signup_time]
        # sort the library books by their value
        books.sort(key=lambda x: x.score, reverse=True)
        processed_books = []
        for day in range(signup_time, total_days):
            day_bucket = book_bucket[day]
            for i in range(min(len(books), max_books_to_ship)):
                book = books[i]
                if book in visited_books: continue
                book_bucket[day].append(book)
                visited_books[book] = None
                processed_books.append(book.book_id)
            books = books[max_books_to_ship:]
        if processed_books:
            o.generate_output(library_id, processed_books)
        days_remaining = days_remaining - signup_time

    return o.result


def read_input(file_name):
    idx = 0
    lines = open(file_name, "r").readlines()
    total_books, total_libraries, total_days = list(map(int, lines[idx].strip().split()))
    idx = idx+1
    book_scores = list(map(int, lines[idx].strip().split()))
    idx = idx+1
    l = Library()
    books = []
    for i in range(len(book_scores)):
        books.append(Book(i, book_scores[i]))

    for library_id in range(total_libraries):
        num_books, signup_time, max_books_to_ship = list(map(int, lines[idx].strip().split()))
        idx = idx + 1
        library_book_ids = list(map(int, lines[idx].strip().split()))
        library_books = [books[library_book_id] for library_book_id in library_book_ids]
        idx = idx + 1
        l.assign_library_content(library_id, num_books, signup_time, max_books_to_ship, library_books, total_days)

    return  l, total_days

def write_to_file(result, file_name):
    open(file_name, "w").close()
    ofile = open(file_name, "a")
    total_libraries = len(result.items())
    ofile.write(str(total_libraries) + "\n")
    for library_id, books in result.items():
        ofile.write(str(library_id) + " " + str(len(books)) + "\n")
        book_id_str = " " .join(str(book_id) for book_id in books)
        book_id_str = book_id_str.strip()
        ofile.write(book_id_str + "\n")
    ofile.close()

if __name__ == "__main__":
    files = os.listdir("data")
    print(files)
    for file_name in files:
        print("processing file: " + file_name)
        library, total_days = read_input("data/" + file_name)
        result = solve(library.library_dict, total_days)
        write_to_file(result, "output4/" + file_name)
        print("Done")
        print("###################")
