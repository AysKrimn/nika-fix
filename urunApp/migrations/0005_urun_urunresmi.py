# Generated by Django 4.1.7 on 2023-04-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunApp', '0004_alter_urun_serino'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='urunResmi',
            field=models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Urunun Resmi'),
        ),
    ]
