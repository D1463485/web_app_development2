from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import Book
from app.models.note import Note

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
    books = Book.get_all()
    return render_template('index.html', books=books)

@book_bp.route('/search')
def search():
    """
    搜尋書籍與筆記。
    輸入: query 參數 'q'
    邏輯: 根據關鍵字搜尋 books 和 notes 表
    輸出: 渲染 search_results.html
    """
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('book.index'))
    
    books = Book.search(query)
    notes = Note.search(query)
    return render_template('search_results.html', query=query, books=books, notes=notes)

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    顯示新增書籍的表單。
    輸入: 無
    邏輯: 無
    輸出: 渲染 form.html (create 模式)
    """
    return render_template('form.html', mode='create')

@book_bp.route('/books', methods=['POST'])
def create_book():
    """
    接收表單資料並建立新書籍。
    輸入: 表單 title, author
    邏輯: 存入資料庫
    輸出: 重導向至首頁
    """
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    
    if not title:
        flash('書名是必填欄位', 'error')
        return redirect(url_for('book.new_book'))
        
    Book.create(title, author)
    flash('書籍新增成功', 'success')
    return redirect(url_for('book.index'))

@book_bp.route('/books/<int:id>', methods=['GET'])
def book_detail(id):
    """
    顯示書籍詳細資訊及關聯的分段筆記。
    輸入: URL 參數 id
    邏輯: 取得特定書籍與其所有筆記
    輸出: 渲染 book_detail.html
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍', 'error')
        return redirect(url_for('book.index'))
        
    notes = Note.get_by_book_id(id)
    return render_template('book_detail.html', book=book, notes=notes)

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    顯示編輯書籍的表單。
    輸入: URL 參數 id
    邏輯: 取得特定書籍資料帶入表單
    輸出: 渲染 form.html (edit 模式)
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍', 'error')
        return redirect(url_for('book.index'))
        
    return render_template('form.html', mode='edit', book=book)

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    更新書籍資訊。
    輸入: URL 參數 id, 表單 title, author, status
    邏輯: 更新資料庫
    輸出: 重導向至書籍詳情頁
    """
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    status = request.form.get('status', 'unread')
    
    if not title:
        flash('書名是必填欄位', 'error')
        return redirect(url_for('book.edit_book', id=id))
        
    Book.update(id, title, author, status)
    flash('書籍更新成功', 'success')
    return redirect(url_for('book.book_detail', id=id))

@book_bp.route('/books/<int:id>/status', methods=['POST'])
def update_status(id):
    """
    快速更新書籍的閱讀狀態。
    輸入: URL 參數 id, 表單 status
    邏輯: 更新資料庫該書的 status 欄位
    輸出: 重導向至書籍詳情頁
    """
    status = request.form.get('status')
    if status in ['unread', 'reading', 'finished']:
        Book.update_status(id, status)
        flash('狀態更新成功', 'success')
    else:
        flash('無效的狀態', 'error')
        
    return redirect(url_for('book.book_detail', id=id))

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    刪除書籍及其所有關聯筆記。
    輸入: URL 參數 id
    邏輯: 從資料庫刪除書籍
    輸出: 重導向至首頁
    """
    Book.delete(id)
    flash('書籍刪除成功', 'success')
    return redirect(url_for('book.index'))
