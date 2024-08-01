from config.DBConnection import DBConnection
from datetime import datetime, date
from models.GenresModel import GenresModel


class BooksModel:
    def __init__(self):
        self.db = DBConnection()
        self.genre_model = GenresModel()

    def create_book(self, book_data):
        try:
            query = "INSERT INTO books(stock, isbn13, author, original_publication_year, title, summary, genre_id, availability, best_seller) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING book_id"
            params = (book_data.get("stock", None),
                      book_data.get("isbn13"),
                      book_data.get("author"),
                      book_data.get("original_publication_year", None),
                      book_data.get("title"),
                      book_data.get("summary", None),
                      book_data.get("genre_id", None),
                      book_data.get("availability", True),
                      book_data.get("best_seller", False))
            result = self.db.execute_query(query, params)  # result returns a list of tuples [(123,)]
            if result:
                return result[0][0]  # access first item in row and column of tuple
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
# try-except is used to handle errors during database operations like connection issues, SQL errors or data processing
# if-else is conditional logic to handle scenarios based on outcome of the operation or checks

    def get_book_by_isbn(self, isbn13):
        try:
            query = "SELECT book_id, stock FROM books WHERE isbn13 = %s;"
            params = (isbn13,)
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error: {e}")

    def update_stock(self, isbn13):
        try:
            query = "UPDATE books SET stock = stock + 1 WHERE isbn13 = %s;"
            params = (isbn13,)
            self.db.execute_CUD_query(query, params)
        except Exception as e:
            print(f"Error: {e}")

    def book_data_validator(self, book_data):
        expected_types = {
            "stock": int,
            "isbn13": str,
            "author": str,
            "original_publication_year": date,
            "title": str,
            "summary": str,
            "genre_id": int,
            "availability": bool,
            "best_seller": bool
        }
        for key, value in book_data.items():
            if key in expected_types:
                if key == "original_publication_year":
                    value = self.parse_date(value)
                if not isinstance(value, expected_types[key]):
                    raise TypeError(
                        f"Invalid type for {key}. Expected {expected_types[key].__name__}, got {type(value).__name__}.")
            else:
                raise KeyError(f"Unexpected key {key} found in data.")
        return True

    def parse_date(self, date_str):
        try:
            parsed_date = datetime.strptime(date_str, '%d%m%Y').date()
            return parsed_date
        except ValueError:
            raise ValueError(f"Invalid date format for {date_str}. Expected format is DDMMYYYY.")

    def update_book(self, book_id, book_data):
        try:
            update_fields = []
            params = []
            allowed_fields = {
                "stock": "stock = %s",
                "isbn13": "isbn13 = %s",
                "author": "author = %s",
                "original_publication_year": "original_publication_year = %s",
                "title": "title = %s",
                "summary": "summary = %s",
                "genre_id": "genre_id = %s",
                "availability": "availability = %s",
                "best_seller": "best_seller = %s",
            }

            for field in book_data:
                if field in allowed_fields:
                    update_fields.append(allowed_fields[field])
                    params.append(book_data[field])

            if not update_fields:
                raise ValueError("No valid fields to update.")

            query = f"UPDATE books SET {', '.join(update_fields)} WHERE book_id = %s;"
            params.append(book_id)
            self.db.execute_CUD_query(query, tuple(params))
            return True
        except Exception as e:
            print(f"Error updating book with ID {book_id}: {e}")
            return False


"""    def search_books(self, author=None, title=None, genre_id=None):
        try:
            query = "SELECT book_id, stock, isbn13, author, original_publication_year, title, summary, genre_id, availability, best_seller FROM books WHERE 1=1 "
            params = []
            if author:
                query += " AND author ILIKE %s"
                params.append(f"%{author}%")
            if title:
                query += " AND title ILIKE %s"
                params.append(f"%{title}%")
            if genre_id:
                query += "AND genre_id = %s"
                params.append(f"%{genre_id}%")
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error: {e}")"""


