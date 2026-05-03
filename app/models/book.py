from .database import get_db_connection

class Book:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(book) for book in books]

    @staticmethod
    def get_by_id(book_id):
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        return dict(book) if book else None

    @staticmethod
    def create(title, author='', status='unread'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO books (title, author, status) VALUES (?, ?, ?)',
            (title, author, status)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def update(book_id, title, author, status):
        conn = get_db_connection()
        conn.execute(
            '''UPDATE books 
               SET title = ?, author = ?, status = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?''',
            (title, author, status, book_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(book_id, status):
        conn = get_db_connection()
        conn.execute(
            'UPDATE books SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status, book_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = get_db_connection()
        search_term = f"%{keyword}%"
        books = conn.execute(
            'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY created_at DESC',
            (search_term, search_term)
        ).fetchall()
        conn.close()
        return [dict(book) for book in books]
