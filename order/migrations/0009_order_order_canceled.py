# Generated by Django 2.2.7 on 2020-07-15 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20200715_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
