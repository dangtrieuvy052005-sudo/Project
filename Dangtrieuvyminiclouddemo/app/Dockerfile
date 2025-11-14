# File: app/Dockerfile (Đã nâng cấp)
# Thêm: requests, python-jose, flask-cors

# Sử dụng base image Python
FROM python:3.10-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Sao chép file requirements (nếu có)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Cài đặt các thư viện Python cần thiết
# (Đã thêm 3 thư viện cho Cấp độ 2)
RUN pip install flask mariadb flask-cors requests python-jose

# Sao chép toàn bộ code từ thư mục 'app' (local)
# vào thư mục '/app' (container)
COPY . .

# Chỉ định cổng mà Flask sẽ chạy (bên trong container)
EXPOSE 8081

# Lệnh để khởi động ứng dụng khi container chạy
# (Sử dụng gunicorn cho production hoặc flask run cho dev)
# ENV FLASK_APP=app.py
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8081"]

# Hoặc chạy trực tiếp (như code mẫu của bạn):
CMD ["python", "app.py"]

