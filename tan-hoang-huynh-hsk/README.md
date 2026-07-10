# Website Trung tâm Tiếng Trung Tân Hoàng Huynh HSK

Website Django hoàn chỉnh cho trung tâm tiếng Trung và luyện thi HSK tại Bắc Ninh. Project gồm giao diện responsive, quản trị nội dung, tuyển sinh, xuất dữ liệu, SEO cơ bản và dữ liệu mẫu bằng tiếng Việt.

## Công nghệ

- Python 3.11+ và Django 5.2 LTS (bản vá bảo mật mới)
- SQLite cho demo; PostgreSQL cho production
- Django Templates, HTML, CSS, JavaScript và Bootstrap 5
- Pillow để quản lý ảnh; WhiteNoise để phục vụ static
- openpyxl để xuất danh sách tư vấn ra Excel
- django-axes để khóa đăng nhập sai nhiều lần
- django-otp để bật 2FA cho quản trị
- django-storages để lưu media trên S3/R2

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
`CENTER_SECONDARY_HOTLINE`, `CENTER_EMAIL`, `CENTER_ZALO_URL`, `CENTER_FACEBOOK_URL`,
`CENTER_MESSENGER_URL`, `CENTER_TIKTOK_URL` và `CENTER_MAP_EMBED_URL`. Facebook/Messenger/TikTok sẽ
không được hiển thị nếu chưa có URL thật, tránh đưa người dùng tới liên kết
chung hoặc liên kết không thuộc trung tâm.

Đăng ký tư vấn và đặt lịch học thử luôn được lưu trong trang quản trị
`/quan-tri/`. Để nhận thêm email báo học viên mới, cấu hình:

- `ADMISSION_NOTIFICATION_EMAILS`: email nhận thông báo, có thể nhập nhiều email cách nhau bằng dấu phẩy
- `EMAIL_BACKEND`: ví dụ `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`

Nếu SMTP lỗi, website vẫn lưu lead trong database và ghi log lỗi email để tư vấn
viên kiểm tra lại trong Render Logs.

Khi deploy trên Render Free và không dùng được Shell, có thể tạo hoặc cập nhật
tài khoản quản trị bằng biến môi trường:

- `DJANGO_SUPERUSER_USERNAME`: tên đăng nhập quản trị
- `DJANGO_SUPERUSER_EMAIL`: email quản trị
- `DJANGO_SUPERUSER_PASSWORD`: mật khẩu quản trị

Lệnh build sẽ tự chạy `python manage.py ensure_superuser` sau khi migrate.
Không lưu mật khẩu quản trị trực tiếp trong mã nguồn.

## Bảo mật quản trị

Website khóa brute-force đăng nhập bằng `django-axes`. Có thể điều chỉnh:

- `AXES_FAILURE_LIMIT`: số lần sai trước khi khóa, mặc định `5`
- `AXES_COOLOFF_MINUTES`: thời gian khóa, mặc định `60`

2FA cho trang quản trị dùng TOTP qua `django-otp`. Để tránh tự khóa tài khoản,
quy trình an toàn là:

1. Để `ADMIN_2FA_REQUIRED=False`.
2. Đăng nhập `/quan-tri/`.
3. Vào phần TOTP devices và tạo thiết bị cho tài khoản admin.
4. Quét mã/nhập secret bằng Google Authenticator, Microsoft Authenticator hoặc
   app TOTP tương đương.
5. Sau khi xác nhận thiết bị hoạt động, đặt `ADMIN_2FA_REQUIRED=True` trong
   Render Environment và redeploy.

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

Ảnh tải lên qua admin được lưu trong thư mục `media/` và được phục vụ qua đường
dẫn `/media/...`. Trên Render Free, filesystem của web service không bền vững
qua deploy/restart, vì vậy ảnh upload trực tiếp có thể cần tải lại sau deploy.
Khi vận hành lâu dài, nên chuyển ảnh upload sang dịch vụ lưu trữ bền vững như
S3 hoặc Cloudinary.

## Lưu media bền vững bằng S3 hoặc Cloudflare R2

Project hỗ trợ S3-compatible storage. Khi chưa cấu hình, `MEDIA_STORAGE=local`
và ảnh vẫn lưu trong `media/`. Để chuyển sang AWS S3 hoặc Cloudflare R2, đặt:

- `MEDIA_STORAGE=s3` hoặc `MEDIA_STORAGE=r2`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_REGION_NAME` (`auto` cho Cloudflare R2)
- `AWS_S3_ENDPOINT_URL` (bắt buộc với R2, ví dụ endpoint của account R2)
- `AWS_S3_CUSTOM_DOMAIN` nếu có domain public/CDN cho bucket
- `AWS_LOCATION=media`

Sau khi chuyển media ra R2/S3, ảnh upload qua admin sẽ còn sau deploy/restart.
Nếu đang dùng Cloudinary thay vì R2/S3, cần thay backend storage và biến môi
trường theo tài khoản Cloudinary riêng.

## Dữ liệu mẫu

`seed_data` chỉ dành cho local/demo. Khi `DEBUG=False`, lệnh này bị chặn để
tránh ghi đè dữ liệu thật. Chỉ bật `ALLOW_PRODUCTION_SEED_DATA=True` khi hiểu
rõ rủi ro và cần nạp lại dữ liệu chủ động.

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

5. Tạo tài khoản quản trị bằng `python manage.py createsuperuser`.
   Nếu không dùng được Shell, đặt `DJANGO_SUPERUSER_USERNAME`,
   `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` trong Render Environment
   rồi deploy lại để build tự tạo tài khoản quản trị.
6. Dùng dịch vụ lưu ảnh bền vững (S3/R2/Cloudinary) khi deploy trên nền tảng có filesystem tạm thời.
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

   Nếu gói Free không dùng được Shell, thêm các biến `DJANGO_SUPERUSER_USERNAME`,
   `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` vào Environment Group
   rồi deploy lại.

6. Chỉ nạp dữ liệu mẫu ở local/demo. Production mặc định chặn `seed_data`; nếu
   vẫn cần chạy thủ công, phải đặt `ALLOW_PRODUCTION_SEED_DATA=True`:

   ```bash
   python manage.py seed_data
   ```

Website sẽ có URL dạng `https://ten-service.onrender.com/`. Với domain chính
`tanhoanghuynhhsk.com`, thêm Custom Domain trong Render, trỏ DNS theo hướng dẫn
của Render, rồi dùng:

```text
ALLOWED_HOSTS=tanhoanghuynhhsk.com,www.tanhoanghuynhhsk.com
CSRF_TRUSTED_ORIGINS=https://tanhoanghuynhhsk.com,https://www.tanhoanghuynhhsk.com
```
