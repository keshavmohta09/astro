# Generated by Django 3.2.18 on 2023-05-12 21:13

import django.core.validators
from django.db import migrations, models
import helpers.files


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_alter_property_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydocument',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertydocument',
            name='document',
            field=models.FileField(upload_to='', validators=[helpers.files.ValidateFileSize(max_file_size=5), django.core.validators.FileExtensionValidator(allowed_extensions=('pdf', 'docx', 'doc'))]),
        ),
    ]
