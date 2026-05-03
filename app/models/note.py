import sqlite3
from .database import get_db_connection

class Note:
    @staticmethod
    def get_by_book_id(book_id):
        """根據書籍 ID 取得所有關聯筆記"""
        try:
            conn = get_db_connection()
            notes = conn.execute(
                'SELECT * FROM notes WHERE book_id = ? ORDER BY created_at DESC', 
                (book_id,)
            ).fetchall()
            return [dict(note) for note in notes]
        except sqlite3.Error as e:
            print(f"Error in Note.get_by_book_id: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(note_id):
        """根據 ID 取得單筆筆記記錄"""
        try:
            conn = get_db_connection()
            note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
            return dict(note) if note else None
        except sqlite3.Error as e:
            print(f"Error in Note.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def create(book_id, content):
        """新增一筆筆記記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO notes (book_id, content) VALUES (?, ?)',
                (book_id, content)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error in Note.create: {e}")
            if 'conn' in locals():
                conn.rollback()
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(note_id, content):
        """更新單筆筆記記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                '''UPDATE notes 
                   SET content = ?, updated_at = CURRENT_TIMESTAMP 
                   WHERE id = ?''',
                (content, note_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error in Note.update: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(note_id):
        """刪除單筆筆記記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error in Note.delete: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search(keyword):
        """根據關鍵字搜尋筆記內容"""
        try:
            conn = get_db_connection()
            search_term = f"%{keyword}%"
            notes = conn.execute(
                '''SELECT notes.*, books.title as book_title 
                   FROM notes 
                   JOIN books ON notes.book_id = books.id 
                   WHERE content LIKE ? 
                   ORDER BY notes.created_at DESC''',
                (search_term,)
            ).fetchall()
            return [dict(note) for note in notes]
        except sqlite3.Error as e:
            print(f"Error in Note.search: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
