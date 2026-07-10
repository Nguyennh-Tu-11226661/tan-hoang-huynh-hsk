from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="consultationrequest",
            name="consent_given_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Thời điểm đồng ý xử lý dữ liệu",
            ),
        ),
        migrations.AddField(
            model_name="consultationrequest",
            name="consent_text",
            field=models.TextField(blank=True, verbose_name="Nội dung đồng ý"),
        ),
        migrations.AddField(
            model_name="consultationrequest",
            name="consent_version",
            field=models.CharField(
                default="privacy-2026-07-10",
                max_length=40,
                verbose_name="Phiên bản đồng ý",
            ),
        ),
        migrations.AddField(
            model_name="triallessonbooking",
            name="consent_given_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Thời điểm đồng ý xử lý dữ liệu",
            ),
        ),
        migrations.AddField(
            model_name="triallessonbooking",
            name="consent_text",
            field=models.TextField(blank=True, verbose_name="Nội dung đồng ý"),
        ),
        migrations.AddField(
            model_name="triallessonbooking",
            name="consent_version",
            field=models.CharField(
                default="privacy-2026-07-10",
                max_length=40,
                verbose_name="Phiên bản đồng ý",
            ),
        ),
    ]
