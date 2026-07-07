from django.test import TestCase
from django.urls import reverse

from .models import Course


class CoursePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(
            title="Chinh phục HSK 3",
            slug="hsk-3",
            level="HSK 3",
            short_description="Luyện thi HSK tại Bắc Ninh.",
            description="Nội dung",
            duration="4 tháng",
            sessions=40,
            tuition=4000000,
            target_students="Người đã học HSK 2",
            outcomes="Nghe tốt\nĐọc tốt",
            syllabus="Nền tảng\nLuyện đề",
            is_active=True,
        )

    def test_course_list_and_detail_render(self):
        self.assertEqual(self.client.get(reverse("courses:list")).status_code, 200)
        response = self.client.get(self.course.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chinh phục HSK 3")

    def test_inactive_course_is_not_public(self):
        self.course.is_active = False
        self.course.save()
        self.assertEqual(self.client.get(self.course.get_absolute_url()).status_code, 404)
