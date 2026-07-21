from django.core.validators import RegexValidator
from django.db import models
from config.image_pipeline import validate_web_image


phone_validator = RegexValidator(
    regex=r"^(0|\+84)[0-9]{9,10}$",
    message="Số điện thoại chưa đúng định dạng Việt Nam.",
)


class Banner(models.Model):
    title = models.CharField("Tiêu đề", max_length=180)
    subtitle = models.TextField("Mô tả ngắn")
    image = models.ImageField(
        "Ảnh banner",
        upload_to="banners/",
        blank=True,
        validators=[validate_web_image],
    )
    button_text = models.CharField("Nhãn nút", max_length=50, default="Đăng ký học thử")
    button_url = models.CharField("Đường dẫn nút", max_length=255, default="/dat-lich-hoc-thu/")
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)
    is_active = models.BooleanField("Đang hiển thị", default=True)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "Banner trang chủ"
        verbose_name_plural = "Banner trang chủ"

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField("Câu hỏi", max_length=255)
    answer = models.TextField("Câu trả lời")
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)
    is_active = models.BooleanField("Đang hiển thị", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Câu hỏi thường gặp"
        verbose_name_plural = "Câu hỏi thường gặp"

    def __str__(self):
        return self.question


class ContactInfo(models.Model):
    center_name = models.CharField("Tên trung tâm", max_length=180)
    address = models.CharField("Địa chỉ", max_length=255)
    hotline = models.CharField("Hotline", max_length=20, validators=[phone_validator])
    secondary_hotline = models.CharField(
        "Hotline phụ", max_length=20, blank=True, default="", validators=[phone_validator]
    )
    email = models.EmailField("Email")
    zalo_url = models.URLField("Zalo", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    messenger_url = models.URLField("Messenger", blank=True)
    tiktok_url = models.URLField("TikTok", blank=True)
    map_embed_url = models.URLField("Link nhúng Google Maps", max_length=1000, blank=True)
    working_hours = models.CharField("Giờ làm việc", max_length=255)
    is_active = models.BooleanField("Đang sử dụng", default=True)

    class Meta:
        verbose_name = "Thông tin liên hệ"
        verbose_name_plural = "Thông tin liên hệ"

    def __str__(self):
        return self.center_name

    @staticmethod
    def _clean_phone(value):
        return "".join(char for char in value if char.isdigit() or char == "+")

    @staticmethod
    def _format_phone(value):
        cleaned = ContactInfo._clean_phone(value)
        if cleaned.startswith("+84") and len(cleaned) == 12:
            cleaned = "0" + cleaned[3:]
        if len(cleaned) == 10 and cleaned.startswith("0"):
            return f"{cleaned[:4]}.{cleaned[4:7]}.{cleaned[7:]}"
        return value

    @property
    def hotline_tel(self):
        return self._clean_phone(self.hotline)

    @property
    def secondary_hotline_tel(self):
        return self._clean_phone(self.secondary_hotline)

    @property
    def hotline_display(self):
        return self._format_phone(self.hotline)

    @property
    def secondary_hotline_display(self):
        return self._format_phone(self.secondary_hotline)

    @property
    def phone_display(self):
        return " - ".join(
            phone
            for phone in [self.hotline_display, self.secondary_hotline_display]
            if phone
        )
