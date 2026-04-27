# Note App - API & Firebase

## 1. Giới thiệu

Đây là ứng dụng **Note App** đơn giản được xây dựng theo kiến trúc full-stack nhằm minh họa luồng hoạt động giữa:

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Authentication**: Firebase Authentication
- **Database**: Firebase Firestore

Ứng dụng cho phép người dùng đăng nhập bằng Firebase, sau đó thực hiện các thao tác quản lý ghi chú cá nhân như:

- Tạo ghi chú
- Xem danh sách ghi chú
- Cập nhật ghi chú
- Xóa ghi chú

Mỗi ghi chú được gắn với tài khoản người dùng hiện tại thông qua `user_id`, giúp dữ liệu của từng người dùng được tách biệt.

---

## 2. Công nghệ sử dụng

### Frontend

- Streamlit
- Requests

### Backend

- FastAPI
- Uvicorn
- Firebase Admin SDK

### Authentication

- Firebase Authentication
- Email/Password Login

### Database

- Firebase Firestore

---

## 3. Chức năng chính

### 3.1. Authentication

Ứng dụng hỗ trợ:

- Đăng ký tài khoản bằng email/password
- Đăng nhập bằng Firebase Authentication
- Đăng xuất
- Lấy thông tin người dùng hiện tại thông qua Firebase ID Token

### 3.2. Note Management

Sau khi đăng nhập, người dùng có thể:

- Tạo note mới
- Xem danh sách note của chính mình
- Cập nhật nội dung note
- Xóa note

Tất cả dữ liệu note được lưu trên Firebase Firestore và được gắn với `user_id` của người dùng đang đăng nhập.

---

## 4. Luồng hoạt động hệ thống

```text
Người dùng đăng nhập trên frontend
        ↓
Firebase Authentication trả về ID Token
        ↓
Frontend gửi request kèm ID Token đến backend
        ↓
Backend xác thực token bằng Firebase Admin SDK
        ↓
Backend xử lý CRUD note
        ↓
Dữ liệu được lưu hoặc đọc từ Firestore
        ↓
Backend trả kết quả về frontend
        ↓
Frontend hiển thị kết quả cho người dùng
```

---

## 5. Cấu trúc thư mục

```text
Lab2_API-Firebase/
│
├── backend/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

> Lưu ý: File `serviceAccountKey.json` chỉ được đặt ở máy local để chạy backend. File này **không được commit lên GitHub**.

---

## 6. API Endpoints

### 6.1. System

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/` | Kiểm tra backend đang hoạt động |
| GET | `/health` | Kiểm tra trạng thái hệ thống |

### 6.2. Authentication

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/auth/me` | Lấy thông tin người dùng hiện tại từ Firebase ID Token |

### 6.3. Notes

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/notes` | Tạo ghi chú mới |
| GET | `/notes` | Lấy danh sách ghi chú của người dùng hiện tại |
| PUT | `/notes/{note_id}` | Cập nhật ghi chú |
| DELETE | `/notes/{note_id}` | Xóa ghi chú |

Các endpoint liên quan đến note yêu cầu header xác thực:

```text
Authorization: Bearer <Firebase_ID_Token>
```

---

## 7. Cấu trúc dữ liệu Firestore

Collection:

```text
notes
```

Mỗi document note có cấu trúc ví dụ:

```json
{
  "id": "note_document_id",
  "user_id": "firebase_user_uid",
  "content": "Nội dung ghi chú",
  "created_at": "2026-04-27T10:00:00",
  "updated_at": "2026-04-27T10:10:00"
}
```

---

## 8. Hướng dẫn cài đặt

### 8.1. Clone repository

```bash
git clone https://github.com/KhaTuan1111/Lab2_API-Firebase.git
cd Lab2_API-Firebase
```

### 8.2. Tạo môi trường ảo

```bash
python -m venv venv
```

### 8.3. Kích hoạt môi trường ảo

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 8.4. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

## 9. Cấu hình Firebase

### 9.1. Bật Firebase Authentication

1. Truy cập Firebase Console.
2. Chọn project Firebase.
3. Vào **Authentication**.
4. Chọn **Sign-in method**.
5. Bật phương thức **Email/Password**.

### 9.2. Tạo Firestore Database

