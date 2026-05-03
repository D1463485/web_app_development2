# 路由與頁面設計 - 讀書筆記本

本文件定義系統的 Flask 路由 (Routes)、HTTP 方法、處理邏輯與對應的 Jinja2 模板，做為前後端串接的開發依據。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁 / 書籍列表 | GET | `/` 或 `/books` | `index.html` | 顯示所有已建立的書籍清單 |
| 搜尋功能 | GET | `/search` | `search_results.html` | 根據關鍵字搜尋書籍與筆記 |
| 新增書籍頁面 | GET | `/books/new` | `form.html` | 顯示新增書籍的輸入表單 |
| 建立書籍 | POST | `/books` | — | 接收表單資料，存入 DB，重導向至首頁 |
| 書籍詳情 | GET | `/books/<id>` | `book_detail.html` | 顯示書籍詳細資訊及該書的分段筆記 |
| 編輯書籍頁面 | GET | `/books/<id>/edit` | `form.html` | 顯示編輯書籍的表單（帶入原資料） |
| 更新書籍 | POST | `/books/<id>/update` | — | 接收表單，更新 DB，重導向至書籍詳情 |
| 更新閱讀狀態 | POST | `/books/<id>/status` | — | 接收狀態變更，更新 DB，重導向至書籍詳情 |
| 刪除書籍 | POST | `/books/<id>/delete` | — | 刪除書籍及關聯筆記，重導向至首頁 |
| 新增分段筆記 | POST | `/books/<id>/notes` | — | 接收筆記內容，存入 DB，重導向至書籍詳情 |
| 刪除分段筆記 | POST | `/notes/<id>/delete` | — | 刪除單筆筆記，重導向至原書籍詳情頁 |

---

## 2. 每個路由的詳細說明

### 2.1 書籍相關路由 (book_routes)

- **首頁 / 書籍列表**
  - **輸入**：無
  - **處理邏輯**：呼叫 `Book.get_all()` 取得書籍列表。
  - **輸出**：渲染 `index.html`。
  
- **搜尋功能**
  - **輸入**：URL 參數 `q` (例如 `?q=習慣`)。
  - **處理邏輯**：取得參數 `q`，呼叫 `Book.search(q)` 與 `Note.search(q)`。
  - **輸出**：渲染 `search_results.html` 顯示搜尋結果。

- **新增書籍頁面**
  - **輸入**：無
  - **處理邏輯**：準備空表單供前端使用。
  - **輸出**：渲染 `form.html` (模式設為 create)。

- **建立書籍**
  - **輸入**：表單欄位 `title`、`author`。
  - **處理邏輯**：驗證 `title` 是否為空。呼叫 `Book.create(title, author)`。
  - **輸出**：重導向至 `/books`。
  - **錯誤處理**：若標題空白，閃現 (flash) 錯誤訊息並重導回新增頁面。

- **書籍詳情**
  - **輸入**：URL 參數 `<id>`。
  - **處理邏輯**：呼叫 `Book.get_by_id(id)`，若不存在回傳 404；呼叫 `Note.get_by_book_id(id)` 取得該書筆記。
  - **輸出**：渲染 `book_detail.html`。

- **編輯書籍頁面**
  - **輸入**：URL 參數 `<id>`。
  - **處理邏輯**：取得書籍資料，準備編輯表單。
  - **輸出**：渲染 `form.html` (模式設為 edit，並帶入現有資料)。

- **更新書籍**
  - **輸入**：URL 參數 `<id>`，表單欄位 `title`、`author`、`status`。
  - **處理邏輯**：呼叫 `Book.update(id, title, author, status)`。
  - **輸出**：重導向至 `/books/<id>`。

- **更新閱讀狀態**
  - **輸入**：URL 參數 `<id>`，表單欄位或參數 `status`。
  - **處理邏輯**：呼叫 `Book.update_status(id, status)`。
  - **輸出**：重導向至 `/books/<id>`。

- **刪除書籍**
  - **輸入**：URL 參數 `<id>`。
  - **處理邏輯**：呼叫 `Book.delete(id)` (資料庫設定 ON DELETE CASCADE 會一併刪除筆記)。
  - **輸出**：重導向至 `/books`。

### 2.2 筆記相關路由 (note_routes)

- **新增分段筆記**
  - **輸入**：URL 參數 `book_id`，表單欄位 `content`。
  - **處理邏輯**：呼叫 `Note.create(book_id, content)`。
  - **輸出**：重導向至 `/books/<book_id>`。
  - **錯誤處理**：內容空白則 flash 警告並重導向。

- **刪除分段筆記**
  - **輸入**：URL 參數 `<id>`。
  - **處理邏輯**：先透過 `Note.get_by_id(id)` 取得 `book_id`，接著呼叫 `Note.delete(id)`。
  - **輸出**：重導向至 `/books/<book_id>`。

---

## 3. Jinja2 模板清單

所有的 HTML 檔案皆建立在 `app/templates/` 目錄中，並使用模板繼承機制。

- `base.html`：母版 (Base Template)，包含全站共用的 `<head>`、導覽列、頁尾與 Flash 訊息區塊。所有其他模板都必須 `{% extends "base.html" %}`。
- `index.html`：首頁，繼承 `base.html`，展示書籍卡片與狀態過濾選項。
- `search_results.html`：搜尋結果頁，繼承 `base.html`，展示符合的書籍與筆記清單。
- `book_detail.html`：書籍詳情頁，繼承 `base.html`，展示書籍資訊、閱讀狀態切換按鈕，以及該書所有的筆記列表與新增筆記的表單。
- `form.html`：共用的書籍表單頁，繼承 `base.html`，用於「新增書籍」與「編輯書籍」。

## 4. 路由骨架程式碼
對應的路由骨架已建立於 `app/routes/book_routes.py` 與 `app/routes/note_routes.py`，使用 Flask Blueprint 模組化設計。
