from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from django.core.files.base import ContentFile
from PIL import Image
from config.storage import R2WorkerStorage


class R2WorkerStorageTests(TestCase):
    def setUp(self):
        self.storage = R2WorkerStorage(
            endpoint_url="https://media-upload.example.workers.dev",
            auth_key="test-secret",
            public_base_url="https://public.example.test",
            location="media",
        )

    @patch("config.storage.urlopen")
    def test_save_uses_authenticated_worker(self, mocked_urlopen):
        response = Mock(status=201)
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        mocked_urlopen.return_value = response

        source = BytesIO()
        Image.new("RGB", (120, 80), "navy").save(source, format="JPEG")
        content = ContentFile(source.getvalue(), name="anh co dau cach.jpg")
        content.content_type = "image/jpeg"

        saved_name = self.storage.save("blog/anh co dau cach.jpg", content)

        self.assertRegex(
            saved_name,
            r"^blog/anh co dau cach-[0-9a-f]{12}\.webp$",
        )
        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "PUT")
        self.assertRegex(
            request.full_url,
            r"^https://media-upload\.example\.workers\.dev/media/blog/"
            r"anh%20co%20dau%20cach-[0-9a-f]{12}\.webp$",
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(
            request.get_header("User-agent"), "tan-hoang-huynh-hsk-media/1.0"
        )
        self.assertEqual(request.get_header("Content-type"), "image/webp")

    @patch("config.storage.urlopen")
    def test_exists_returns_false_for_missing_object(self, mocked_urlopen):
        mocked_urlopen.side_effect = HTTPError(
            self.storage._worker_url("missing.jpg"), 404, "Not found", {}, None
        )

        self.assertFalse(self.storage.exists("missing.jpg"))

    def test_public_url_includes_location(self):
        self.assertEqual(
            self.storage.url("gallery/a b.jpg"),
            "https://public.example.test/media/gallery/a%20b.jpg",
        )
