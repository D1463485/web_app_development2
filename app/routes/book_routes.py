from flask import Blueprint, render_template, request, redirect, url_for, flash

book_bp = Blueprint('book', __name__)

@book_bp.route('/')
@book_bp.route('/books')
def index():
    """
    顯示所有書籍列表。
    輸入: 無
    邏輯: 取得所有書籍
    輸出: 渲染 index.html
    """
    pass

@book_bp.route('/search')
def search():
    """
    搜尋書籍與筆記。
    輸入: query 參數 'q'
    邏輯: 根據關鍵字搜尋 books 和 notes 表
    輸出: 渲染 search_results.html
    """
    pass

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    顯示新增書籍的表單。
    輸入: 無
    邏輯: 無
    輸出: 渲染 form.html (create 模式)
    """
    pass

@book_bp.route('/books', methods=['POST'])
def create_book():
    """
    接收表單資料並建立新書籍。
    輸入: 表單 title, author
    邏輯: 存入資料庫
    輸出: 重導向至首頁
    """
    pass

@book_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    顯示書籍詳細資訊及關聯的分段筆記。
    輸入: URL 參數 id
    邏輯: 取得特定書籍與其所有筆記
    輸出: 渲染 book_detail.html
    """
    pass

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    顯示編輯書籍的表單。
    輸入: URL 參數 id
    邏輯: 取得特定書籍資料帶入表單
    輸出: 渲染 form.html (edit 模式)
    """
    pass

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    更新書籍資訊。
    輸入: URL 參數 id, 表單 title, author, status
    邏輯: 更新資料庫
    輸出: 重導向至書籍詳情頁
    """
    pass

@book_bp.route('/books/<int:id>/status', methods=['POST'])
def update_status(id):
    """
    快速更新書籍的閱讀狀態。
    輸入: URL 參數 id, 表單 status
    邏輯: 更新資料庫該書的 status 欄位
    輸出: 重導向至書籍詳情頁
    """
    pass

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除書籍及其所有關聯筆記。
    輸入: URL 參數 id
    邏輯: 從資料庫刪除書籍
    輸出: 重導向至首頁
    """
    pass
