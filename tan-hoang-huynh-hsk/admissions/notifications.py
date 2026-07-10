import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


logger = logging.getLogger(__name__)


def _recipients():
    return getattr(settings, "ADMISSION_NOTIFICATION_EMAILS", [])


def _send_notification(subject, lines):
    recipients = _recipients()
    if not recipients:
        return 0

    try:
        return send_mail(
            subject=subject,
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
    except Exception:
        logger.exception("Không gửi được email tuyển sinh: %s", subject)
        return 0


def notify_consultation_request(request):
    course = request.course.title if request.course else "Cần tư vấn lộ trình"
    created_at = timezone.localtime(request.created_at).strftime("%d/%m/%Y %H:%M")
    return _send_notification(
        "[Tân Hoàng Huynh HSK] Đăng ký tư vấn mới",
        [
            "Có học viên vừa đăng ký tư vấn trên website.",
            "",
            f"Họ tên: {request.full_name}",
            f"Số điện thoại: {request.phone}",
            f"Email: {request.email or 'Không cung cấp'}",
            f"Khóa học quan tâm: {course}",
            f"Trình độ hiện tại: {request.current_level or 'Chưa cung cấp'}",
            f"Thời gian thuận tiện: {request.preferred_time or 'Chưa cung cấp'}",
            f"Lời nhắn: {request.message or 'Không có'}",
            f"Thời gian gửi: {created_at}",
            "",
            "Vào trang quản trị /quan-tri/ để cập nhật trạng thái chăm sóc.",
        ],
    )


def notify_trial_booking(booking):
    created_at = timezone.localtime(booking.created_at).strftime("%d/%m/%Y %H:%M")
    preferred_date = booking.preferred_date.strftime("%d/%m/%Y")
    return _send_notification(
        "[Tân Hoàng Huynh HSK] Đặt lịch học thử/test mới",
        [
            "Có học viên vừa đặt lịch học thử hoặc test đầu vào trên website.",
            "",
            f"Họ tên: {booking.full_name}",
            f"Số điện thoại: {booking.phone}",
            f"Email: {booking.email or 'Không cung cấp'}",
            f"Nhu cầu: {booking.get_booking_type_display()}",
            f"Ngày mong muốn: {preferred_date}",
            f"Khung giờ: {booking.preferred_slot}",
            f"Trình độ hiện tại: {booking.current_level or 'Chưa cung cấp'}",
            f"Mục tiêu: {booking.goal or 'Chưa cung cấp'}",
            f"Thời gian gửi: {created_at}",
            "",
            "Vào trang quản trị /quan-tri/ để xác nhận lịch hẹn.",
        ],
    )
