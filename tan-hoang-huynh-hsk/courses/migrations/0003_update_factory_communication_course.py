from django.db import migrations


def update_factory_communication_course(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Course.objects.filter(title="Tiếng Trung giao tiếp công việc").update(
        title="Tiếng Trung giao tiếp công xưởng",
        slug="tieng-trung-giao-tiep-cong-xuong",
        short_description="20 buổi giao tiếp tiếng Trung trong nhà máy và công việc hằng ngày.",
        description="Nội dung thiết kế sát nhu cầu người đi làm tại các khu công nghiệp Bắc Ninh: chào hỏi, nhận việc, báo cáo tiến độ, trao đổi lỗi sản phẩm, xin nghỉ, hỏi lịch làm và giao tiếp với quản lý.",
        duration="20 buổi",
        sessions=20,
        tuition=4200000,
        target_students="Nhân viên văn phòng, kỹ thuật, sản xuất và nhân sự đang làm việc với đồng nghiệp Trung Quốc.\nNgười chuẩn bị phỏng vấn vị trí yêu cầu tiếng Trung.",
        outcomes="Giao tiếp trong nhà máy bằng các mẫu câu thường dùng\nTrao đổi tiến độ, chất lượng và lịch làm việc\nViết tin nhắn công việc ngắn, đúng ngữ cảnh\nPhản xạ tốt trong 20 tình huống công xưởng",
        syllabus="Phát âm và mẫu câu giao tiếp ca kíp\nTừ vựng nhà máy, chất lượng và sản xuất\nBáo cáo lỗi, hỏi việc, xin nghỉ và nhắn tin\nMô phỏng tình huống công xưởng thực tế",
        is_active=True,
        order=10,
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_official_price_list_courses"),
    ]

    operations = [
        migrations.RunPython(update_factory_communication_course, noop_reverse),
    ]
