# Generated by Django 5.0.2 on 2024-02-28 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_followers_remove_profile_follows_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/avatar.jpg', upload_to='profile_pics'),
        ),
    ]
