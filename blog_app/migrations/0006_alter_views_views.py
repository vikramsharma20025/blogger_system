# Generated by Django 4.1.6 on 2023-05-15 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_alter_post_blogbg_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='views',
            name='views',
            field=models.IntegerField(default=1),
        ),
    ]