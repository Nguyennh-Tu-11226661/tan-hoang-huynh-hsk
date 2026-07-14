import os
from datetime import timedelta

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from content.models import BlogPost, GalleryImage, Testimonial
from core.models import Banner, ContactInfo, FAQ
from core.utils import vietnamese_slugify
from courses.models import ClassSchedule, Course


class Command(BaseCommand):
    help = "Tạo hoặc cập nhật dữ liệu mẫu cho website Tân Hoàng Huynh HSK."

    def attach_demo_image(
        self,
        instance,
        field_name,
        source_name,
        upload_name=None,
        source_dir="demo",
        force=False,
    ):
        image_field = getattr(instance, field_name)
        if not force and image_field and image_field.storage.exists(image_field.name):
            return

        source_path = settings.BASE_DIR / "static" / "img" / source_dir / source_name
        if not source_path.exists():
            self.stdout.write(self.style.WARNING(f"Không tìm thấy ảnh: {source_path}"))
            return

        if force and image_field:
            image_field.delete(save=False)

        with source_path.open("rb") as source:
            image_field.save(upload_name or source_name, File(source), save=True)

    def handle(self, *args, **options):
        allow_production_seed = os.getenv("ALLOW_PRODUCTION_SEED_DATA", "").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        if not settings.DEBUG and not allow_production_seed:
            raise CommandError(
                "Không chạy seed_data khi DEBUG=False. "
                "Nếu thật sự cần, đặt ALLOW_PRODUCTION_SEED_DATA=True."
            )

        today = timezone.localdate()

        ContactInfo.objects.update_or_create(
            center_name="Trung tâm tiếng Trung Tân Hoàng Huynh HSK",
            defaults={
                "address": os.getenv(
                    "CENTER_ADDRESS",
                    "198 Lý Anh Tông, phường Võ Cường, TP. Bắc Ninh",
                ),
                "hotline": os.getenv("CENTER_HOTLINE", "0829304304"),
                "secondary_hotline": os.getenv(
                    "CENTER_SECONDARY_HOTLINE", "0886056556"
                ),
                "email": os.getenv("CENTER_EMAIL", "tuvan@tanhoanghuynhhsk.com"),
                "zalo_url": os.getenv(
                    "CENTER_ZALO_URL", "https://zalo.me/0829304304"
                ),
                "facebook_url": os.getenv(
                    "CENTER_FACEBOOK_URL",
                    "https://www.facebook.com/profile.php?id=61578072303057",
                ),
                "messenger_url": os.getenv("CENTER_MESSENGER_URL", ""),
                "tiktok_url": os.getenv(
                    "CENTER_TIKTOK_URL",
                    "https://www.tiktok.com/@tanhoanghuynhhsk",
                ),
                "map_embed_url": os.getenv(
                    "CENTER_MAP_EMBED_URL",
                    "https://www.google.com/maps?q=198+Ly+Anh+Tong,+Vo+Cuong,+Bac+Ninh&output=embed",
                ),
                "working_hours": "Thứ 2–Chủ nhật: 08:00–21:00",
                "is_active": True,
            },
        )
        banner, _ = Banner.objects.update_or_create(
            title="Vững tiếng Trung, rộng đường tương lai",
            defaults={
                "subtitle": "Lộ trình HSK rõ ràng, lớp sĩ số nhỏ và giáo viên theo sát từng bước tiến của học viên Bắc Ninh.",
                "button_text": "Đăng ký học thử",
                "button_url": "/dat-lich-hoc-thu/",
                "order": 1,
                "is_active": True,
            },
        )
        self.attach_demo_image(
            banner,
            "image",
            "lop-hoc-that-01.jpg",
            "banner-lop-hoc-that-01.jpg",
            source_dir="center",
            force=True,
        )

        course_data = [
            {
                "title": "Tiếng Trung nhập môn cho người mới",
                "level": "Người mới",
                "short_description": "Giáo trình Tiếng Trung 123 Q1 cho người mới bắt đầu.",
                "description": "Lộ trình trình độ A theo giáo trình Tiếng Trung 123 Q1, tập trung giới thiệu bản thân, phân biệt bảng chữ cái, đếm số, mua sắm, hỏi đường, thời tiết, thuê nhà và giao tiếp khách sạn.",
                "duration": "40 buổi",
                "sessions": 40,
                "class_size": "8–12 học viên",
                "tuition": 4000000,
                "target_students": "Người chưa từng học tiếng Trung hoặc đã tự học nhưng mất gốc.\nHọc sinh, sinh viên và người đi làm cần nền tảng chắc trước khi học HSK.",
                "outcomes": "Đọc đúng pinyin và phân biệt bốn thanh điệu\nViết được các nét và bộ thủ cơ bản\nGiao tiếp giới thiệu, hỏi đường, mua sắm và lịch hẹn\nSẵn sàng bước vào lộ trình HSK 2",
                "syllabus": "Phát âm pinyin, khẩu hình và quy tắc biến điệu\n80 chữ Hán nền tảng và phương pháp ghi nhớ\nMẫu câu giao tiếp theo chủ đề đời sống\nÔn tập, hội thoại và kiểm tra cuối khóa",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Tiếng Trung YCT 1 cho trẻ em",
                "level": "YCT",
                "short_description": "Khóa YCT 1 gồm 40 buổi, xây nền tiếng Trung vui và dễ hiểu cho trẻ.",
                "description": "Chương trình dùng giáo trình YCT 1, giúp học viên nhỏ tuổi làm quen phát âm, từ vựng và mẫu câu cơ bản qua hoạt động tương tác.",
                "duration": "40 buổi",
                "sessions": 40,
                "class_size": "6–10 học viên",
                "tuition": 3200000,
                "target_students": "Học sinh nhỏ tuổi mới bắt đầu học tiếng Trung.\nPhụ huynh muốn con có lộ trình YCT rõ ràng.",
                "outcomes": "Nhận biết âm và từ vựng cơ bản\nNói các câu chào hỏi, giới thiệu đơn giản\nHình thành thói quen học tiếng Trung tích cực",
                "syllabus": "Làm quen phát âm và lớp học\nTừ vựng YCT 1 theo chủ đề gần gũi\nLuyện nghe nói qua trò chơi và hội thoại\nÔn tập cuối khóa",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "Tiếng Trung YCT 2 cho trẻ em",
                "level": "YCT",
                "short_description": "Khóa YCT 2 gồm 50 buổi, mở rộng vốn từ và phản xạ giao tiếp.",
                "description": "Chương trình dùng giáo trình YCT 2, nối tiếp nền YCT 1 và tăng dần khả năng nghe nói theo tình huống.",
                "duration": "50 buổi",
                "sessions": 50,
                "class_size": "6–10 học viên",
                "tuition": 4000000,
                "target_students": "Học sinh đã học YCT 1 hoặc có nền tiếng Trung sơ cấp.\nTrẻ cần học đều để chuẩn bị kiểm tra YCT.",
                "outcomes": "Mở rộng từ vựng theo chủ đề gia đình, trường học và sinh hoạt\nNghe hiểu câu ngắn quen thuộc\nTự tin trả lời các mẫu câu đơn giản",
                "syllabus": "Ôn nền YCT 1\nTừ vựng và mẫu câu YCT 2\nLuyện nghe nói theo cặp\nÔn tập và kiểm tra cuối khóa",
                "is_featured": False,
                "order": 3,
            },
            {
                "title": "Tiếng Trung YCT 3 cho trẻ em",
                "level": "YCT",
                "short_description": "Khóa YCT 3 gồm 60 buổi, củng cố đọc hiểu và giao tiếp theo chủ đề.",
                "description": "Chương trình dùng giáo trình YCT 3, giúp học viên nhỏ tuổi nâng độ dài câu, đọc hiểu đoạn ngắn và chuẩn bị tốt hơn cho lộ trình HSK sau này.",
                "duration": "60 buổi",
                "sessions": 60,
                "class_size": "6–10 học viên",
                "tuition": 4800000,
                "target_students": "Học sinh đã hoàn thành YCT 2 hoặc có trình độ tương đương.\nTrẻ cần lộ trình dài hơn để duy trì tiếng Trung đều đặn.",
                "outcomes": "Đọc hiểu đoạn ngắn phù hợp lứa tuổi\nNói được câu dài hơn theo chủ đề quen thuộc\nSẵn sàng chuyển tiếp sang YCT cao hơn hoặc HSK sơ cấp",
                "syllabus": "Ôn tập YCT 2\nTừ vựng và ngữ pháp YCT 3\nLuyện đọc hiểu và hội thoại\nThi thử, chữa lỗi và tổng kết",
                "is_featured": False,
                "order": 4,
            },
            {
                "title": "Tiếng Trung 123 - Trình độ B",
                "level": "Người mới",
                "short_description": "Giáo trình Tiếng Trung 123 Q2, học tiếp hội thoại và chủ đề đời sống.",
                "description": "Lộ trình trình độ B theo giáo trình Tiếng Trung 123 Q2, tập trung hội thoại về mua sắm, ẩm thực, giải trí, sức khỏe, học tập, nghề nghiệp, dịch vụ và an ninh trật tự.",
                "duration": "30 buổi",
                "sessions": 30,
                "class_size": "8–12 học viên",
                "tuition": 3000000,
                "target_students": "Học viên đã hoàn thành trình độ A hoặc nắm được phát âm và giao tiếp sơ cấp.\nNgười muốn tăng phản xạ hội thoại đời sống.",
                "outcomes": "Mở rộng vốn từ giao tiếp đời sống\nHỏi đáp tự tin hơn trong các tình huống quen thuộc\nCó nền để chuyển sang lộ trình HSK sơ cấp",
                "syllabus": "Ôn nhanh nền trình độ A\nChủ đề mua sắm, ăn uống và giải trí\nChủ đề sức khỏe, học tập, nghề nghiệp và dịch vụ\nLuyện hội thoại và kiểm tra cuối khóa",
                "is_featured": False,
                "order": 5,
            },
            {
                "title": "Luyện thi HSK 1",
                "level": "HSK 1",
                "short_description": "HSK Standard Course 1 gồm 24 buổi cho nền sơ cấp.",
                "description": "Khóa HSK 1 bám giáo trình HSK Standard Course 1, giúp học viên hệ thống từ vựng, cấu trúc câu và kỹ năng nghe đọc nền tảng.",
                "duration": "24 buổi",
                "sessions": 24,
                "class_size": "8–12 học viên",
                "tuition": 4800000,
                "target_students": "Người mới đã có nền phát âm cơ bản.\nHọc viên muốn bắt đầu lộ trình thi HSK chính quy.",
                "outcomes": "Nắm chắc từ vựng và mẫu câu HSK 1\nNghe hiểu hội thoại rất ngắn\nĐọc hiểu câu đơn và làm quen định dạng đề",
                "syllabus": "Từ vựng HSK 1\nMẫu câu và ngữ pháp nền\nLuyện nghe đọc theo bài\nÔn tập và thi thử",
                "is_featured": False,
                "order": 6,
            },
            {
                "title": "Luyện thi HSK 2 nền tảng",
                "level": "HSK 2",
                "short_description": "HSK Standard Course 2 gồm 30 buổi, luyện nghe đọc sơ cấp.",
                "description": "Khóa học bám giáo trình HSK Standard Course 2, dành cho học viên đã có nền HSK 1 hoặc tương đương và muốn tăng tốc lên HSK 2.",
                "duration": "30 buổi",
                "sessions": 30,
                "class_size": "8–12 học viên",
                "tuition": 6000000,
                "target_students": "Học viên đã hoàn thành nhập môn hoặc có vốn từ cơ bản.\nNgười cần chứng chỉ HSK 2 để hoàn thiện hồ sơ học tập.",
                "outcomes": "Nắm chắc khoảng 500 từ theo khung HSK mới\nNghe hiểu hội thoại ngắn với tốc độ vừa\nĐọc hiểu thông báo và đoạn văn cơ bản\nLàm quen cấu trúc đề thi HSK",
                "syllabus": "Ôn phát âm và kiểm tra vốn từ đầu vào\nTừ vựng, ngữ pháp và nghe theo chủ đề\nĐọc hiểu, sắp xếp câu và phản xạ hội thoại\nLuyện đề tổng hợp và chữa lỗi cá nhân",
                "is_featured": True,
                "order": 7,
            },
            {
                "title": "Chinh phục HSK 3",
                "level": "HSK 3",
                "short_description": "HSK Standard Course 3 gồm 36 buổi, tăng tốc nghe đọc.",
                "description": "Lộ trình HSK 3 theo HSK Standard Course 3, cân bằng giữa ngôn ngữ ứng dụng và kỹ năng làm bài thi.",
                "duration": "36 buổi",
                "sessions": 36,
                "class_size": "8–12 học viên",
                "tuition": 7200000,
                "target_students": "Học viên đã hoàn thành HSK 2 hoặc đạt bài kiểm tra đầu vào tương đương.\nNgười cần HSK 3 cho học tập, việc làm hoặc chuẩn bị du học.",
                "outcomes": "Sử dụng khoảng 1.000 từ trong chủ đề quen thuộc\nNghe bắt ý chính và thông tin chi tiết\nĐọc hiểu đoạn văn có liên kết\nHoàn thành đề HSK 3 đúng thời gian",
                "syllabus": "Hệ thống lại nền HSK 2 và lấp lỗ hổng\nPhát triển từ vựng, ngữ pháp theo 12 chủ đề\nLuyện nghe đọc theo dạng câu hỏi\nBa vòng luyện đề và thi thử cuối khóa",
                "is_featured": True,
                "order": 8,
            },
            {
                "title": "Luyện thi HSK 4 tăng tốc",
                "level": "HSK 4",
                "short_description": "HSK Standard Course 4 trọn quyển thượng và hạ.",
                "description": "Khóa HSK 4 gồm quyển thượng 22 buổi và quyển hạ 22 buổi. Nội dung tập trung vốn từ trung cấp, đọc hiểu tốc độ cao, viết câu chính xác và luyện đề có phân tích lỗi.",
                "duration": "44 buổi",
                "sessions": 44,
                "class_size": "6–10 học viên",
                "tuition": 8800000,
                "target_students": "Người đã đạt HSK 3 hoặc tương đương.\nHọc viên cần HSK 4 để xét tốt nghiệp, xin học bổng hoặc ứng tuyển doanh nghiệp Trung Quốc.",
                "outcomes": "Hệ thống hóa khoảng 2.000 từ vựng theo lộ trình HSK Standard Course 4, đối chiếu mục tiêu thi HSK cấp 4 dạng 6 cấp hiện hành\nNắm chiến thuật nghe và đọc giới hạn thời gian\nViết câu đúng trật tự và ngữ pháp\nĐạt mục tiêu 220+ qua các lần thi thử",
                "syllabus": "Quyển thượng: 22 buổi - 4.400.000đ\nQuyển hạ: 22 buổi - 4.400.000đ\nLuyện từng dạng nghe, đọc và viết\nThi thử, thống kê lỗi và tăng tốc",
                "is_featured": True,
                "order": 9,
            },
            {
                "title": "Tiếng Trung giao tiếp công xưởng",
                "level": "Giao tiếp",
                "short_description": "Khóa giao tiếp độc lập 20 buổi cho môi trường nhà máy, văn phòng và phỏng vấn.",
                "description": "Đây là khóa giao tiếp độc lập, không yêu cầu đi theo lộ trình HSK trước đó. Nội dung thiết kế sát nhu cầu người đi làm tại các khu công nghiệp Bắc Ninh: chào hỏi, nhận việc, báo cáo tiến độ, trao đổi lỗi sản phẩm, xin nghỉ, hỏi lịch làm, nhắn tin công việc và giao tiếp với quản lý.",
                "duration": "20 buổi",
                "sessions": 20,
                "class_size": "8–10 học viên",
                "tuition": 4200000,
                "target_students": "Nhân viên văn phòng, kỹ thuật, sản xuất và nhân sự đang làm việc với đồng nghiệp Trung Quốc.\nNgười chuẩn bị phỏng vấn vị trí yêu cầu tiếng Trung.",
                "outcomes": "Giao tiếp trong nhà máy và văn phòng bằng các mẫu câu thường dùng\nTrao đổi tiến độ, chất lượng và lịch làm việc\nViết tin nhắn công việc ngắn, đúng ngữ cảnh\nPhản xạ tốt trong 20 tình huống công xưởng và phỏng vấn",
                "syllabus": "Phát âm và mẫu câu giao tiếp ca kíp\nTừ vựng nhà máy, chất lượng, văn phòng và sản xuất\nBáo cáo lỗi, hỏi việc, xin nghỉ và nhắn tin\nMô phỏng tình huống công xưởng, văn phòng và phỏng vấn",
                "is_featured": True,
                "order": 10,
            },
            {
                "title": "Ôn thi HSK 5 chuyên sâu",
                "level": "HSK 5",
                "short_description": "HSK Standard Course 5 trọn quyển thượng và hạ.",
                "description": "Chương trình HSK 5 gồm quyển thượng 30 buổi và quyển hạ 30 buổi, dành cho học viên cần điểm HSK 5 phục vụ du học, học bổng hoặc công việc chuyên môn.",
                "duration": "60 buổi",
                "sessions": 60,
                "class_size": "6–8 học viên",
                "tuition": 18000000,
                "target_students": "Học viên có nền HSK 4 vững và sẵn sàng dành tối thiểu 8 giờ tự học mỗi tuần.",
                "outcomes": "Mở rộng vốn từ trung cao cấp theo chủ đề\nĐọc nhanh bài dài và xác định lập luận\nViết đoạn văn mạch lạc từ tranh và từ khóa\nKiểm soát thời gian ở đề thi HSK 5",
                "syllabus": "Quyển thượng: 30 buổi - 9.000.000đ\nQuyển hạ: 30 buổi - 9.000.000đ\nĐọc dài, nghe nhanh và kỹ thuật ghi chú\nLuyện viết, thi thử và chiến lược phòng thi",
                "is_featured": False,
                "order": 11,
            },
            {
                "title": "Luyện thi HSK 6 chuyên sâu",
                "level": "HSK 6",
                "short_description": "HSK Standard Course 6 gồm 4 giai đoạn chuyên sâu.",
                "description": "Lộ trình HSK 6 chia thành bốn giai đoạn: đọc hiểu học thuật, nghe nâng cao, viết học thuật, luyện đề và đánh giá toàn diện.",
                "duration": "70 buổi",
                "sessions": 70,
                "class_size": "6–8 học viên",
                "tuition": 21000000,
                "target_students": "Học viên đã hoàn thành HSK 5 hoặc có nền trung cao cấp vững.\nNgười cần HSK 6 cho học thuật, công việc hoặc hồ sơ du học.",
                "outcomes": "Đọc hiểu văn bản học thuật dài\nNghe bắt ý và ghi chú ở tốc độ cao\nViết bài có cấu trúc và lập luận rõ\nLàm đề HSK 6 theo chiến thuật cá nhân",
                "syllabus": "Giai đoạn 1: đọc hiểu học thuật - 20 buổi - 6.000.000đ\nGiai đoạn 2: nghe nâng cao - 15 buổi - 4.500.000đ\nGiai đoạn 3: viết học thuật - 15 buổi - 4.500.000đ\nGiai đoạn 4: luyện đề và đánh giá toàn diện - 20 buổi - 6.000.000đ",
                "is_featured": False,
                "order": 12,
            },
        ]
        courses = {}
        course_images = [
            "lop-hoc-that-01.jpg",
            "hoc-vien-nhi-giang-sinh.jpg",
            "lop-hoc-man-hinh-thong-minh.jpg",
            "lop-giao-tiep-thuc-te.jpg",
            "mat-tien-trung-tam.jpg",
        ]
        for index, data in enumerate(course_data):
            slug = vietnamese_slugify(data["title"])
            course, _ = Course.objects.update_or_create(
                title=data["title"], defaults={**data, "slug": slug, "is_active": True}
            )
            self.attach_demo_image(
                course,
                "image",
                course_images[index % len(course_images)],
                f"{slug}.jpg",
                source_dir="center",
                force=True,
            )
            courses.setdefault(course.level, course)

        schedules = [
            ("NMB-T07-01", "Người mới", 7, "Thứ 2-4-6 · 19:00–20:30", "offline", "Cô Nguyễn Hoàng Anh", 7),
            ("HSK2-T07-02", "HSK 2", 12, "Thứ 3-5 · 19:00–21:00", "offline", "Thầy Trần Minh Quân", 5),
            ("HSK3-T07-03", "HSK 3", 18, "Thứ 2-4-6 · 19:30–21:00", "hybrid", "Cô Đỗ Phương Linh", 4),
            ("GT-T08-01", "Giao tiếp", 25, "Thứ 7-CN · 09:00–11:00", "offline", "Cô Nguyễn Hoàng Anh", 8),
            ("HSK4-T08-02", "HSK 4", 32, "Thứ 3-5-7 · 19:00–20:30", "hybrid", "Thầy Trần Minh Quân", 3),
            ("HSK5-T09-01", "HSK 5", 48, "Thứ 7-CN · 14:00–17:00", "online", "Cô Đỗ Phương Linh", 6),
        ]
        for code, level, days, schedule_text, format_value, teacher, seats in schedules:
            ClassSchedule.objects.update_or_create(
                class_code=code,
                defaults={
                    "course": courses[level],
                    "start_date": today + timedelta(days=days),
                    "schedule_text": schedule_text,
                    "format": format_value,
                    "teacher": teacher,
                    "seats_left": seats,
                    "is_active": True,
                },
            )

        testimonial_data = [
            ("Nguyễn Thu Trang", "Chinh phục HSK 3", "HSK 3 · 278/300", "Trước đây mình nghe được vài từ nhưng không ghép nổi ý. Sau bốn tháng, mình biết cách bắt từ khóa và lần đầu làm đề đủ thời gian. Giáo viên chữa rất kỹ từng lỗi nhỏ."),
            ("Trần Đức Anh", "Tiếng Trung giao tiếp công xưởng", "", "Mình làm tại KCN Quế Võ và cần trao đổi với kỹ sư Trung Quốc. Các tình huống trên lớp rất sát công việc nên sau hai tháng mình đã tự tin báo cáo tiến độ."),
            ("Lê Phương Thảo", "Luyện thi HSK 4 tăng tốc", "HSK 4 · 252/300", "Điểm mình tăng rõ nhất ở phần đọc. Trung tâm cho thống kê lỗi sau mỗi đề nên mình biết chính xác dạng nào cần luyện thay vì làm đề thật nhiều mà không tiến bộ."),
            ("Ngô Minh Hải", "Tiếng Trung nhập môn", "", "Từng bỏ cuộc hai lần vì phát âm khó, nhưng ở đây cô sửa từng khẩu hình. Sau khóa nhập môn mình đã có thể tự giới thiệu và trò chuyện các chủ đề đơn giản."),
            ("Phạm Khánh Linh", "Ôn thi HSK 5 chuyên sâu", "HSK 5 · 241/300", "Lộ trình khá nặng nhưng rất rõ. Mình đặc biệt thích các buổi chữa viết vì nhận được góp ý cụ thể về từ nối, cách triển khai và lỗi dùng từ."),
            ("Đặng Mai Hương", "Luyện thi HSK 2 nền tảng", "HSK 2 · 286/300", "Lớp ít người nên ai cũng được gọi nói. Mỗi tuần cô gửi báo cáo nhỏ về từ vựng và bài tập, nhờ vậy mình duy trì được thói quen học đều."),
        ]
        for order, (name, course_name, score, text) in enumerate(testimonial_data, 1):
            Testimonial.objects.update_or_create(
                student_name=name,
                defaults={
                    "course_name": course_name,
                    "score": score,
                    "content": text,
                    "rating": 5,
                    "is_featured": order <= 3,
                    "is_active": True,
                    "order": order,
                },
            )

        gallery_data = [
            (
                "Lớp học tại trung tâm",
                "Không gian học thật với sĩ số nhỏ và giáo viên theo sát",
                "lop-hoc-that-01.jpg",
            ),
            (
                "Mặt tiền trung tâm",
                "Địa điểm học trực tiếp tại Bắc Ninh",
                "mat-tien-trung-tam.jpg",
            ),
            (
                "Lớp học với màn hình thông minh",
                "Bài giảng trực quan, luyện nghe nói ngay tại lớp",
                "lop-hoc-man-hinh-thong-minh.jpg",
            ),
            (
                "Luyện giao tiếp thực tế",
                "Học viên thực hành theo chủ đề đời sống và công việc",
                "lop-giao-tiep-thuc-te.jpg",
            ),
            (
                "Hoạt động học viên nhí",
                "Khoảnh khắc học tập và sinh hoạt tại trung tâm",
                "hoc-vien-nhi-giang-sinh.jpg",
            ),
        ]
        old_demo_gallery_titles = [
            "Lớp giao tiếp HSK",
            "Thi thử HSK định kỳ",
            "Workshop viết chữ Hán",
            "Luyện nói theo cặp",
            "Vinh danh học viên",
        ]
        GalleryImage.objects.filter(title__in=old_demo_gallery_titles).update(
            is_active=False
        )
        for order, (title, caption, source_name) in enumerate(gallery_data, 1):
            gallery_item, _ = GalleryImage.objects.update_or_create(
                title=title,
                defaults={
                    "caption": caption,
                    "media_type": GalleryImage.MediaType.IMAGE,
                    "video_url": "",
                    "event_date": today - timedelta(days=order * 9),
                    "is_active": True,
                    "order": order,
                },
            )
            self.attach_demo_image(
                gallery_item,
                "image",
                source_name,
                f"{vietnamese_slugify(title)}.jpg",
                source_dir="center",
                force=True,
            )

        faq_data = [
            ("Người chưa biết gì có thể học được không?", "Có. Khóa nhập môn bắt đầu từ pinyin, khẩu hình và bốn thanh điệu. Bạn sẽ được sửa phát âm trực tiếp trước khi chuyển sang từ vựng và chữ Hán."),
            ("Trung tâm xếp lớp như thế nào?", "Học viên được trao đổi mục tiêu và làm bài kiểm tra ngắn. Kết quả giúp trung tâm đề xuất cấp độ, lịch học và nhịp học phù hợp; không chỉ dựa trên khóa đã từng học."),
            ("Một lớp có bao nhiêu học viên?", "Phần lớn lớp có 8–12 học viên; lớp HSK 4–5 chuyên sâu có 6–10 học viên. Sĩ số nhỏ giúp giáo viên theo dõi phát âm và bài tập của từng người."),
            ("Có lớp dành cho người đi làm không?", "Có. Trung tâm có lớp tối trong tuần, lớp cuối tuần và một số chương trình học trực tuyến linh hoạt. Lịch cụ thể được cập nhật tại trang Lịch khai giảng."),
            ("Có được học thử trước khi đăng ký không?", "Có. Bạn có thể đăng ký một buổi học thử hoặc kiểm tra đầu vào miễn phí. Trung tâm sẽ gọi lại xác nhận khung giờ phù hợp."),
            ("Học phí đã bao gồm tài liệu chưa?", "Học phí công bố là học phí trọn khóa. Tư vấn viên sẽ nói rõ tài liệu, chính sách bảo lưu và ưu đãi đang áp dụng trước khi bạn đăng ký."),
            ("Trung tâm có cam kết đầu ra HSK không?", "Mỗi khóa có chuẩn đầu ra và mốc thi thử rõ ràng. Kết quả phụ thuộc cả thời lượng học và mức độ hoàn thành bài tập; trung tâm cam kết theo sát, đánh giá minh bạch và hỗ trợ bù kiến thức."),
        ]
        for order, (question, answer) in enumerate(faq_data, 1):
            FAQ.objects.update_or_create(
                question=question,
                defaults={"answer": answer, "order": order, "is_active": True},
            )

        posts = [
            (
                "Học tiếng Trung cho người mới: 30 ngày đầu nên làm gì?",
                "Một kế hoạch thực tế để xây nền phát âm, từ vựng và thói quen học tiếng Trung mà không bị quá tải.",
                "Ba mươi ngày đầu không phải lúc để cố nhớ thật nhiều chữ Hán. Đây là giai đoạn tạo nền phát âm và nhịp học ổn định.\nTuần đầu tiên, hãy dành phần lớn thời gian cho thanh mẫu, vận mẫu và bốn thanh điệu. Tự ghi âm câu ngắn rồi nghe lại. Một lỗi phát âm được sửa sớm sẽ tiết kiệm rất nhiều thời gian về sau.\nTừ tuần thứ hai, bạn có thể học từ theo cụm và đặt vào câu. Thay vì chỉ nhớ 认识 là “quen biết”, hãy tập cả câu 很高兴认识你. Não sẽ ghi nhớ tốt hơn khi từ có ngữ cảnh.\nTrong hai tuần cuối, duy trì mỗi ngày 20 phút nghe, 15 phút ôn từ và 10 phút đọc thành tiếng. Đừng tăng thời lượng quá nhanh. Một lịch ngắn nhưng đều luôn tốt hơn ba giờ học dồn vào cuối tuần.\nNếu không chắc phát âm của mình đúng hay chưa, một buổi kiểm tra với giáo viên sẽ giúp bạn nhận ra điểm cần sửa trước khi đi xa hơn.",
                "Lộ trình học tiếng Trung 30 ngày đầu cho người mới: phát âm, từ vựng theo cụm và cách duy trì thói quen hiệu quả.",
            ),
            (
                "5 lỗi khiến bạn nghe tiếng Trung mãi không tiến bộ",
                "Bạn nghe nhiều nhưng vẫn không bắt được ý? Có thể vấn đề nằm ở cách nghe, không phải số giờ.",
                "Nghe tiếng Trung không tiến bộ thường không phải vì bạn thiếu năng khiếu. Phần lớn người học đang lặp lại một trong năm lỗi quen thuộc.\nLỗi đầu tiên là chọn tài liệu khó hơn trình độ quá nhiều. Khi một đoạn có hơn 20% từ mới, não chỉ nghe thấy chuỗi âm thanh. Hãy chọn bài bạn đã hiểu phần lớn nội dung.\nLỗi thứ hai là bật phụ đề tiếng Việt ngay từ đầu. Mắt sẽ đọc nhanh hơn tai xử lý và bạn tưởng mình đã nghe hiểu. Hãy nghe một lượt không phụ đề, ghi lại từ khóa, rồi mới kiểm tra bằng transcript tiếng Trung.\nLỗi thứ ba là không học âm nối và biến điệu. Tiếng Trung trong hội thoại không tách rõ như từng từ trong sách. Đọc thành tiếng và bắt chước từng câu giúp tai quen với nhịp thật.\nHai lỗi còn lại là nghe thụ động quá lâu và không nghe lại cùng một bài. Một đoạn ngắn được xử lý sâu ba lần có giá trị hơn danh sách mười video bạn chỉ mở làm âm nền.",
                "Năm lỗi phổ biến khi luyện nghe tiếng Trung và cách chọn tài liệu, dùng phụ đề, shadowing đúng trình độ.",
            ),
            (
                "Cách nhớ chữ Hán bằng bộ thủ thay vì học thuộc nét",
                "Hiểu cấu tạo chữ giúp bạn nhớ lâu, đoán nghĩa và viết chính xác hơn.",
                "Chữ Hán trở nên đáng sợ khi người học nhìn mỗi chữ như một bức tranh hoàn toàn mới. Bộ thủ giúp biến bức tranh đó thành các mảnh có quy luật.\nVí dụ, những chữ có bộ 氵 thường liên quan đến nước hoặc chất lỏng như 河, 海, 洗. Khi gặp chữ mới, việc nhận ra bộ nghĩa tạo một chiếc móc để trí nhớ bám vào.\nTuy nhiên, không nên học một danh sách 214 bộ thủ trước rồi mới học chữ. Cách hiệu quả hơn là gặp chữ nào, phân tích bộ của chữ đó và đặt nó vào một từ hoặc câu quen thuộc.\nMỗi ngày bạn có thể chọn năm chữ, viết ba lần theo đúng thứ tự nét, nói to âm đọc và tự tạo một liên tưởng ngắn. Cuối tuần, hãy ôn bằng cách nhìn nghĩa viết chữ thay vì chỉ nhìn chữ đọc nghĩa.\nKhi vốn chữ tăng, bạn sẽ dần đoán được trường nghĩa và âm đọc của nhiều chữ mới. Đó là lúc chữ Hán chuyển từ bài học thuộc thành một hệ thống có logic.",
                "Phương pháp nhớ chữ Hán qua bộ thủ, cấu tạo chữ và ngữ cảnh dành cho người mới học tiếng Trung.",
            ),
            (
                "Kinh nghiệm luyện đề HSK 4 để không thiếu thời gian",
                "Ba bước phân bổ thời gian, đánh dấu câu khó và phân tích lỗi sau mỗi đề HSK 4.",
                "Thiếu thời gian ở HSK 4 thường xuất phát từ việc phân bổ sai, đặc biệt là dành quá lâu cho một câu đọc hiểu khó.\nTrước khi luyện đề trọn vẹn, hãy đo thời gian từng phần. Bạn cần biết mình chậm ở sắp xếp câu, đọc đoạn hay phần viết. Dữ liệu này quan trọng hơn cảm giác “mình đọc hơi chậm”.\nTrong phòng thi, đặt giới hạn cho mỗi câu. Nếu đã đọc hai lượt mà chưa xác định được đáp án, hãy đánh dấu và chuyển tiếp. Một câu khó không được phép lấy thời gian của ba câu dễ phía sau.\nSau mỗi đề, chia lỗi thành ba nhóm: không biết từ, hiểu sai cấu trúc và sai vì vội. Mỗi nhóm cần cách sửa khác nhau. Chép thêm từ sẽ không giải quyết được lỗi đọc nhầm yêu cầu.\nCuối cùng, hãy dành ba đến bốn đề cuối để mô phỏng đúng giờ và không dừng giữa chừng. Sự quen thuộc với áp lực thời gian là một phần của kỹ năng thi.",
                "Cách luyện đề HSK 4 đúng thời gian, phân loại lỗi và xây chiến thuật làm bài hiệu quả.",
            ),
        ]
        now = timezone.now()
        blog_images = [
            "lop-hoc-that-01.jpg",
            "lop-giao-tiep-thuc-te.jpg",
            "lop-hoc-man-hinh-thong-minh.jpg",
            "mat-tien-trung-tam.jpg",
        ]
        for index, (title, excerpt, body, meta) in enumerate(posts):
            post, _ = BlogPost.objects.update_or_create(
                title=title,
                defaults={
                    "slug": vietnamese_slugify(title),
                    "excerpt": excerpt,
                    "content": body,
                    "author_name": "Ban học thuật Tân Hoàng Huynh",
                    "status": BlogPost.Status.PUBLISHED,
                    "published_at": now - timedelta(days=index * 8),
                    "meta_description": meta[:160],
                },
            )
            self.attach_demo_image(
                post,
                "featured_image",
                blog_images[index % len(blog_images)],
                f"{post.slug}.jpg",
                source_dir="center",
                force=True,
            )

        self.stdout.write(self.style.SUCCESS("Đã tạo/cập nhật dữ liệu mẫu thành công."))
