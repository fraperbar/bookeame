# Generated by Django 3.1.2 on 2020-12-25 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20201225_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='fechapublicacion',
            field=models.DateTimeField(null=True),
        ),
    ]
