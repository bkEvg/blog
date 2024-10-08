# Generated by Django 3.1.4 on 2021-01-04 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210104_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='default_cover.jpeg', upload_to='blog_covers/%d.%m.%Y/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Готов')], default='draft', max_length=10),
        ),
    ]
