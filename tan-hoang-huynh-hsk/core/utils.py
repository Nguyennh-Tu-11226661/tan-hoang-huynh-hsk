from django.utils.text import slugify


def vietnamese_slugify(value):
    """Giữ URL tiếng Việt dễ đọc bằng cách chuyển đ/Đ thành d trước slugify."""
    return slugify(value.replace("đ", "d").replace("Đ", "D"))
