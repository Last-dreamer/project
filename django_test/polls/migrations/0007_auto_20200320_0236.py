# Generated by Django 3.0.4 on 2020-03-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='polls.Tags'),
        ),
    ]
