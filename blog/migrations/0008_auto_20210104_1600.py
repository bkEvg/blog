# Generated by Django 3.1.4 on 2021-01-04 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210104_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover',
            field=models.ImageField(default='default.jpeg', upload_to='blog_covers/%s%d%Y/'),
        ),
        migrations.AlterField(
            model_name='author',
            name='profile_image',
            field=models.ImageField(default='default.jpeg', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='blog.author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Готов к публикации')], default='draft', max_length=10),
        ),
    ]
