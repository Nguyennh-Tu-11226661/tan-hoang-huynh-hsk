from django.db import migrations


BLOG_IMAGE_PATHS = {
    "HỌC TIẾNG TRUNG – MỞ RỘNG TƯƠNG LAI CÙNG TRUNG TÂM TIẾNG TRUNG TÂN HOÀNG HUYNH": "blog/hoc-tieng-trung-mo-rong-tuong-lai.jpg",
    "KHAI GIẢNG LỚP TIẾNG TRUNG GIAO TIẾP": "blog/khai-giang-lop-tieng-trung-giao-tiep.jpg",
    "HSK mở lối tương lai: Lợi ích cho học sinh, người đi làm và người muốn du học": "blog/hsk-loi-ich.png",
    "Không khí học tập thực tế tại Trung tâm tiếng Trung Tân Hoàng Huỳnh HSK": "blog/khong-khi-hoc-tap-thuc-te.jpg",
    "Niềm vui học tiếng Trung của các học viên nhí tại Tân Hoàng Huỳnh HSK": "blog/hoc-vien-nhi.jpg",
}


PREVIOUS_BLOG_IMAGE_PATHS = {
    "HỌC TIẾNG TRUNG – MỞ RỘNG TƯƠNG LAI CÙNG TRUNG TÂM TIẾNG TRUNG TÂN HOÀNG HUYNH": "",
    "KHAI GIẢNG LỚP TIẾNG TRUNG GIAO TIẾP": "",
    "HSK mở lối tương lai: Lợi ích cho học sinh, người đi làm và người muốn du học": "blog/HSK.png",
    "Không khí học tập thực tế tại Trung tâm tiếng Trung Tân Hoàng Huỳnh HSK": "blog/4.jpg",
    "Niềm vui học tiếng Trung của các học viên nhí tại Tân Hoàng Huỳnh HSK": "blog/2.jpg",
}


def set_media_paths(apps, schema_editor, *, blog_paths, gallery_path):
    BlogPost = apps.get_model("content", "BlogPost")
    GalleryImage = apps.get_model("content", "GalleryImage")

    for title, image_path in blog_paths.items():
        BlogPost.objects.filter(title=title).update(featured_image=image_path)

    GalleryImage.objects.filter(
        title="Lợi ích HSK – Nền tảng vững chắc mở ra tương lai rộng mở"
    ).update(image=gallery_path)


def restore_media_paths(apps, schema_editor):
    set_media_paths(
        apps,
        schema_editor,
        blog_paths=BLOG_IMAGE_PATHS,
        gallery_path="gallery/hsk-loi-ich.png",
    )


def reverse_media_paths(apps, schema_editor):
    set_media_paths(
        apps,
        schema_editor,
        blog_paths=PREVIOUS_BLOG_IMAGE_PATHS,
        gallery_path="gallery/HSK.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0003_polish_testimonial_labels"),
    ]

    operations = [
        migrations.RunPython(restore_media_paths, reverse_media_paths),
    ]
