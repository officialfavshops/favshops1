# Generated by Django 3.0.3 on 2020-07-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0006_auto_20200723_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Grocery', 'Grocery'), ('Snacks', 'Snacks'), ('Cooking oil', 'Cooking oil'), ('Tooth paste', 'Tooth paste'), ('Soap', 'Soap'), ('Beauty_products', 'Beauty_products'), ('Drinks', 'Drinks'), ('Masala', 'Masala'), ('Hair oil', 'Hair oil'), ('Yeepi noodles', 'Yeepi noodles'), ('Finail', 'Finail'), ('Biscuts', 'Biscuts'), ('Tea', 'Tea'), ('Detergent', 'Detergent'), ('Sanitary napkins', 'Sanitary napkins'), ('Face Cream', 'Face Cream'), ('Powders', 'Powders'), ('Purfumes', 'Purfumes'), ('Others', 'Others')], max_length=20),
        ),
    ]