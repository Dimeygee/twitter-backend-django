# Generated by Django 3.1.7 on 2021-10-30 21:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweets',
            options={'ordering': ['-date_posted'], 'verbose_name': 'tweet'},
        ),
        migrations.AlterField(
            model_name='tweets',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]