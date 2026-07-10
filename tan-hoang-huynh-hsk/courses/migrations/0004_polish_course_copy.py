from django.db import migrations


def polish_course_copy(apps, schema_editor):
    Course = apps.get_model("courses", "Course")

    replacements = {
        "Giáo trình Tiếng Việt 123 Q1 cho người mới bắt đầu.": "Giáo trình Tiếng Trung 123 Q1 cho người mới bắt đầu.",
        "Lộ trình trình độ A theo giáo trình Tiếng Việt 123 Q1, tập trung giới thiệu bản thân, phân biệt bảng chữ cái, đếm số, mua sắm, hỏi đường, thời tiết, thuê nhà và giao tiếp khách sạn.": "Lộ trình trình độ A theo giáo trình Tiếng Trung 123 Q1, tập trung giới thiệu bản thân, phân biệt bảng chữ cái, đếm số, mua sắm, hỏi đường, thời tiết, thuê nhà và giao tiếp khách sạn.",
        "Giáo trình Tiếng Việt 123 Q2, học tiếp hội thoại và chủ đề đời sống.": "Giáo trình Tiếng Trung 123 Q2, học tiếp hội thoại và chủ đề đời sống.",
        "Lộ trình trình độ B theo giáo trình Tiếng Việt 123 Q2, tập trung hội thoại về mua sắm, ẩm thực, giải trí, sức khỏe, học tập, nghề nghiệp, dịch vụ và an ninh trật tự.": "Lộ trình trình độ B theo giáo trình Tiếng Trung 123 Q2, tập trung hội thoại về mua sắm, ẩm thực, giải trí, sức khỏe, học tập, nghề nghiệp, dịch vụ và an ninh trật tự.",
    }

    for old_value, new_value in replacements.items():
        Course.objects.filter(short_description=old_value).update(short_description=new_value)
        Course.objects.filter(description=old_value).update(description=new_value)

    for course in Course.objects.filter(target_students__contains="bài test đầu vào"):
        course.target_students = course.target_students.replace(
            "bài test đầu vào", "bài kiểm tra đầu vào"
        )
        course.save(update_fields=["target_students"])


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_update_factory_communication_course"),
    ]

    operations = [
        migrations.RunPython(polish_course_copy, migrations.RunPython.noop),
    ]
