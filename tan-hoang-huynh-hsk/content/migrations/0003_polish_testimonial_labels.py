from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0002_polish_blog_copy"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="testimonial",
            options={
                "ordering": ["order", "-id"],
                "verbose_name": "Cảm nhận học viên",
                "verbose_name_plural": "Cảm nhận học viên",
            },
        ),
        migrations.AlterField(
            model_name="testimonial",
            name="course_name",
            field=models.CharField("Khóa học / kết quả", max_length=180),
        ),
    ]
