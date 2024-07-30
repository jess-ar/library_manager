from config.DBConnection import DBConnection


class BooksModel:
    def __init__(self):
        self.db = DBConnection()

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

