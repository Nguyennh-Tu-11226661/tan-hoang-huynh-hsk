# Checklist deploy website len Render

## 1. Chuan bi source

- [ ] Mo terminal tai thu muc:

  ```powershell
  C:\Users\nguye\Downloads\tan-hoang-huynh-hsk-source
  ```

- [ ] Kiem tra project co cac file sau:

  ```text
  render.yaml
  tan-hoang-huynh-hsk/build.sh
  tan-hoang-huynh-hsk/requirements.txt
  tan-hoang-huynh-hsk/manage.py
  ```

- [ ] Kiem tra local truoc khi day len GitHub:

  ```powershell
  cd tan-hoang-huynh-hsk
  .\.venv\Scripts\python.exe manage.py check
  ```

## 2. Day source len GitHub

- [ ] Tao repository moi tren GitHub, vi du:

  ```text
  tan-hoang-huynh-hsk
  ```

- [ ] Neu thu muc chua duoc git init, chay:

  ```powershell
  cd C:\Users\nguye\Downloads\tan-hoang-huynh-hsk-source
  git init
  git add .
  git commit -m "Prepare Render deployment"
  git branch -M main
  git remote add origin https://github.com/USERNAME/tan-hoang-huynh-hsk.git
  git push -u origin main
  ```

- [ ] Neu da co remote GitHub, chi can:

  ```powershell
  git add .
  git commit -m "Prepare Render deployment"
  git push
  ```

## 3. Tao Blueprint tren Render

- [ ] Vao Render Dashboard.
- [ ] Chon **Blueprints**.
- [ ] Chon **New Blueprint Instance**.
- [ ] Ket noi GitHub va chon repository vua push.
- [ ] Render se doc file `render.yaml` va tao:
  - Web service `tan-hoang-huynh-hsk`
  - PostgreSQL database `tan-hoang-huynh-hsk-db`
  - `SECRET_KEY` tu sinh
  - `DATABASE_URL` tu gan vao database
- [ ] Bam **Apply** va doi deploy hoan tat.

## 4. Thiet lap sau deploy dau tien

- [ ] Mo web service tren Render.
- [ ] Vao tab **Shell**.
- [ ] Tao tai khoan quan tri:

  ```bash
  python manage.py createsuperuser
  ```

- [ ] Nap du lieu mau neu can:

  ```bash
  python manage.py seed_data
  ```

## 5. Kiem tra website

- [ ] Mo URL Render dang:

  ```text
  https://tan-hoang-huynh-hsk.onrender.com/
  ```

- [ ] Kiem tra cac trang:
  - [ ] Trang chu `/`
  - [ ] Khoa hoc `/khoa-hoc/`
  - [ ] Lich khai giang `/lich-khai-giang/`
  - [ ] Lien he `/lien-he/`
  - [ ] Quan tri `/quan-tri/`

- [ ] Kiem tra tren dien thoai:
  - [ ] Menu mobile mo duoc
  - [ ] Nut goi/Zalo hien dung
  - [ ] Form tu van gui duoc
  - [ ] Mau xanh logo hien dung

## 6. Gan ten mien rieng neu co

- [ ] Trong Render, vao web service > **Settings** > **Custom Domains**.
- [ ] Them domain, vi du:

  ```text
  tanhoanghuynhhsk.vn
  www.tanhoanghuynhhsk.vn
  ```

- [ ] Cap nhat DNS theo huong dan Render.
- [ ] Neu can, them env vars:

  ```text
  ALLOWED_HOSTS=tanhoanghuynhhsk.vn,www.tanhoanghuynhhsk.vn
  CSRF_TRUSTED_ORIGINS=https://tanhoanghuynhhsk.vn,https://www.tanhoanghuynhhsk.vn
  ```

## 7. Luu y van hanh

- Render free instance co the ngu sau mot thoi gian khong truy cap, lan dau mo lai se cham.
- File upload trong `media/` tren Render free khong phu hop de luu anh lau dai. Neu website dung anh hoc vien that, nen dung Cloudinary/S3 hoac goi co persistent disk.
- Sau moi lan sua code, commit va push len GitHub, Render se tu deploy lai.
