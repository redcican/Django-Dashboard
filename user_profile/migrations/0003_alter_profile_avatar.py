# Generated by Django 3.2.5 on 2021-07-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default-avatar.png', upload_to='avatars'),
        ),
    ]
