import time
from datetime import timedelta
from io import BytesIO

from django.core import signing
from django.core import mail
from django.test import RequestFactory, TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from openpyxl import load_workbook

from .admin import export_consultations_csv, export_consultations_excel
from .models import ConsultationRequest, TrialLessonBooking


class AdmissionFormTests(TestCase):
    def token(self):
        return signing.dumps(int(time.time()) - 3)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        ADMISSION_NOTIFICATION_EMAILS=["tuvan@example.com"],
    )
    def test_consultation_submission(self):
        response = self.client.post(
            reverse("admissions:consultation"),
            {
                "full_name": "Nguyễn Minh An",
                "phone": "0988668596",
                "email": "an@example.com",
                "current_level": "Người mới",
                "preferred_time": "Buổi tối",
                "message": "Muốn học HSK",
                "consent": "on",
                "website": "",
                "form_started": self.token(),
            },
        )
        self.assertRedirects(response, reverse("admissions:success"))
        self.assertEqual(ConsultationRequest.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Đăng ký tư vấn mới", mail.outbox[0].subject)

    def test_honeypot_blocks_spam(self):
        response = self.client.post(
            reverse("admissions:consultation"),
            {
                "full_name": "Spam Bot",
                "phone": "0988668596",
                "consent": "on",
                "website": "https://spam.example",
                "form_started": self.token(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultationRequest.objects.count(), 0)

    def test_trial_date_cannot_be_in_past(self):
        response = self.client.post(
            reverse("admissions:trial"),
            {
                "full_name": "Nguyễn Minh An",
                "phone": "0988668596",
                "booking_type": "trial",
                "preferred_date": (timezone.localdate() - timedelta(days=1)).isoformat(),
                "preferred_slot": "18:00–20:00",
                "consent": "on",
                "website": "",
                "form_started": self.token(),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TrialLessonBooking.objects.count(), 0)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        ADMISSION_NOTIFICATION_EMAILS=["tuvan@example.com"],
    )
    def test_trial_submission_saves_booking(self):
        response = self.client.post(
            reverse("admissions:trial"),
            {
                "full_name": "Nguyễn Minh An",
                "phone": "0988668596",
                "email": "an@example.com",
                "booking_type": "placement",
                "preferred_date": (timezone.localdate() + timedelta(days=1)).isoformat(),
                "preferred_slot": "18:00–20:00",
                "current_level": "Mất gốc",
                "goal": "Muốn học HSK 3",
                "consent": "on",
                "website": "",
                "form_started": self.token(),
            },
        )

        self.assertRedirects(response, reverse("admissions:success"))
        self.assertEqual(TrialLessonBooking.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Đặt lịch học thử/test mới", mail.outbox[0].subject)

    def test_rate_limit_blocks_immediate_second_submission(self):
        payload = {
            "full_name": "Nguyễn Minh An",
            "phone": "0988668596",
            "consent": "on",
            "website": "",
            "form_started": self.token(),
        }
        self.client.post(reverse("admissions:consultation"), payload)
        response = self.client.post(
            reverse("admissions:consultation"),
            {**payload, "form_started": self.token()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vui lòng chờ một phút")
        self.assertEqual(ConsultationRequest.objects.count(), 1)


class ConsultationExportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ConsultationRequest.objects.create(
            full_name="Nguyễn Minh An",
            phone="0988668596",
            email="an@example.com",
            current_level="Người mới",
            preferred_time="Buổi tối",
            message="Muốn học HSK",
        )

    def setUp(self):
        self.request = RequestFactory().get("/quan-tri/")
        self.queryset = ConsultationRequest.objects.all()

    def test_csv_export(self):
        response = export_consultations_csv(None, self.request, self.queryset)
        text = response.content.decode("utf-8-sig")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Nguyễn Minh An", text)
        self.assertIn("Số điện thoại", text)
        self.assertIn("dang-ky-tu-van.csv", response["Content-Disposition"])

    def test_excel_export(self):
        response = export_consultations_excel(None, self.request, self.queryset)
        workbook = load_workbook(BytesIO(response.content), read_only=True)
        sheet = workbook["Đăng ký tư vấn"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(sheet["A2"].value, "Nguyễn Minh An")
        self.assertEqual(sheet["B2"].value, "0988668596")
        self.assertIn("dang-ky-tu-van.xlsx", response["Content-Disposition"])
