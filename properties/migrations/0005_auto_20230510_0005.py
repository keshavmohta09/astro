# Generated by Django 3.2.18 on 2023-05-09 18:35

import django.core.validators
from django.db import migrations, models
import helpers.files


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_alter_propertydocument_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertydocument',
            name='document',
            field=models.FileField(upload_to='', validators=[helpers.files.ValidateFileSize(max_file_size=5), django.core.validators.FileExtensionValidator(allowed_extensions=('pdf', 'jpeg', 'png', 'jpg'))]),
        ),
        migrations.AlterField(
            model_name='propertygallery',
            name='file',
            field=models.FileField(upload_to='', validators=[helpers.files.ValidateFileSize(max_file_size=5), django.core.validators.FileExtensionValidator(allowed_extensions=('jpeg', 'png', 'jpg'))]),
        ),
    ]
