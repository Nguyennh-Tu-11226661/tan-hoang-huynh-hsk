from django.db import models

from core.models import phone_validator
from courses.models import Course


class ConsultationRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Mới"
        CONTACTED = "contacted", "Đã liên hệ"
        ENROLLED = "enrolled", "Đã nhập học"
        CLOSED = "closed", "Đã đóng"

    full_name = models.CharField("Họ và tên", max_length=120)
    phone = models.CharField("Số điện thoại", max_length=20, validators=[phone_validator])
    email = models.EmailField("Email", blank=True)
    course = models.ForeignKey(
        Course,
        verbose_name="Khóa học quan tâm",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    current_level = models.CharField("Trình độ hiện tại", max_length=120, blank=True)
    preferred_time = models.CharField("Thời gian thuận tiện", max_length=180, blank=True)
    message = models.TextField("Lời nhắn", blank=True)
    status = models.CharField(
        "Trạng thái", max_length=20, choices=Status.choices, default=Status.NEW
    )
    admin_note = models.TextField("Ghi chú nội bộ", blank=True)
    created_at = models.DateTimeField("Ngày đăng ký", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Đăng ký tư vấn"
        verbose_name_plural = "Đăng ký tư vấn"

    def __str__(self):
        return f"{self.full_name} – {self.phone}"


class TrialLessonBooking(models.Model):
    class BookingType(models.TextChoices):
        TRIAL = "trial", "Học thử"
        PLACEMENT = "placement", "Test đầu vào"

    class Status(models.TextChoices):
        NEW = "new", "Chờ xác nhận"
        CONFIRMED = "confirmed", "Đã xác nhận"
        COMPLETED = "completed", "Đã tham gia"
        CANCELLED = "cancelled", "Đã hủy"

    full_name = models.CharField("Họ và tên", max_length=120)
    phone = models.CharField("Số điện thoại", max_length=20, validators=[phone_validator])
    email = models.EmailField("Email", blank=True)
    booking_type = models.CharField(
        "Nhu cầu", max_length=20, choices=BookingType.choices
    )
    preferred_date = models.DateField("Ngày mong muốn")
    preferred_slot = models.CharField("Khung giờ", max_length=80)
    current_level = models.CharField("Trình độ hiện tại", max_length=120, blank=True)
    goal = models.TextField("Mục tiêu học tập", blank=True)
    status = models.CharField(
        "Trạng thái", max_length=20, choices=Status.choices, default=Status.NEW
    )
    admin_note = models.TextField("Ghi chú nội bộ", blank=True)
    created_at = models.DateTimeField("Ngày đặt lịch", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Lịch học thử / test"
        verbose_name_plural = "Lịch học thử / test"

    def __str__(self):
        return f"{self.full_name} – {self.get_booking_type_display()}"
