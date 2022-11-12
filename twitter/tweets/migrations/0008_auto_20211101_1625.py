# Generated by Django 3.1.7 on 2021-11-01 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profile_location'),
        ('tweets', '0007_auto_20211101_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile'),
        ),
    ]
