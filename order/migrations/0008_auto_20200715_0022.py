# Generated by Django 2.2.7 on 2020-07-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_delete_orderid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='packed',
            field=models.BooleanField(default=False),
        ),
    ]
