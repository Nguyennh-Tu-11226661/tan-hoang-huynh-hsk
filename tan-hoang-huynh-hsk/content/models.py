from django.db import models
from django.urls import reverse
from core.utils import vietnamese_slugify


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Bản nháp"
        PUBLISHED = "published", "Đã xuất bản"

    title = models.CharField("Tiêu đề", max_length=220)
    slug = models.SlugField("Đường dẫn", max_length=240, unique=True, blank=True)
    excerpt = models.CharField("Mô tả ngắn", max_length=320)
    content = models.TextField("Nội dung")
    featured_image = models.ImageField("Ảnh đại diện", upload_to="blog/", blank=True)
    author_name = models.CharField("Tác giả", max_length=100, default="Ban học thuật")
    status = models.CharField(
        "Trạng thái", max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    published_at = models.DateTimeField("Ngày xuất bản", null=True, blank=True)
    meta_description = models.CharField("Meta description", max_length=160, blank=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Cập nhật", auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = vietnamese_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:blog_detail", kwargs={"slug": self.slug})

    @property
    def paragraphs(self):
        return [p.strip() for p in self.content.splitlines() if p.strip()]


class Testimonial(models.Model):
    student_name = models.CharField("Tên học viên", max_length=120)
    course_name = models.CharField("Khóa học / kết quả", max_length=180)
    content = models.TextField("Chia sẻ")
    score = models.CharField("Điểm HSK", max_length=80, blank=True)
    avatar = models.ImageField("Ảnh học viên", upload_to="testimonials/", blank=True)
    rating = models.PositiveSmallIntegerField("Đánh giá", default=5)
    is_featured = models.BooleanField("Nổi bật", default=False)
    is_active = models.BooleanField("Đang hiển thị", default=True)
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "Cảm nhận học viên"
        verbose_name_plural = "Cảm nhận học viên"

    def __str__(self):
        return self.student_name


class GalleryImage(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Hình ảnh"
        VIDEO = "video", "Video"

    title = models.CharField("Tiêu đề", max_length=180)
    image = models.ImageField("Hình ảnh", upload_to="gallery/", blank=True)
    media_type = models.CharField(
        "Loại nội dung", max_length=10, choices=MediaType.choices, default=MediaType.IMAGE
    )
    video_url = models.URLField("Link video", blank=True)
    caption = models.CharField("Chú thích", max_length=255, blank=True)
    event_date = models.DateField("Ngày diễn ra", null=True, blank=True)
    is_active = models.BooleanField("Đang hiển thị", default=True)
    order = models.PositiveSmallIntegerField("Thứ tự", default=0)

    class Meta:
        ordering = ["order", "-event_date", "-id"]
        verbose_name = "Thư viện ảnh / video"
        verbose_name_plural = "Thư viện ảnh / video"

    def __str__(self):
        return self.title
