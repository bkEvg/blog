# Generated by Django 3.1.4 on 2021-10-12 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default='None', max_length=250, verbose_name='Краткое описание поста для продвижения'),
            preserve_default=False,
        ),
    ]
