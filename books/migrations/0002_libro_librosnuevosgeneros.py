# Generated by Django 3.1.2 on 2020-12-24 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.IntegerField()),
                ('titulo', models.TextField()),
                ('autor', models.TextField()),
                ('descripcionHTML', models.TextField()),
                ('urlImagen', models.URLField()),
                ('rating', models.FloatField()),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.genero')),
            ],
        ),
        migrations.CreateModel(
            name='LibrosNuevosGeneros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.genero')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.libro')),
            ],
        ),
    ]
