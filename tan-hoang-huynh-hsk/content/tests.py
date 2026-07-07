from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost, GalleryImage, Testimonial


class PublicContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = BlogPost.objects.create(
            title="Cách học từ vựng HSK hiệu quả",
            slug="cach-hoc-tu-vung-hsk",
            excerpt="Phương pháp học từ theo ngữ cảnh.",
            content="Học theo cụm từ.\nÔn tập ngắt quãng.",
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        Testimonial.objects.create(
            student_name="Nguyễn Minh Anh",
            course_name="HSK 3",
            content="Giáo viên chữa bài rất kỹ.",
            is_active=True,
        )
        GalleryImage.objects.create(
            title="Lớp luyện nói",
            caption="Học viên luyện phản xạ theo cặp.",
            is_active=True,
        )

    def test_public_content_pages_render(self):
        for name in [
            "content:blog_list",
            "content:testimonials",
            "content:gallery",
        ]:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_published_blog_detail_renders(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_draft_blog_is_not_public(self):
        self.post.status = BlogPost.Status.DRAFT
        self.post.save()
        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 404)
