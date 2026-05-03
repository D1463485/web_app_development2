# 系統與使用者流程圖 - 讀書筆記本

本文件根據 PRD 需求與架構設計，繪製了使用者的操作流程圖與系統後端的序列圖，並整理了未來預計開發的功能路徑清單。

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者進入網站後，可以進行的各項主要操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 書籍列表]
    
    B --> C{選擇操作}
    
    C -->|新增書籍| D[填寫書籍表單]
    D -->|送出| B
    
    C -->|關鍵字搜尋| E[顯示篩選後的書籍結果]
    E --> B
    
    C -->|點擊特定書籍| F[書籍詳細與筆記頁面]
    
    F --> G{針對單一書籍操作}
    
    G -->|更新閱讀狀態| H[切換狀態:未讀/在讀/完讀]
    H --> F
    
    G -->|新增分段筆記| I[填寫筆記內容]
    I -->|送出| F
    
    G -->|編輯/刪除書籍| J[執行修改或刪除]
    J -->|刪除成功或修改後| B
    
    G -->|返回上一頁| B
```

## 2. 系統序列圖 (Sequence Diagram)

此圖以「使用者新增分段筆記」為例，描述前端瀏覽器、後端 Flask 路由與 SQLite 資料庫之間的完整互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask Route (Controller)
    participant Model as Database Model
    participant DB as SQLite

    User->>Browser: 填寫筆記內容並點擊「送出筆記」
    Browser->>Flask: POST /books/1/notes (傳送表單資料)
    Flask->>Model: 呼叫 add_note(book_id, content)
    Model->>DB: 執行 SQL: INSERT INTO notes...
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳成功結果
    Flask-->>Browser: HTTP 302 重導向 (Redirect) 至 /books/1
    Browser->>Flask: GET /books/1 (重新請求頁面)
    Flask->>Model: 查詢該書籍與最新筆記清單
    Model->>DB: 執行 SQL: SELECT ...
    DB-->>Model: 回傳查詢資料
    Model-->>Flask: 格式化後的書籍與筆記物件
    Flask-->>Browser: 渲染 book_detail.html 並回傳 HTML
    Browser-->>User: 畫面更新，顯示剛新增的筆記
```

## 3. 功能清單對照表

根據上述流程，初步規劃系統功能對應的 URL 路徑與 HTTP 方法（可作為後續 API / 路由設計的參考）：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|----------|----------|-----------|------|
| 首頁 / 書架列表 | `/` 或 `/books` | GET | 顯示所有已建立的書籍清單 |
| 新增書籍 | `/books/add` | GET / POST | GET: 顯示新增表單<br>POST: 接收資料寫入資料庫 |
| 書籍詳細頁 | `/books/<id>` | GET | 顯示書籍資訊及該書的所有分段筆記 |
| 編輯書籍 | `/books/<id>/edit`| GET / POST | 顯示並送出書名、作者等修改資訊 |
| 刪除書籍 | `/books/<id>/delete`| POST | 刪除整本書籍與關聯的所有筆記 |
| 更新閱讀狀態 | `/books/<id>/status`| POST | 接收狀態變更請求並更新資料庫 |
| 新增分段筆記 | `/books/<id>/notes/add`| POST | 接收筆記內容並寫入資料庫 |
| 刪除分段筆記 | `/notes/<note_id>/delete`| POST | 刪除特定的一則筆記 |
| 關鍵字搜尋 | `/search` | GET | 根據 GET 參數（如 `?q=關鍵字`）搜尋 |
