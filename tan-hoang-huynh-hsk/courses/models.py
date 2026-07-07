from django.db import models
from django.urls import reverse
from core.utils import vietnamese_slugify


class Course(models.Model):
    title = models.CharField("Tên khóa học", max_length=180)
    slug = models.SlugField("Đường dẫn", max_length=200, unique=True, blank=True)
    level = models.CharField("Trình độ", max_length=80)
    short_description = models.CharField("Mô tả ngắn", max_length=255)
    description = models.TextField("Nội dung chi tiết")
    duration = models.CharField("Thời lượng", max_length=100)
    sessions = models.PositiveSmallIntegerField("Số buổi")
    class_size = models.CharField("Sĩ số", max_length=80, default="8–12 học viên")
    tuition = models.PositiveIntegerField("Học phí (VNĐ)")
    target_students = models.TextField("Đối tượng học")
    outcomes = models.TextField(
        "Kết quả đầu ra", help_text="Mỗi kết quả một dòng."
    )
    syllabus = models.TextField("Lộ trình học", help_text="Mỗi chặng một dòng.")
    image = models.ImageField("Ảnh khóa học", upload_to="courses/", blank=True)
    is_featured = models.BooleanField("Nổi bật", default=False)
    is_active = models.BooleanField("Đang tuyển sinh", default=True)
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Khóa học"
        verbose_name_plural = "Khóa học"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = vietnamese_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    @property
    def outcomes_list(self):
        return [line.strip() for line in self.outcomes.splitlines() if line.strip()]

    @property
    def syllabus_list(self):
        return [line.strip() for line in self.syllabus.splitlines() if line.strip()]


class ClassSchedule(models.Model):
    class Format(models.TextChoices):
        OFFLINE = "offline", "Học trực tiếp"
        ONLINE = "online", "Học online"
        HYBRID = "hybrid", "Linh hoạt"

    course = models.ForeignKey(
        Course, verbose_name="Khóa học", on_delete=models.CASCADE, related_name="schedules"
    )
    class_code = models.CharField("Mã lớp", max_length=30, unique=True)
    start_date = models.DateField("Ngày khai giảng")
    schedule_text = models.CharField("Lịch học", max_length=180)
    format = models.CharField("Hình thức", max_length=20, choices=Format.choices)
    seats_left = models.PositiveSmallIntegerField("Chỗ còn lại", default=10)
    teacher = models.CharField("Giảng viên", max_length=120)
    is_active = models.BooleanField("Đang nhận đăng ký", default=True)

    class Meta:
        ordering = ["start_date", "course__order"]
        verbose_name = "Lịch khai giảng"
        verbose_name_plural = "Lịch khai giảng"

    def __str__(self):
        return f"{self.class_code} – {self.course.title}"
