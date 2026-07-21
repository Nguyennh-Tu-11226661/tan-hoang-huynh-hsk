from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings
from PIL import Image

from config.image_pipeline import optimize_web_image, validate_web_image


class ImagePipelineTests(SimpleTestCase):
    @staticmethod
    def make_image(size=(400, 200), image_format="PNG"):
        source = BytesIO()
        Image.new("RGB", size, "orange").save(source, format=image_format)
        return source.getvalue()

    @override_settings(
        MEDIA_IMAGE_ALLOWED_FORMATS={"JPEG", "PNG", "WEBP"},
        MEDIA_IMAGE_MAX_SOURCE_BYTES=1024 * 1024,
        MEDIA_IMAGE_MAX_PIXELS=1_000_000,
        MEDIA_IMAGE_MAX_DIMENSION=100,
        MEDIA_IMAGE_WEBP_QUALITY=82,
        MEDIA_IMAGE_MAX_STORED_BYTES=200_000,
    )
    def test_optimizes_to_bounded_webp(self):
        name, payload, content_type = optimize_web_image(
            "gallery/anh lop hoc.png",
            self.make_image(),
        )

        self.assertRegex(name, r"^gallery/anh lop hoc-[0-9a-f]{12}\.webp$")
        self.assertEqual(content_type, "image/webp")
        self.assertLessEqual(len(payload), 200_000)
        with Image.open(BytesIO(payload)) as optimized:
            self.assertEqual(optimized.format, "WEBP")
            self.assertLessEqual(max(optimized.size), 100)

    def test_validator_rejects_non_image_content(self):
        invalid = ContentFile(b"not-an-image", name="fake.jpg")

        with self.assertRaisesMessage(ValidationError, "không phải hình ảnh"):
            validate_web_image(invalid)

    @override_settings(
        MEDIA_IMAGE_ALLOWED_FORMATS={"JPEG", "PNG", "WEBP", "GIF", "BMP", "TIFF"},
        MEDIA_IMAGE_MAX_SOURCE_BYTES=1024 * 1024,
        MEDIA_IMAGE_MAX_PIXELS=1_000_000,
        MEDIA_IMAGE_MAX_DIMENSION=120,
        MEDIA_IMAGE_WEBP_QUALITY=82,
        MEDIA_IMAGE_MAX_STORED_BYTES=200_000,
    )
    def test_converts_a_different_source_format_to_webp(self):
        name, payload, content_type = optimize_web_image(
            "gallery/anh-nguon.bmp",
            self.make_image(image_format="BMP"),
        )

        self.assertTrue(name.endswith(".webp"))
        self.assertEqual(content_type, "image/webp")
        with Image.open(BytesIO(payload)) as optimized:
            self.assertEqual(optimized.format, "WEBP")
