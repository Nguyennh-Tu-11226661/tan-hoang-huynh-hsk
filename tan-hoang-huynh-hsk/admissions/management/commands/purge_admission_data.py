from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from admissions.models import ConsultationRequest, TrialLessonBooking


class Command(BaseCommand):
    help = "Xóa dữ liệu tuyển sinh đã đóng và quá thời hạn lưu trữ."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=settings.ADMISSION_DATA_RETENTION_DAYS,
            help="Số ngày lưu dữ liệu đã đóng.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Chỉ thống kê, không xóa dữ liệu.",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Xác nhận thực hiện xóa vĩnh viễn.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        if days < 30:
            raise CommandError("Thời hạn lưu trữ phải từ 30 ngày trở lên.")
        if not options["dry_run"] and not options["confirm"]:
            raise CommandError("Dùng --dry-run để kiểm tra hoặc --confirm để xóa.")

        cutoff = timezone.now() - timedelta(days=days)
        consultations = ConsultationRequest.objects.filter(
            status=ConsultationRequest.Status.CLOSED,
            created_at__lt=cutoff,
        )
        bookings = TrialLessonBooking.objects.filter(
            status__in=[
                TrialLessonBooking.Status.COMPLETED,
                TrialLessonBooking.Status.CANCELLED,
            ],
            created_at__lt=cutoff,
        )
        consultation_count = consultations.count()
        booking_count = bookings.count()

        if options["dry_run"]:
            action = "Sẽ xóa"
        else:
            with transaction.atomic():
                consultations.delete()
                bookings.delete()
            action = "Đã xóa"

        self.stdout.write(
            f"{action} {consultation_count} đăng ký tư vấn và "
            f"{booking_count} lịch học thử/kiểm tra cũ hơn {days} ngày."
        )
