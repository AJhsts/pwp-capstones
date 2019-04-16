class User(object):
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, new_email):
        self.email = new_email
        print("User {}'s email has been updated to {}".format(self.name, self.email))

    def __repr__(self):
        return("User: {}, with email: {}, has {} books read".format(self.name, self.email, len(self.books)))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        self.books[book] = rating


    def get_average_rating(self):
        book_count = 0
        rtng_total = 0
        for rtng in self.books.values():
            if rtng:
                book_count += 1
                rtng_total += rtng
                avrtng = rtng_total / book_count
        return avrtng


class Book(object):

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("ISBN for {title} has been updated".format(title=self.title))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False


class Fiction(Book):

    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return("{} by {}".format(self.title, self.author))


class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return("{}, a {} manual on {}".format(self.title, self.level, self.subject))


class TomeRater(object):

    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        new_book = Book(title, isbn)
        return new_book

    def create_novel(self, title, author, isbn):
        new_novel = Fiction(title, author, isbn)
        return new_novel

    def create_non_fiction(self, title, subject, level, isbn):
        new_non_fiction = Non_Fiction(title, subject, level, isbn)
        return new_non_fiction

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print("No user with e-mail {email}!".format(email=email))
        else:
            self.users[email].read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
    
    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("User already exists.")
        else:
            user = User(name, email)
            self.users[email] = user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        most_read = None
        num_read = 0
        return max(self.books, key=lambda key: self.books[key])

    def highest_rated_book(self):
        highest_rated = None
        highest_rating = 0
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > highest_rating:
                highest_rated = book 
                highest_rating = rating
        return highest_rated

    def most_positive_user(self):
        for user in self.users.values():
            avg_user_rating = user.get_average_rating()
            if avg_user_rating > highest_rating:
                positive_user = user
                highest_rating = avg_user_rating
        return positive_user

    def get_n_most_read_books(self, n):
        sorted_by_value = sorted(self.books.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_by_value[0:n]

    def get_n_most_prolific_readers(self, n):
        readers = []
        for email in self.users:
            books_read = len(self.users[email].books)
            readers.append((books_read, email))
        readers.sort(reverse=True)

        if n > len(readers):
            n = len(readers)

        result = []
        for i in range(n):
            result.append(self.users[readers[i][1]])
        return result

    def get_n_most_expensive_books(self, n):
        most_expensive_books = []
        for book in self.books.keys():
            most_expensive_books.append((book.price, book))
        most_expensive_books.sort(reverse=True)

        if n > len(most_expensive_books):
            n = len(most_expensive_books)

        return most_expensive_books[0:n]

    def get_worth_of_user(self, user_email):
        total_worth = 0
        user = self.users[user_email]        

        for book in user.books:
            total_worth += book.price
        return "Total price of books"