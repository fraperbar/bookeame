# Generated by Django 3.1.2 on 2020-12-24 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_libro_librosnuevosgeneros'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librosnuevosgeneros',
            name='libro',
        ),
        migrations.AddField(
            model_name='librosnuevosgeneros',
            name='libros',
            field=models.ManyToManyField(to='books.Libro'),
        ),
    ]