from django.db import migrations


BANNER_TITLE = "Lớp học tiếng trung giao tiếp HSK - Tân Hoàng Huynh HSK"


def restore_banner_path(apps, schema_editor):
    Banner = apps.get_model("core", "Banner")
    Banner.objects.filter(title=BANNER_TITLE).update(
        image="banners/lop-tieng-trung-giao-tiep-hsk.jpg"
    )


def reverse_banner_path(apps, schema_editor):
    Banner = apps.get_model("core", "Banner")
    Banner.objects.filter(title=BANNER_TITLE).update(
        image="banners/Gemini_Generated_Image_muxatomuxatomuxa.png"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_align_contact_domain"),
    ]

    operations = [
        migrations.RunPython(restore_banner_path, reverse_banner_path),
    ]
