from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admissions", "0003_polish_admin_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consultationrequest",
            name="consent_version",
            field=models.CharField(
                default="privacy-2026-07-20",
                max_length=40,
                verbose_name="Phiên bản đồng ý",
            ),
        ),
        migrations.AlterField(
            model_name="triallessonbooking",
            name="consent_version",
            field=models.CharField(
                default="privacy-2026-07-20",
                max_length=40,
                verbose_name="Phiên bản đồng ý",
            ),
        ),
    ]
