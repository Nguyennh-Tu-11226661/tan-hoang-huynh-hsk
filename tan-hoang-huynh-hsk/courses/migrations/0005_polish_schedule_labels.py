from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0004_polish_course_copy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classschedule",
            name="format",
            field=models.CharField(
                choices=[
                    ("offline", "Học trực tiếp"),
                    ("online", "Học trực tuyến"),
                    ("hybrid", "Linh hoạt"),
                ],
                max_length=20,
                verbose_name="Hình thức",
            ),
        ),
    ]
