from django.db import migrations


def align_contact_domain(apps, schema_editor):
    ContactInfo = apps.get_model("core", "ContactInfo")
    ContactInfo.objects.filter(email="tuvan@tanhoanghuynhhsk.vn").update(
        email="tuvan@tanhoanghuynhhsk.com"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_fix_banner_subtitle_typos"),
    ]

    operations = [
        migrations.RunPython(align_contact_domain, migrations.RunPython.noop),
    ]
