# Generated by Django 3.0.2 on 2020-01-13 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='admin', max_length=100),
            preserve_default=False,
        ),
    ]
