from django.db import migrations, models


def apply_official_social_links(apps, schema_editor):
    ContactInfo = apps.get_model("core", "ContactInfo")
    center_name = "Trung tâm Tiếng Trung Tân Hoàng Huynh HSK"
    official_contact = {
        "center_name": center_name,
        "address": "Số 86 đường Nguyễn Gia Thiều, phường Suối Hoa, TP. Bắc Ninh",
        "hotline": "0988668596",
        "email": "tuvan@tanhoanghuynhhsk.vn",
        "zalo_url": "https://zalo.me/0988668596",
        "facebook_url": "https://www.facebook.com/profile.php?id=61578072303057",
        "messenger_url": "",
        "tiktok_url": "https://www.tiktok.com/@tanhoanghuynhhsk",
        "map_embed_url": "https://www.google.com/maps?q=So+86+Nguyen+Gia+Thieu,+Suoi+Hoa,+Bac+Ninh&output=embed",
        "working_hours": "Thứ 2–Chủ nhật: 08:00–21:00",
        "is_active": True,
    }

    contact, created = ContactInfo.objects.get_or_create(
        center_name=center_name,
        defaults=official_contact,
    )
    if created:
        return

    contact.facebook_url = official_contact["facebook_url"]
    contact.tiktok_url = official_contact["tiktok_url"]
    contact.save(update_fields=["facebook_url", "tiktok_url"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_contactinfo_optional_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactinfo",
            name="tiktok_url",
            field=models.URLField(blank=True, verbose_name="TikTok"),
        ),
        migrations.RunPython(apply_official_social_links, noop_reverse),
    ]
