# Generated by Django 4.1.5 on 2023-01-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hastags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
