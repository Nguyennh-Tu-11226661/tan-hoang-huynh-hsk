from django.conf import settings
from django.contrib import admin


def configure_admin_site():
    if not settings.ADMIN_2FA_REQUIRED:
        return

    from django_otp.admin import OTPAdminSite

    admin.site = OTPAdminSite(name="admin")
