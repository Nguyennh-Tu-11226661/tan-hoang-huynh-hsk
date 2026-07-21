import hashlib
import posixpath
import warnings
from io import BytesIO

from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image, ImageOps, UnidentifiedImageError


def _validation_error(message):
    return ValidationError(message, code="invalid_web_image")


def _open_image(payload):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(BytesIO(payload))
            image.load()
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise _validation_error("Ảnh có độ phân giải quá lớn để xử lý an toàn.")
    except (UnidentifiedImageError, OSError, ValueError):
        raise _validation_error("Tệp tải lên không phải hình ảnh hợp lệ.")
    return image


def optimize_web_image(name, payload):
    if len(payload) > settings.MEDIA_IMAGE_MAX_SOURCE_BYTES:
        limit_mb = settings.MEDIA_IMAGE_MAX_SOURCE_BYTES // (1024 * 1024)
        raise _validation_error(f"Ảnh gốc phải nhỏ hơn hoặc bằng {limit_mb} MB.")

    image = _open_image(payload)
    if image.format not in settings.MEDIA_IMAGE_ALLOWED_FORMATS:
        raise _validation_error(
            "Định dạng ảnh này chưa thể chuyển sang chuẩn WebP của website."
        )

    if image.width * image.height > settings.MEDIA_IMAGE_MAX_PIXELS:
        raise _validation_error("Ảnh có quá nhiều điểm ảnh để xử lý an toàn.")

    image = ImageOps.exif_transpose(image)
    image.thumbnail(
        (settings.MEDIA_IMAGE_MAX_DIMENSION, settings.MEDIA_IMAGE_MAX_DIMENSION),
        Image.Resampling.LANCZOS,
    )

    has_alpha = image.mode in {"RGBA", "LA"} or (
        image.mode == "P" and "transparency" in image.info
    )
    image = image.convert("RGBA" if has_alpha else "RGB")

    quality = settings.MEDIA_IMAGE_WEBP_QUALITY
    output = BytesIO()
    while True:
        output.seek(0)
        output.truncate(0)
        image.save(output, format="WEBP", quality=quality, method=6)
        if output.tell() <= settings.MEDIA_IMAGE_MAX_STORED_BYTES or quality <= 54:
            break
        quality -= 8

    while (
        output.tell() > settings.MEDIA_IMAGE_MAX_STORED_BYTES
        and max(image.size) > 900
    ):
        image.thumbnail(
            (int(image.width * 0.85), int(image.height * 0.85)),
            Image.Resampling.LANCZOS,
        )
        output.seek(0)
        output.truncate(0)
        image.save(output, format="WEBP", quality=max(quality, 54), method=6)

    optimized_payload = output.getvalue()
    if len(optimized_payload) > settings.MEDIA_IMAGE_MAX_STORED_BYTES:
        raise _validation_error("Không thể tối ưu ảnh xuống dung lượng website cho phép.")

    directory, filename = posixpath.split(name.replace("\\", "/"))
    stem, _extension = posixpath.splitext(filename)
    digest = hashlib.sha256(optimized_payload).hexdigest()[:12]
    optimized_filename = f"{stem[:55]}-{digest}.webp"
    optimized_name = posixpath.join(directory, optimized_filename)
    return optimized_name, optimized_payload, "image/webp"


def validate_web_image(uploaded_file):
    position = uploaded_file.tell() if hasattr(uploaded_file, "tell") else 0
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        payload = uploaded_file.read()
        optimize_web_image(uploaded_file.name, payload)
    finally:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(position)
