import tempfile
from unittest.mock import patch

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse
from django.views.static import serve
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.plugins.otp_totp.models import TOTPDevice

from admissions.models import ConsultationRequest
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

    def test_public_pages_do_not_show_seed_data_instructions(self):
        public_pages = [
            "core:home",
            "core:faq",
            "core:contact",
            "content:gallery",
        ]
        for name in public_pages:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertNotContains(response, "dữ liệu mẫu")
                self.assertNotContains(response, "chạy lệnh")

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
            with self.settings(DEBUG=True, MEDIA_ROOT=media_root):
                call_command("seed_data", verbosity=0)

                banner = Banner.objects.get(
                    title="Vững tiếng Trung, rộng đường tương lai"
                )
                self.assertTrue(banner.image)
                self.assertTrue(banner.image.storage.exists(banner.image.name))
                self.assertEqual(GalleryImage.objects.exclude(image="").count(), 5)
                self.assertEqual(Course.objects.exclude(image="").count(), 12)
                self.assertEqual(BlogPost.objects.exclude(featured_image="").count(), 4)

    def test_seed_data_is_blocked_in_production(self):
        with self.settings(DEBUG=False):
            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaises(CommandError):
                    call_command("seed_data", verbosity=0)

    def test_production_media_route_is_configured(self):
        from config.urls import urlpatterns

        media_routes = [
            pattern
            for pattern in urlpatterns
            if getattr(pattern, "callback", None) == serve
        ]
        self.assertTrue(media_routes)


class EnsureSuperuserCommandTests(TestCase):
    def test_command_creates_superuser_from_environment(self):
        with patch.dict(
            "os.environ",
            {
                "DJANGO_SUPERUSER_USERNAME": "admin",
                "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
                "DJANGO_SUPERUSER_PASSWORD": "StrongPassword123!",
            },
        ):
            call_command("ensure_superuser", verbosity=0)

        User = get_user_model()
        user = User.objects.get(username="admin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_command_skips_when_required_environment_is_missing(self):
        with patch.dict("os.environ", {}, clear=True):
            call_command("ensure_superuser", verbosity=0)

        User = get_user_model()
        self.assertFalse(User.objects.exists())


class AdminInterfaceTests(TestCase):
    def test_secure_admin_site_keeps_registered_models(self):
        self.assertIn(Course, admin.site._registry)
        self.assertIn(BlogPost, admin.site._registry)
        self.assertIn(ConsultationRequest, admin.site._registry)

    def test_admin_uses_custom_stylesheet(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="StrongPassword123!",
        )
        user = User.objects.get(username="admin")
        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin/css/tan-hoang-admin.css")
        self.assertContains(response, "Quản lý nội dung và tuyển sinh")
        self.assertContains(response, "Bảo mật đăng nhập")
        self.assertContains(response, "Xác thực 2 lớp")
        self.assertContains(response, "Quản lý khóa học và lịch khai giảng")
        self.assertContains(response, "Thêm/sửa/xóa sẽ ảnh hưởng trang Khóa học")
        self.assertEqual(response["Cache-Control"], "no-store, private")
        self.assertEqual(
            response["Permissions-Policy"],
            "camera=(), geolocation=(), microphone=()",
        )

    def test_custom_admin_stylesheet_exists(self):
        self.assertIsNotNone(finders.find("admin/css/tan-hoang-admin.css"))

    def test_admin_requires_verified_otp_when_enabled(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="secure-admin",
            email="secure-admin@example.com",
            password="StrongPassword123!",
        )
        device = TOTPDevice.objects.create(
            user=user,
            name="test-device",
            confirmed=True,
        )
        self.client.force_login(user)

        with self.settings(ADMIN_2FA_REQUIRED=True):
            unverified_response = self.client.get(reverse("admin:index"))
            self.assertRedirects(
                unverified_response,
                f'{reverse("admin:login")}?next={reverse("admin:index")}',
            )

            session = self.client.session
            session[DEVICE_ID_SESSION_KEY] = device.persistent_id
            session.save()
            verified_response = self.client.get(reverse("admin:index"))

        self.assertEqual(verified_response.status_code, 200)
        self.assertContains(verified_response, "Quản lý khóa học và lịch khai giảng")
