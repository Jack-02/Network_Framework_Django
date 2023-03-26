# Generated by Django 3.2.7 on 2023-03-01 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='esg_reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('edittime', models.DateTimeField(verbose_name='上传时间')),
                ('pdf_url', models.URLField(verbose_name='报告URL')),
                ('md5', models.CharField(max_length=500, verbose_name='md5码')),
                ('abstract', models.TextField(verbose_name='摘要')),
                ('key_words', models.TextField(verbose_name='关键词')),
                ('key_phrases', models.TextField(verbose_name='关键短语')),
            ],
        ),
    ]