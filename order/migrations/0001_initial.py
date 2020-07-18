# Generated by Django 2.2.7 on 2020-07-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=30, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='order_images')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('price', models.CharField(blank=True, max_length=20, null=True)),
                ('brand', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
