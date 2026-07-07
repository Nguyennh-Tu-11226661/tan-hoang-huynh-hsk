from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactinfo",
            name="facebook_url",
            field=models.URLField(blank=True, verbose_name="Facebook"),
        ),
        migrations.AlterField(
            model_name="contactinfo",
            name="map_embed_url",
            field=models.URLField(
                blank=True, max_length=1000, verbose_name="Link nhúng Google Maps"
            ),
        ),
        migrations.AlterField(
            model_name="contactinfo",
            name="messenger_url",
            field=models.URLField(blank=True, verbose_name="Messenger"),
        ),
        migrations.AlterField(
            model_name="contactinfo",
            name="zalo_url",
            field=models.URLField(blank=True, verbose_name="Zalo"),
        ),
    ]
