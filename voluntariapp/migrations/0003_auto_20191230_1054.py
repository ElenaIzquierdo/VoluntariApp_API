# Generated by Django 3.0 on 2019-12-30 10:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voluntariapp', '0002_week_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ForumTheme',
            new_name='ForumTopic',
        ),
    ]
