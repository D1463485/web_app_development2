import sqlite3
from .database import get_db_connection

class Book:
    @staticmethod
    def get_all():
        """取得所有書籍記錄"""
        try:
            conn = get_db_connection()
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            return [dict(book) for book in books]
        except sqlite3.Error as e:
            print(f"Error in Book.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(book_id):
        """根據 ID 取得單筆書籍記錄"""
        try:
            conn = get_db_connection()
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            return dict(book) if book else None
        except sqlite3.Error as e:
            print(f"Error in Book.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def create(title, author='', status='unread'):
        """新增一筆書籍記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO books (title, author, status) VALUES (?, ?, ?)',
                (title, author, status)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error in Book.create: {e}")
            if 'conn' in locals():
                conn.rollback()
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(book_id, title, author, status):
        """更新單筆書籍記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                '''UPDATE books 
                   SET title = ?, author = ?, status = ?, updated_at = CURRENT_TIMESTAMP 
                   WHERE id = ?''',
                (title, author, status, book_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error in Book.update: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update_status(book_id, status):
        """更新書籍的閱讀狀態"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE books SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (status, book_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error in Book.update_status: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(book_id):
        """刪除單筆書籍記錄（關聯筆記將一併被刪除）"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error in Book.delete: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search(keyword):
        """根據關鍵字搜尋書籍"""
        try:
            conn = get_db_connection()
            search_term = f"%{keyword}%"
            books = conn.execute(
                'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY created_at DESC',
                (search_term, search_term)
            ).fetchall()
            return [dict(book) for book in books]
        except sqlite3.Error as e:
            print(f"Error in Book.search: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
