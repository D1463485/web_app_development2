from flask import Blueprint, request, redirect, url_for, flash

note_bp = Blueprint('note', __name__)

@note_bp.route('/books/<int:book_id>/notes', methods=['POST'])
def create_note(book_id):
    """
    為特定書籍新增分段筆記。
    輸入: URL 參數 book_id, 表單 content
    邏輯: 將筆記內容寫入資料庫
    輸出: 重導向至書籍詳情頁
    """
    pass

@note_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete_note(id):
    """
    刪除特定分段筆記。
    輸入: URL 參數 id
    邏輯: 從資料庫刪除筆記
    輸出: 重導向至原書籍的詳情頁
    """
    pass
