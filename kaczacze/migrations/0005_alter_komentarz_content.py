# Generated by Django 4.2.7 on 2024-02-08 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kaczacze", "0004_komentarz_date_komentarz_time_komentarz_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="komentarz",
            name="content",
            field=models.CharField(max_length=100),
        ),
    ]
