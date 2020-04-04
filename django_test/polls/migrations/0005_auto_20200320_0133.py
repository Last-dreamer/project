# Generated by Django 3.0.4 on 2020-03-20 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200320_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('indoor', 'indoor'), ('outDoor', 'outdoor')], max_length=100, null=True),
        ),
    ]