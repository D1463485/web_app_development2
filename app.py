import os
from flask import Flask
from app.routes.book_routes import book_bp
from app.routes.note_routes import note_bp
from app.models.database import init_db

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# 設定 SECRET_KEY 用於 session 與 flash message
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret_key')

# 註冊 Blueprints
app.register_blueprint(book_bp)
app.register_blueprint(note_bp)

# 在應用程式啟動前確保資料庫已經初始化
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
