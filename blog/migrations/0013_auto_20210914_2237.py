# Generated by Django 3.1.4 on 2021-09-14 15:37

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0012_auto_20210105_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='posts', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Тэги'),
        ),
    ]
