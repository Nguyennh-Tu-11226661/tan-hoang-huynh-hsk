from django.db import migrations


def fix_banner_subtitle_typos(apps, schema_editor):
    Banner = apps.get_model("core", "Banner")
    for banner in Banner.objects.all():
        subtitle = banner.subtitle
        fixed = (
            subtitle.replace("cùn giáo viên", "cùng giáo viên")
            .replace("tại bắc ninh", "tại Bắc Ninh")
            .replace("tại Bắc ninh", "tại Bắc Ninh")
        )
        if fixed != subtitle:
            banner.subtitle = fixed
            banner.save(update_fields=["subtitle"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_polish_public_copy"),
    ]

    operations = [
        migrations.RunPython(fix_banner_subtitle_typos, migrations.RunPython.noop),
    ]