1. Vào **Firestore Database**.
2. Chọn **Create database**.
3. Chọn chế độ phù hợp để test.
4. Tạo database để lưu dữ liệu note.

### 9.3. Tạo Firebase Admin SDK key

1. Vào **Project settings**.
2. Chọn tab **Service accounts**.
3. Chọn **Generate new private key**.
4. Tải file JSON về.
5. Đổi tên file thành:

```text
serviceAccountKey.json
```

6. Đặt file vào thư mục:

```text
backend/serviceAccountKey.json
```

> File `serviceAccountKey.json` chứa private key, vì vậy không được upload lên GitHub.

---

## 10. Cấu hình Frontend

Trong file:

```text
frontend/app.py
```

cần cấu hình Firebase Web API Key và URL backend:

```python
FIREBASE_WEB_API_KEY = "YOUR_FIREBASE_WEB_API_KEY"
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000"
```

Trong đó:

- `FIREBASE_WEB_API_KEY`: lấy từ Firebase project settings.
- `FASTAPI_BACKEND_URL`: địa chỉ backend FastAPI đang chạy.

---

## 11. Chạy ứng dụng

### 11.1. Chạy Backend

Từ thư mục gốc của project:

```bash
cd backend
uvicorn main:app --reload
```

Backend chạy tại:

```text
http://127.0.0.1:8000
```

Có thể kiểm tra backend bằng cách mở:

```text
http://127.0.0.1:8000
```

hoặc:

```text
http://127.0.0.1:8000/health
```

---

### 11.2. Chạy Frontend

Mở terminal mới, kích hoạt môi trường ảo nếu cần, sau đó chạy:

```bash
cd frontend
streamlit run app.py
```

Frontend chạy tại:

```text
http://localhost:8501
```

---

## 12. Hướng dẫn sử dụng

1. Mở frontend tại `http://localhost:8501`.
2. Đăng ký tài khoản bằng email/password nếu chưa có tài khoản.
3. Đăng nhập bằng tài khoản Firebase.
4. Sau khi đăng nhập, ứng dụng hiển thị thông tin người dùng hiện tại.
5. Nhập nội dung note và chọn tạo note.
6. Danh sách note sẽ được hiển thị trên giao diện.
7. Người dùng có thể cập nhật hoặc xóa note đã tạo.
8. Dữ liệu được lưu trên Firebase Firestore theo từng user.

---

## 13. Video demo

Link video demo:

```text
https://drive.google.com/drive/u/0/folders/1TGHgDU15yByadarf5cLeksAPP6sLCZ_a
```

> Khuyến nghị: Nên thay link folder bằng link trực tiếp đến file video và bật quyền **Anyone with the link can view** để giảng viên có thể xem ngay.

---

## 14. Lưu ý bảo mật

Không commit các file hoặc thông tin sau lên GitHub:

```text
serviceAccountKey.json
.env
token
private key
file cache
__pycache__/
venv/
```

Nên thêm các dòng sau vào `.gitignore`:

```gitignore
# Python
__pycache__/
*.pyc
venv/

# Environment variables
.env

# Firebase secrets
backend/serviceAccountKey.json
serviceAccountKey.json

# OS / Editor
.DS_Store
.vscode/
```

---

## 15. Checklist trước khi nộp bài

Trước khi nộp, cần đảm bảo repository có đầy đủ:

- `frontend/app.py`
- `backend/main.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

Đồng thời đảm bảo:

- Backend chạy được bằng FastAPI.
- Frontend chạy được bằng Streamlit.
- Có đăng nhập bằng Firebase Authentication.
- Có đăng xuất.
- Có nhận diện người dùng hiện tại sau khi đăng nhập.
- Có thao tác thêm, xem, sửa, xóa note.
- Dữ liệu note được lưu và đọc từ Firestore.
- README có hướng dẫn cài đặt và chạy project.
- README có link video demo.
- Không upload `serviceAccountKey.json`, token hoặc private key lên GitHub.

---

## 16. Tác giả

- Họ tên: Bùi Đặng Khả Tuân
- MSSV: 24120236
- Trường: Đại học Khoa học Tự nhiên - ĐHQG-HCM
- Môn học: Tư duy tính toán
