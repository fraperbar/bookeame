# Generated by Django 3.1.2 on 2021-01-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_remove_todostuslibros_categorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='todostuslibros',
            name='categorias',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
