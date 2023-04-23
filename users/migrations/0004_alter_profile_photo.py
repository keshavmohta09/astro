# Generated by Django 4.1.7 on 2023-04-06 10:22

from django.db import migrations, models
import helpers.files


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=helpers.files.RenameFile(
                    "users/profile_pics/{instance.user.email}.{extension}"
                ),
            ),
        ),
    ]
