from django.db import migrations


def polish_blog_copy(apps, schema_editor):
    BlogPost = apps.get_model("content", "BlogPost")
    for post in BlogPost.objects.filter(content__contains="buổi test"):
        post.content = post.content.replace("buổi test", "buổi kiểm tra")
        post.save(update_fields=["content"])


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(polish_blog_copy, migrations.RunPython.noop),
    ]
