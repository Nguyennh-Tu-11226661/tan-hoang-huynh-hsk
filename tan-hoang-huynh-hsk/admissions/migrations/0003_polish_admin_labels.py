from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admissions", "0002_store_privacy_consent"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="triallessonbooking",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Lịch học thử / kiểm tra đầu vào",
                "verbose_name_plural": "Lịch học thử / kiểm tra đầu vào",
            },
        ),
        migrations.AlterField(
            model_name="triallessonbooking",
            name="booking_type",
            field=models.CharField(
                choices=[
                    ("trial", "Học thử"),
                    ("placement", "Kiểm tra đầu vào"),
                ],
                max_length=20,
                verbose_name="Nhu cầu",
            ),
        ),
    ]
