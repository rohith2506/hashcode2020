import pdb
import os
from pprint import pprint
import math
from random import shuffle, randrange, randint

class Book:
    def __init__(self, book_id, score):
        self.book_id = book_id
        self.score = score

class Library:
    def __init__(self):
        self.library_dict = {}

    def assign_library_content(self, library_id, num_books, signup_time, max_books_to_ship, books, total_days):
        books.sort(key=lambda x: x.score, reverse=True)
        self.library_dict[library_id] = [num_books, signup_time, max_books_to_ship, books]

class Output:
    def __init__(self):
        self.result = {}

    def generate_output(self, library_id, book_ids):
        self.result[library_id] = book_ids

def get_initial_solution(library_dict):
    return sorted(library_dict.items(), key=lambda v:v[1][1])

def get_neighbour(library_dict):
    i1, i2 = randrange(len(library_dict)), randrange(len(library_dict))
    library_dict[i1], library_dict[i2] = library_dict[i2], library_dict[i1]
    return library_dict

def total_score(result, book_dict):
    score = 0
    for key, value in result.items():
        score = score + sum(book_dict[v.book_id] for v in value)
    return score

def get_result(library_dict, total_days, book_dict):
    days_remaining = total_days
    o = Output()
    for library_id, value in library_dict:
        num_books, signup_time, max_books_to_ship, books  = value
        if days_remaining < signup_time: break
        processed_books = books[0 : min(len(books), (total_days - signup_time) * max_books_to_ship)]
        if processed_books:
            o.generate_output(library_id, processed_books)
        days_remaining = days_remaining - signup_time
    return total_score(o.result, book_dict), o.result

def acceptance_prob(cur, new, temp):
    if new > cur: return 1.0
    return math.exp((new - cur) / temp)

def solve(library_dict, total_days, book_dict):
    current = get_initial_solution(library_dict)
    library_dict = current
    temperature, cooling_rate, best_score = 1000, 0.003, 0
    while temperature > 1:
        neighbour = get_neighbour(library_dict)
        cur_energy, result1 = get_result(current, total_days, book_dict)
        neighbour_energy, result2 = get_result(neighbour, total_days, book_dict)
        if acceptance_prob(cur_energy, neighbour_energy, temperature) > randint(0, 1):
            current = neighbour
        score, result = get_result(current, total_days,  book_dict)
        if score > best_score:
            best_score = score
            best_result = result
        temperature = temperature *  (1 - cooling_rate)
    return best_result, total_score(result, book_dict)

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

    book_dict = {}
    for book in books:
        book_dict[book.book_id] = book.score

    return  l, total_days, book_dict

def write_to_file(result, file_name):
    open(file_name, "w").close()
    ofile = open(file_name, "a")
    total_libraries = len(result.items())
    ofile.write(str(total_libraries) + "\n")
    for library_id, books in result.items():
        ofile.write(str(library_id) + " " + str(len(books)) + "\n")
        book_id_str = " " .join(str(book.book_id) for book in books)
        book_id_str = book_id_str.strip()
        ofile.write(book_id_str + "\n")
    ofile.close()

if __name__ == "__main__":
    files = os.listdir("data")
    print(files)
    total = 0
    for file_name in files:
        print("processing file: " + file_name)
        library, total_days, book_dict = read_input("data/" + file_name)
        result, score = solve(library.library_dict, total_days, book_dict)
        write_to_file(result, "output5/" + file_name)
        total = total + score
        print("Done. Total score so far: %d\n", total)
        print("###################")
