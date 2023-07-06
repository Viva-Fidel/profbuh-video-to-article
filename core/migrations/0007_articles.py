# Generated by Django 4.2.2 on 2023-07-06 07:09

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_paragraphs_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.CharField(editable=False, max_length=36)),
                ('article_file', models.FileField(upload_to=core.models.article_upload_to)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.videos')),
            ],
        ),
    ]