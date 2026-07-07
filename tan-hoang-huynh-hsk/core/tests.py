import tempfile

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from content.models import BlogPost, GalleryImage
from courses.models import Course

from .models import Banner, ContactInfo, FAQ


class PublicPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ContactInfo.objects.create(
            center_name="Tân Hoàng Huynh HSK",
            address="Bắc Ninh",
            hotline="0988668596",
            email="test@example.com",
            zalo_url="https://zalo.me/0988668596",
            facebook_url="https://facebook.com/example",
            messenger_url="https://m.me/example",
            map_embed_url="https://www.google.com/maps?q=Bac+Ninh&output=embed",
            working_hours="08:00–21:00",
        )
        FAQ.objects.create(question="Có học thử không?", answer="Có.")
        Banner.objects.create(
            title="Banner do Admin quản lý",
            subtitle="Nội dung banner tùy chỉnh.",
            button_text="Kiểm tra trình độ",
            button_url="/dat-lich-hoc-thu/",
        )

    def test_core_pages_render(self):
        for name in ["core:home", "core:about", "core:faq", "core:contact"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_sitemap_renders(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<urlset", status_code=200)

    def test_robots_points_to_sitemap(self):
        response = self.client.get(reverse("core:robots"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/sitemap.xml")

    def test_home_uses_banner_button_from_admin(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Banner do Admin quản lý")
        self.assertContains(response, "Kiểm tra trình độ")
        self.assertContains(response, 'href="/dat-lich-hoc-thu/"')

    def test_empty_optional_social_links_are_not_rendered(self):
        contact = ContactInfo.objects.first()
        contact.facebook_url = ""
        contact.messenger_url = ""
        contact.save()

        response = self.client.get(reverse("core:contact"))
        self.assertNotContains(response, 'href=""')
        self.assertNotContains(response, ">Messenger</a>")

    def test_seed_data_creates_media_backed_demo_content(self):
        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                call_command("seed_data", verbosity=0)

                banner = Banner.objects.get(
                    title="Vững tiếng Trung, rộng đường tương lai"
                )
                self.assertTrue(banner.image)
                self.assertTrue(banner.image.storage.exists(banner.image.name))
                self.assertEqual(GalleryImage.objects.exclude(image="").count(), 5)
                self.assertEqual(Course.objects.exclude(image="").count(), 12)
                self.assertEqual(BlogPost.objects.exclude(featured_image="").count(), 4)
