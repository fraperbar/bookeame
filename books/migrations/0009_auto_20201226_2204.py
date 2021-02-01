# Generated by Django 3.1.2 on 2020-12-26 21:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20201226_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todostuslibros',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='todostuslibros',
            name='url_libro',
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='autor',
            field=models.TextField(default='sin definir'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='descripcion',
            field=models.TextField(default='sin descripcion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='fechapublicacion',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='isbn',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='titulo',
            field=models.TextField(default='sin titulo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todostuslibros',
            name='urlImagen',
            field=models.URLField(default='nada'),
            preserve_default=False,
        ),
    ]