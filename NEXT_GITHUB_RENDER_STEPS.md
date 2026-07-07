# Buoc tiep theo de dua website len GitHub va Render

Trang thai hien tai:

- Code da duoc commit local.
- Commit hien tai: `1654479 Prepare Render deployment`
- Branch hien tai: `main`
- Remote hien tai van la placeholder:

  ```text
  https://github.com/USERNAME/tan-hoang-huynh-hsk.git
  ```

## Cach 1: Tao repo GitHub thu cong roi de Codex push tiep

1. Vao GitHub va tao repository moi:

   ```text
   tan-hoang-huynh-hsk
   ```

2. Khong can them README, .gitignore hoac license tren GitHub.

3. Copy URL repo, vi du:

   ```text
   https://github.com/nguyenanhtu1113/tan-hoang-huynh-hsk.git
   ```

4. Gui URL do cho Codex.

5. Codex se chay:

   ```powershell
   git remote set-url origin <URL_REPO_THAT>
   git push -u origin main
   ```

## Cach 2: Cai GitHub CLI de Codex tao repo va push tu dong

1. Cai GitHub CLI:

   ```powershell
   winget install --id GitHub.cli
   ```

2. Dang nhap GitHub:

   ```powershell
   gh auth login
   ```

3. Sau khi dang nhap xong, bao Codex tiep tuc.

4. Codex co the tao repo va push bang:

   ```powershell
   gh repo create tan-hoang-huynh-hsk --private --source . --remote origin --push
   ```

## Sau khi code da len GitHub

1. Vao Render Dashboard.
2. Chon **Blueprints** > **New Blueprint Instance**.
3. Chon GitHub repo `tan-hoang-huynh-hsk`.
4. Render se tu doc `render.yaml`.
5. Bam **Apply** va doi deploy xong.
6. Vao Shell cua web service tren Render, chay:

   ```bash
   python manage.py createsuperuser
   python manage.py seed_data
   ```

7. Mo URL Render de kiem tra website.
