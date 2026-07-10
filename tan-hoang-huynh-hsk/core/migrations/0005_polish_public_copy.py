from django.db import migrations


def polish_core_copy(apps, schema_editor):
    ContactInfo = apps.get_model("core", "ContactInfo")
    FAQ = apps.get_model("core", "FAQ")

    ContactInfo.objects.filter(
        center_name="Trung tâm Tiếng Trung Tân Hoàng Huynh HSK"
    ).update(center_name="Trung tâm tiếng Trung Tân Hoàng Huynh HSK")

    replacements = {
        "Học viên được trao đổi mục tiêu và làm bài test ngắn. Kết quả giúp trung tâm đề xuất cấp độ, lịch học và nhịp học phù hợp; không chỉ dựa trên khóa đã từng học.": "Học viên được trao đổi mục tiêu và làm bài kiểm tra ngắn. Kết quả giúp trung tâm đề xuất cấp độ, lịch học và nhịp học phù hợp; không chỉ dựa trên khóa đã từng học.",
        "Có. Trung tâm có lớp tối trong tuần, lớp cuối tuần và một số chương trình học linh hoạt online. Lịch cụ thể được cập nhật tại trang Lịch khai giảng.": "Có. Trung tâm có lớp tối trong tuần, lớp cuối tuần và một số chương trình học trực tuyến linh hoạt. Lịch cụ thể được cập nhật tại trang Lịch khai giảng.",
        "Có. Bạn có thể đăng ký một buổi học thử hoặc test đầu vào miễn phí. Trung tâm sẽ gọi lại xác nhận khung giờ phù hợp.": "Có. Bạn có thể đăng ký một buổi học thử hoặc kiểm tra đầu vào miễn phí. Trung tâm sẽ gọi lại xác nhận khung giờ phù hợp.",
    }
    for old_value, new_value in replacements.items():
        FAQ.objects.filter(answer=old_value).update(answer=new_value)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_contactinfo_secondary_hotline"),
    ]

    operations = [
        migrations.RunPython(polish_core_copy, migrations.RunPython.noop),
    ]
