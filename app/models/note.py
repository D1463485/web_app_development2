from .database import get_db_connection

class Note:
    @staticmethod
    def get_by_book_id(book_id):
        conn = get_db_connection()
        notes = conn.execute(
            'SELECT * FROM notes WHERE book_id = ? ORDER BY created_at DESC', 
            (book_id,)
        ).fetchall()
        conn.close()
        return [dict(note) for note in notes]

    @staticmethod
    def get_by_id(note_id):
        conn = get_db_connection()
        note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
        conn.close()
        return dict(note) if note else None

    @staticmethod
    def create(book_id, content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO notes (book_id, content) VALUES (?, ?)',
            (book_id, content)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def update(note_id, content):
        conn = get_db_connection()
        conn.execute(
            '''UPDATE notes 
               SET content = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?''',
            (content, note_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(note_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(keyword):
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
        conn.close()
        return [dict(note) for note in notes]
