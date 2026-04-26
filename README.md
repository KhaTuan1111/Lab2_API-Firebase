# Note App - API & Firebase

##  Giới thiệu

Đây là một ứng dụng **Note App** đơn giản được xây dựng theo kiến trúc full-stack, nhằm minh họa cách hoạt động của:

* Frontend (Streamlit)
* Backend (FastAPI)
* Firebase Authentication (đăng nhập)
* Firebase Firestore (lưu trữ dữ liệu)

Ứng dụng cho phép người dùng:

* Đăng nhập bằng Firebase
* Tạo ghi chú (note)
* Xem danh sách ghi chú
* Cập nhật ghi chú
* Xóa ghi chú

---

##  Kiến trúc hệ thống

```
Lab2_API-Firebase/
│
├── frontend/
│   └── app.py              # Giao diện Streamlit
│
├── backend/
│   ├── main.py             # API FastAPI
│   └── serviceAccountKey.json  # Firebase Admin SDK 
│
├── requirements.txt
└── README.md
```

---

##  Công nghệ sử dụng

### Frontend:

* Streamlit

### Backend:

* FastAPI
* Uvicorn

### Authentication:

* Firebase Authentication (Email/Password)

### Database:

* Firebase Firestore

---

##  Chức năng chính

###  Authentication

* Đăng nhập bằng Firebase
* Lấy thông tin user hiện tại (`/auth/me`)

###  Note Management (CRUD)

*  Tạo note
*  Xem danh sách note
*  Cập nhật note
*  Xóa note

Tất cả dữ liệu được:

* Gắn với `user_id`
* Lưu trên Firestore

---

##  Luồng hoạt động

1. Người dùng đăng nhập trên frontend (Firebase)
2. Nhận ID Token
3. Frontend gửi request kèm token đến backend
4. Backend xác thực token bằng Firebase Admin SDK
5. Thực hiện thao tác (CRUD note)
6. Lưu/đọc dữ liệu từ Firestore
7. Trả kết quả về frontend

---

## API Endpoints

###  System

* `GET /`
* `GET /health`
  → Kiểm tra server hoạt động

---

###  Authentication

* `GET /auth/me`
  → Lấy thông tin user từ token

---

###  Notes

* `POST /notes`
  → Tạo note

* `GET /notes`
  → Lấy danh sách note của user

* `PUT /notes/{note_id}`
  → Cập nhật note

* `DELETE /notes/{note_id}`
  → Xóa note

---

##  Hướng dẫn cài đặt

###  Clone project

```
git clone <your-repo-link>
cd Lab2_API-Firebase
```

---

###  Cài đặt Backend

```
cd backend
uvicorn main:app --reload
```

#### Windows:

```
venv\Scripts\activate
```

#### Mac/Linux:

```
source venv/bin/activate
```

Cài thư viện:

```
pip install -r requirements.txt
```

---

###  Cấu hình Firebase (QUAN TRỌNG)

1. Vào Firebase Console
2. Tạo project
3. Bật:

   * Authentication (Email/Password)
   * Firestore Database
4. Tải file:

   ```
   serviceAccountKey.json
   ```
5. Đặt vào:

```
backend/serviceAccountKey.json
```

 Không commit file này lên GitHub

---

###  Chạy Backend

```
uvicorn main:app --reload
```

Backend chạy tại:

```
http://127.0.0.1:8000
```

---

###  Chạy Frontend

```
cd frontend
streamlit run app.py
```
Frontend chạy tại:

```
http://localhost:8501/
```
---

##  Cấu hình Frontend

Trong file:

```
frontend/app.py
```

Bạn cần cấu hình:

```
FIREBASE_WEB_API_KEY = "YOUR_API_KEY"
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000"
```

---

##  Cấu trúc dữ liệu (Firestore)

Collection:

```
notes/
```

Document:

```
{
  id: string,
  user_id: string,
  content: string,
  created_at: string,
  updated_at: string (optional)
}
```

---

##  Video Demo

 Link video: https://drive.google.com/drive/u/0/folders/1TGHgDU15yByadarf5cLeksAPP6sLCZ_a

---

##  Lưu ý quan trọng

 Không upload:

* serviceAccountKey.json
* API key
* token

Đảm bảo:

* Backend chạy được
* Frontend kết nối được backend
* Firebase hoạt động bình thường

---

##  Tác giả

* Tên: Bùi Đặng Khả Tuân   
* MSSV: 24120236  
* Trường: Đại học Khoa học Tự nhiên - ĐHQG-HCM

---


