# File: app.py (Đã nâng cấp lên Cấp độ 2)
# Thêm: flask_cors, requests, jose
# Thêm: API /student (Yêu cầu #2)

from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
import os
import json # Thêm thư viện json

# Thêm 2 thư viện cho Yêu cầu #4 (Keycloak)
import requests
from jose import jwt

app = Flask(__name__)
CORS(app) # Cho phép Cross-Origin

# === PHẦN CẤP ĐỘ 2 (Yêu cầu #2 - API /student) ===
# Hàm để đọc file students.json
def load_students_from_file():
    try:
        # Mở file students.json (cùng thư mục với app.py)
        with open('students.json', 'r', encoding='utf-8') as f:
            students_data = json.load(f)
        return students_data
    except FileNotFoundError:
        print("LỖI: Không tìm thấy file 'students.json'.")
        return []
    except json.JSONDecodeError:
        print("LỖI: File 'students.json' bị lỗi định dạng JSON.")
        return []

# API endpoint /student
@app.route('/student', methods=['GET'])
def get_students():
    """
    API endpoint (Cấp độ 2)
    Đọc và trả về danh sách sinh viên từ file students.json
    """
    students = load_students_from_file()
    if not students:
        return jsonify({"error": "Không thể tải dữ liệu sinh viên"}), 500
    return jsonify(students)
# === KẾT THÚC PHẦN CẤP ĐỘ 2 ===


# Cấu hình kết nối DB (Lấy từ biến môi trường)
db_host = os.environ.get('DB_HOST', 'db') # Tên service 'db'
db_user = os.environ.get('DB_USER', 'admin')
db_password = os.environ.get('DB_PASSWORD', 'password123')
db_name = os.environ.get('DB_NAME', 'minicloud')

conn = None

def get_db_connection():
    global conn
    if conn is None or conn.closed:
        try:
            conn = mariadb.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=3306
            )
            print(f"Kết nối thành công đến MariaDB tại {db_host}")
        except mariadb.Error as e:
            print(f"Lỗi khi kết nối đến MariaDB: {e}")
            return None
    return conn

@app.route('/')
def hello():
    return jsonify(message="Chào mừng đến với Application Server (API)!", service="app-server", version="1.0")

@app.route('/health')
def health_check():
    conn_check = get_db_connection()
    if conn_check:
        return jsonify(status="OK", database="Connected"), 200
    else:
        return jsonify(status="ERROR", database="Connection failed"), 500

@app.route('/api/v1/blog/posts', methods=['GET'])
def get_blog_posts():
    db = get_db_connection()
    if not db:
        return jsonify(error="Lỗi kết nối CSDL"), 500
    
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT post_id, title, content, author, created_at FROM posts")
        posts = cursor.fetchall()
        cursor.close()
        return jsonify(posts)
    except mariadb.Error as e:
        cursor.close()
        return jsonify(error=f"Lỗi truy vấn CSDL: {e}"), 500

if __name__ == '__main__':
    # Chạy Flask ở cổng 8081 bên trong container
    app.run(host='0.0.0.0', port=8081, debug=True)

