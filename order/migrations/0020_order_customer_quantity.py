# Generated by Django 3.0.3 on 2020-07-21 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_auto_20200720_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_quantity',
            field=models.CharField(default=1, max_length=30),
        ),
    ]