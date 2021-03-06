# Generated by Django 3.1.2 on 2020-12-27 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_librovotado_usuariovotante'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroUsuarioRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_rating', models.IntegerField()),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.librovotado')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.usuariovotante')),
            ],
        ),
    ]
