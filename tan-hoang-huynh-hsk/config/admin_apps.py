from axes.apps import AppConfig as AxesConfig
from django.apps import apps
from django.contrib.admin.apps import AdminConfig
from django_otp.plugins.otp_totp.apps import DefaultConfig as OTP_TOTPConfig


class SecureAdminConfig(AdminConfig):
    default_site = "config.admin_site.SecureAdminSite"


class VietnameseAxesConfig(AxesConfig):
    verbose_name = "Bảo mật đăng nhập"

    def ready(self):
        super().ready()
        rename_model("axes", "AccessAttempt", "Lần đăng nhập", "Lần đăng nhập")
        rename_model("axes", "AccessFailureLog", "Lỗi đăng nhập", "Lỗi đăng nhập")
        rename_model("axes", "AccessLog", "Nhật ký truy cập", "Nhật ký truy cập")


class VietnameseTOTPConfig(OTP_TOTPConfig):
    verbose_name = "Xác thực 2 lớp"

    def ready(self):
        super().ready()
        rename_model(
            "otp_totp",
            "TOTPDevice",
            "Thiết bị OTP",
            "Thiết bị OTP",
        )


def rename_model(app_label, model_name, verbose_name, verbose_name_plural):
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        return
    model._meta.verbose_name = verbose_name
    model._meta.verbose_name_plural = verbose_name_plural
