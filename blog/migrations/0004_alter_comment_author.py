# Generated by Django 4.0.5 on 2023-03-10 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_options_alter_comment_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default='anonymous', max_length=100),
        ),
    ]
