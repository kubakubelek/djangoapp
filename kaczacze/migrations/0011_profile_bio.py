# Generated by Django 4.2.7 on 2024-02-12 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kaczacze", "0010_alter_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(default=""),
        ),
    ]
