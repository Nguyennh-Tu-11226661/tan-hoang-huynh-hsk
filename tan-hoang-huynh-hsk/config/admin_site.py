from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django_otp.admin import OTPAdminSite


APP_HELP = {
    "axes": "Theo dõi đăng nhập sai và khóa brute-force. Không làm thay đổi nội dung hiển thị trên website.",
    "otp_totp": "Quản lý thiết bị xác thực 2 lớp cho tài khoản quản trị. Thêm/xóa ở đây chỉ ảnh hưởng đăng nhập admin.",
    "courses": "Quản lý khóa học và lịch khai giảng hiển thị trên Trang chủ, Khóa học và Khai giảng.",
    "content": "Quản lý bài viết, cảm nhận học viên và thư viện hiển thị ở Góc học tập, Thành tích và Thư viện.",
    "core": "Quản lý banner, FAQ và thông tin liên hệ hiển thị ở Trang chủ, Footer, Liên hệ và Câu hỏi thường gặp.",
    "admissions": "Quản lý dữ liệu học viên gửi form. Các mục này không hiển thị công khai trên website.",
    "auth": "Quản lý tài khoản và nhóm quyền truy cập trang quản trị.",
}

MODEL_HELP = {
    "Course": "Thêm/sửa/xóa sẽ ảnh hưởng trang Khóa học, Trang chủ và trang chi tiết từng khóa.",
    "ClassSchedule": "Thêm/sửa/xóa sẽ ảnh hưởng mục Khai giảng và phần lớp sắp khai giảng trên Trang chủ.",
    "BlogPost": "Bài đã xuất bản sẽ hiển thị ở Góc học tập và trang chi tiết bài viết.",
    "Testimonial": "Cảm nhận học viên đang hiển thị sẽ xuất hiện ở Trang chủ và trang Thành tích.",
    "GalleryImage": "Ảnh/video đang hiển thị sẽ xuất hiện ở trang Thư viện.",
    "Banner": "Banner đang bật sẽ hiển thị ở phần đầu Trang chủ.",
    "FAQ": "Câu hỏi đang bật sẽ hiển thị ở trang Câu hỏi thường gặp.",
    "ContactInfo": "Thông tin đang sử dụng sẽ hiển thị ở Footer, trang Liên hệ và các nút gọi/Zalo.",
    "ConsultationRequest": "Dữ liệu từ form tư vấn. Đổi trạng thái chỉ phục vụ chăm sóc học viên, không hiện ngoài website.",
    "TrialLessonBooking": "Dữ liệu từ form học thử/kiểm tra đầu vào. Đổi trạng thái chỉ phục vụ xác nhận lịch, không hiện ngoài website.",
    "User": "Tạo/xóa tài khoản đăng nhập trang quản trị. Không hiển thị công khai.",
    "Group": "Quản lý nhóm quyền cho nhân viên trong trang quản trị.",
    "AccessAttempt": "Xem hoặc xóa dấu vết đăng nhập sai. Không ảnh hưởng nội dung website.",
    "AccessFailureLog": "Nhật ký lỗi đăng nhập để kiểm tra bảo mật quản trị.",
    "AccessLog": "Nhật ký truy cập đăng nhập quản trị.",
    "TOTPDevice": "Thiết bị mã OTP của admin. Xóa mục này sẽ làm tài khoản đó mất 2FA đã cấu hình.",
}


class SecureAdminSite(OTPAdminSite):
    """Use one admin registry while optionally enforcing verified OTP sessions."""

    def has_permission(self, request):
        if settings.ADMIN_2FA_REQUIRED:
            return super().has_permission(request)
        return AdminSite.has_permission(self, request)


def configure_admin_site():
    patch_admin_help(admin.site)


def patch_admin_help(site):
    if getattr(site, "_tan_hoang_help_patched", False):
        return

    original_get_app_list = site.get_app_list

    def get_app_list(request, app_label=None):
        app_list = original_get_app_list(request, app_label)
        for app in app_list:
            app["description"] = APP_HELP.get(app["app_label"], "")
            for model in app.get("models", []):
                model["description"] = MODEL_HELP.get(model["object_name"], "")
        return app_list

    site.get_app_list = get_app_list
    site._tan_hoang_help_patched = True
