# Generated by Django 4.2.7 on 2024-02-10 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kaczacze", "0009_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="profile_pics/default.jpg", upload_to="profile_pics"
            ),
        ),
    ]
