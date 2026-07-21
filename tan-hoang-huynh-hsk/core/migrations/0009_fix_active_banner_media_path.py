from django.db import migrations


def fix_active_banner_path(apps, schema_editor):
    Banner = apps.get_model("core", "Banner")
    Banner.objects.filter(is_active=True).update(
        image="banners/lop-tieng-trung-giao-tiep-hsk.jpg"
    )


def reverse_active_banner_path(apps, schema_editor):
    Banner = apps.get_model("core", "Banner")
    Banner.objects.filter(is_active=True).update(
        image="banners/Gemini_Generated_Image_muxatomuxatomuxa.png"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_restore_production_banner_path"),
    ]

    operations = [
        migrations.RunPython(fix_active_banner_path, reverse_active_banner_path),
    ]
