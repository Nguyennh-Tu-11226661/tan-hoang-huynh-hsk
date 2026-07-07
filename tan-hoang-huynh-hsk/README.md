# Website Trung tâm Tiếng Trung Tân Hoàng Huynh HSK

Website Django hoàn chỉnh cho trung tâm tiếng Trung và luyện thi HSK tại Bắc Ninh. Project gồm giao diện responsive, quản trị nội dung, tuyển sinh, xuất dữ liệu, SEO cơ bản và dữ liệu mẫu bằng tiếng Việt.

## Công nghệ

- Python 3.11+ và Django 5.2 LTS (bản vá bảo mật mới)
- SQLite cho demo; PostgreSQL cho production
- Django Templates, HTML, CSS, JavaScript và Bootstrap 5
- Pillow để quản lý ảnh; WhiteNoise để phục vụ static
- openpyxl để xuất danh sách tư vấn ra Excel

## Cấu trúc project

```text
config/       Cấu hình Django, URL gốc
core/         Banner, FAQ, thông tin liên hệ, trang tĩnh, sitemap
courses/      Khóa học và lịch khai giảng
admissions/   Form tư vấn, học thử/test, chống spam, xuất CSV/Excel
content/      Blog, feedback học viên, thư viện ảnh/video
templates/    Giao diện theo từng app
static/       CSS và JavaScript
```

## Cài đặt nhanh với SQLite

Mở terminal tại thư mục project:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Django đọc biến môi trường của hệ điều hành. Với PowerShell, có thể chạy demo trực tiếp bằng cấu hình mặc định:

```powershell
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Truy cập:

- Website: `http://127.0.0.1:8000/`
- Quản trị: `http://127.0.0.1:8000/quan-tri/`
- Sitemap: `http://127.0.0.1:8000/sitemap.xml`
- Robots: `http://127.0.0.1:8000/robots.txt`

Lệnh `seed_data` có thể chạy lại an toàn; dữ liệu mẫu được cập nhật thay vì nhân bản.

## Dùng file `.env`

Project không tự đọc file `.env` để tránh thêm phụ thuộc không cần thiết. Khi phát triển, có thể nạp các biến từ `.env` bằng công cụ của IDE, Docker, hosting, hoặc gán trong PowerShell:

```powershell
$env:SECRET_KEY = "mot-secret-key-dai-va-ngau-nhien"
$env:DEBUG = "True"
$env:ALLOWED_HOSTS = "127.0.0.1,localhost"
python manage.py runserver
```

Không commit `.env`, mật khẩu database hoặc secret key lên Git.

`seed_data` cũng đọc các biến `CENTER_ADDRESS`, `CENTER_HOTLINE`,
`CENTER_EMAIL`, `CENTER_ZALO_URL`, `CENTER_FACEBOOK_URL`,
`CENTER_MESSENGER_URL` và `CENTER_MAP_EMBED_URL`. Facebook/Messenger sẽ
không được hiển thị nếu chưa có URL thật, tránh đưa người dùng tới liên kết
chung hoặc liên kết không thuộc trung tâm.

## Chuyển sang PostgreSQL

Tạo database và user trước, sau đó đặt biến môi trường:

```powershell
$env:DB_ENGINE = "postgresql"
$env:DB_NAME = "tanhoanghuynh_hsk"
$env:DB_USER = "hsk_app"
$env:DB_PASSWORD = "mat-khau-manh"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
python manage.py migrate
python manage.py seed_data
```

## Quản trị và xuất dữ liệu

Tại `/quan-tri/`, quản trị viên có thể quản lý:

- Khóa học và lịch khai giảng
- Đăng ký tư vấn và trạng thái chăm sóc
- Lịch học thử / test đầu vào
- Bài viết, feedback, thư viện
- Banner, FAQ và thông tin liên hệ

Để xuất danh sách tư vấn, vào **Đăng ký tư vấn**, chọn các dòng, sau đó chọn thao tác **Xuất đăng ký đã chọn ra CSV** hoặc **Excel**.

## Ảnh mẫu và thông tin vận hành

Dữ liệu mẫu có năm ảnh minh họa lớp học được tạo bằng AI dành riêng cho bản
demo. Lệnh `seed_data` tự đưa các ảnh này vào Banner, Khóa học, Blog và Thư
viện; không dùng ảnh stock hoặc liên kết ảnh bên ngoài. Đây không phải ảnh
chụp học viên thật. Trước khi phát hành, thay chúng bằng ảnh đã được trung tâm
cho phép sử dụng và cập nhật:

- Địa chỉ, hotline, email
- Link Zalo, Facebook, Messenger
- Link nhúng Google Maps
- Học phí, giảng viên và lịch khai giảng thực tế

## Kiểm tra project

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
```

## Deploy cơ bản

Ví dụ với Render, Railway hoặc máy chủ Linux:

1. Tạo PostgreSQL managed database.
2. Khai báo `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` và các biến `DB_*`.
3. Build command:

   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```

4. Start command:

   ```bash
   gunicorn config.wsgi:application
   ```

5. Chạy một lần `python manage.py seed_data` và `python manage.py createsuperuser`.
6. Dùng dịch vụ lưu ảnh bền vững (S3/Cloudinary) khi deploy trên nền tảng có filesystem tạm thời.
7. Bật HTTPS và đặt `SECURE_SSL_REDIRECT=True`.

Khi chạy nhiều instance, nên chuyển giới hạn spam từ session sang Redis và cấu hình email/SMS để báo đăng ký mới cho tư vấn viên.

## Deploy nhanh bằng Render Blueprint

Repo đã có sẵn `render.yaml` ở thư mục cha và `build.sh` trong project để
Render tự tạo web service, PostgreSQL database, collect static và migrate.

1. Đưa toàn bộ thư mục này lên một GitHub repository.
2. Vào Render Dashboard, chọn **Blueprints** > **New Blueprint Instance**.
3. Chọn repository vừa đẩy lên GitHub.
4. Render sẽ đọc `render.yaml` và tạo:
   - Web service `tan-hoang-huynh-hsk`
   - PostgreSQL database `tan-hoang-huynh-hsk-db`
   - `SECRET_KEY` tự sinh
   - `DATABASE_URL` tự nối vào database
5. Sau deploy đầu tiên, vào **Shell** của web service để tạo tài khoản quản trị:

   ```bash
   python manage.py createsuperuser
   ```

6. Nếu cần nạp dữ liệu mẫu, chạy thêm:

   ```bash
   python manage.py seed_data
   ```

Website sẽ có URL dạng `https://ten-service.onrender.com/`. Nếu dùng tên miền
riêng, thêm domain trong Render rồi bổ sung domain đó vào `ALLOWED_HOSTS` và
`CSRF_TRUSTED_ORIGINS` nếu Render không tự nhận qua `RENDER_EXTERNAL_HOSTNAME`.
