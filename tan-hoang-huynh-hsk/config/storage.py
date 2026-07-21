import posixpath
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import Storage


class R2WorkerStorage(Storage):
    """Store media through an authenticated Cloudflare Worker R2 binding."""

    def __init__(
        self,
        endpoint_url=None,
        auth_key=None,
        public_base_url=None,
        location="media",
        timeout=30,
    ):
        self.endpoint_url = (endpoint_url or "").rstrip("/")
        self.auth_key = auth_key or ""
        self.public_base_url = (public_base_url or "").rstrip("/")
        self.location = (location or "").strip("/")
        self.timeout = int(timeout)

        missing = [
            name
            for name, value in (
                ("R2_WORKER_UPLOAD_URL", self.endpoint_url),
                ("R2_WORKER_AUTH_KEY", self.auth_key),
                ("R2_PUBLIC_BASE_URL", self.public_base_url),
            )
            if not value
        ]
        if missing:
            raise ImproperlyConfigured(
                "Thiếu biến môi trường lưu media qua Worker: " + ", ".join(missing)
            )

    def _object_name(self, name):
        clean_name = name.replace("\\", "/").lstrip("/")
        return posixpath.join(self.location, clean_name) if self.location else clean_name

    def _worker_url(self, name):
        return f"{self.endpoint_url}/{quote(self._object_name(name), safe='/')}"

    def _request(self, method, name, *, data=None, content_type=None):
        headers = {"Authorization": f"Bearer {self.auth_key}"}
        if content_type:
            headers["Content-Type"] = content_type
        request = Request(
            self._worker_url(name),
            data=data,
            headers=headers,
            method=method,
        )
        try:
            return urlopen(request, timeout=self.timeout)
        except HTTPError:
            raise
        except URLError as exc:
            raise OSError("Không thể kết nối dịch vụ lưu ảnh.") from exc

    def _open(self, name, mode="rb"):
        if mode not in {"r", "rb"}:
            raise ValueError("R2WorkerStorage chỉ hỗ trợ mở tệp ở chế độ đọc.")
        try:
            with urlopen(self.url(name), timeout=self.timeout) as response:
                return ContentFile(response.read(), name=name)
        except (HTTPError, URLError) as exc:
            raise OSError(f"Không thể đọc tệp media: {name}") from exc

    def _save(self, name, content):
        payload = b"".join(content.chunks())
        content_type = getattr(content, "content_type", None) or "application/octet-stream"
        with self._request(
            "PUT", name, data=payload, content_type=content_type
        ) as response:
            if response.status not in {200, 201, 204}:
                raise OSError("Dịch vụ lưu ảnh từ chối tệp tải lên.")
        return name

    def delete(self, name):
        try:
            with self._request("DELETE", name) as response:
                if response.status not in {200, 202, 204}:
                    raise OSError("Không thể xóa tệp media.")
        except HTTPError as exc:
            if exc.code != 404:
                raise

    def exists(self, name):
        try:
            with self._request("HEAD", name) as response:
                return response.status == 200
        except HTTPError as exc:
            if exc.code == 404:
                return False
            raise

    def size(self, name):
        with self._request("HEAD", name) as response:
            value = response.headers.get("Content-Length")
        if value is None:
            raise OSError("Dịch vụ lưu ảnh không trả về kích thước tệp.")
        return int(value)

    def url(self, name):
        object_name = quote(self._object_name(name), safe="/")
        return f"{self.public_base_url}/{object_name}"
