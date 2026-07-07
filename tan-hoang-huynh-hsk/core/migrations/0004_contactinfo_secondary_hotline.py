import django.core.validators
from django.db import migrations, models


def apply_official_contact_details(apps, schema_editor):
    ContactInfo = apps.get_model("core", "ContactInfo")
    center_name = "Trung tâm Tiếng Trung Tân Hoàng Huynh HSK"
    contact_defaults = {
        "center_name": center_name,
        "address": "198 Lý Anh Tông, phường Võ Cường, TP. Bắc Ninh",
        "hotline": "0829304304",
        "secondary_hotline": "0886056556",
        "email": "tuvan@tanhoanghuynhhsk.vn",
        "zalo_url": "https://zalo.me/0829304304",
        "facebook_url": "https://www.facebook.com/profile.php?id=61578072303057",
        "messenger_url": "",
        "tiktok_url": "https://www.tiktok.com/@tanhoanghuynhhsk",
        "map_embed_url": "https://www.google.com/maps?q=198+Ly+Anh+Tong,+Vo+Cuong,+Bac+Ninh&output=embed",
        "working_hours": "Thứ 2–Chủ nhật: 08:00–21:00",
        "is_active": True,
    }

    contact, _ = ContactInfo.objects.get_or_create(
        center_name=center_name,
        defaults=contact_defaults,
    )
    for field, value in contact_defaults.items():
        setattr(contact, field, value)
    contact.save()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_contactinfo_tiktok_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactinfo",
            name="secondary_hotline",
            field=models.CharField(
                blank=True,
                default="",
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Số điện thoại chưa đúng định dạng Việt Nam.",
                        regex="^(0|\\+84)[0-9]{9,10}$",
                    )
                ],
                verbose_name="Hotline phụ",
            ),
        ),
        migrations.RunPython(apply_official_contact_details, noop_reverse),
    ]
