# Generated by Django 2.2 on 2019-09-10 20:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20190909_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 12, 20, 58, 51, 244310, tzinfo=utc), verbose_name='актуальность ключа'),
        ),
    ]
