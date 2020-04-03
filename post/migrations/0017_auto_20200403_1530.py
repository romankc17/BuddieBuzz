# Generated by Django 3.0.4 on 2020-04-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20200403_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='created',
            new_name='post_comment_created',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='updated',
        ),
        migrations.AddField(
            model_name='postcomment',
            name='post_comment_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
