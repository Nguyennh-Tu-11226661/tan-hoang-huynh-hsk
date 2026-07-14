from django.db import migrations


def clarify_hsk4_outcome(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    old_value = (
        "Làm chủ khoảng 2.000 từ vựng theo khung mới\n"
        "Nắm chiến thuật nghe và đọc giới hạn thời gian\n"
        "Viết câu đúng trật tự và ngữ pháp\n"
        "Đạt mục tiêu 220+ qua các lần thi thử"
    )
    new_value = (
        "Hệ thống hóa khoảng 2.000 từ vựng theo lộ trình HSK Standard Course 4, "
        "đối chiếu mục tiêu thi HSK cấp 4 dạng 6 cấp hiện hành\n"
        "Nắm chiến thuật nghe và đọc giới hạn thời gian\n"
        "Viết câu đúng trật tự và ngữ pháp\n"
        "Đạt mục tiêu 220+ qua các lần thi thử"
    )
    Course.objects.filter(title="Luyện thi HSK 4 tăng tốc", outcomes=old_value).update(
        outcomes=new_value
    )


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0005_polish_schedule_labels"),
    ]

    operations = [
        migrations.RunPython(clarify_hsk4_outcome, migrations.RunPython.noop),
    ]
