from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Kiểm tra dịch vụ media bằng thao tác lưu, đọc trạng thái và xóa tệp thử."

    def handle(self, *args, **options):
        if settings.MEDIA_STORAGE != "r2_worker":
            self.stdout.write("Bỏ qua kiểm tra Worker vì MEDIA_STORAGE không phải r2_worker.")
            return

        probe_name = f"_healthchecks/deploy-{uuid4().hex}.txt"
        saved_name = None
        try:
            saved_name = default_storage.save(
                probe_name,
                ContentFile(b"media-storage-ok", name=probe_name),
            )
            if not default_storage.exists(saved_name):
                raise CommandError("Đã lưu tệp thử nhưng không thể kiểm tra lại tệp.")

            default_storage.delete(saved_name)
            if default_storage.exists(saved_name):
                raise CommandError("Đã yêu cầu xóa nhưng tệp thử vẫn còn tồn tại.")
        except CommandError:
            raise
        except Exception as exc:
            raise CommandError(f"Dịch vụ media không hoạt động: {exc}") from exc
        finally:
            if saved_name:
                try:
                    default_storage.delete(saved_name)
                except Exception:
                    pass

        self.stdout.write(self.style.SUCCESS("Dịch vụ media đã vượt qua kiểm tra lưu/đọc/xóa."))
