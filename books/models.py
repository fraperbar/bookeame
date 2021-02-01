from django.db import models

#GoodReads
class Genero(models.Model):
    nombre=models.TextField(help_text="Introduce el nombre del género")
    href=models.TextField(help_text="url para acceder en goodreads")
    
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    isbn = models.IntegerField()
    titulo = models.TextField()
    autor = models.TextField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    descripcionHTML = models.TextField()
    href = models.TextField(unique=True)
    urlImagen = models.URLField()
    rating = models.FloatField()
    fechapublicacion = models.DateTimeField(null=True)
    def __str__(self):
        return self.titulo

class LibrosNuevosGeneros(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    libros = models.ManyToManyField(Libro)
    ultimaactualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.genero.nombre

class LibrosLeidosSemana(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    libros = models.ManyToManyField(Libro)
    ultimaactualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.genero.nombre
#TodosTusLibros
class TodosTusLibros(models.Model):
    titulo = models.TextField()
    isbn = models.IntegerField()
    precio = models.TextField()
    autor = models.TextField()
    categorias = models.TextField()
    urlImagen = models.URLField()
    fechapublicacion = models.DateTimeField()
    descripcion = models.TextField()
    urlCompra = models.URLField()

    def __str__(self):
        return self.titulo

#PlanetaLibros
class PlanetaLibros(models.Model):
    titulo = models.TextField()
    isbn = models.IntegerField()
    #Si es recomendado esta a true y si es nuevo se evalua a false.
    recomendado = models.BooleanField()
    precio = models.TextField()
    autor = models.TextField()
    categorias = models.TextField()
    urlImagen = models.URLField()
    fechapublicacion = models.DateTimeField()
    descripcionHTML = models.TextField()
    urlCompra = models.URLField()

    def __str__(self):
        return self.titulo

    
#modelos del dataset
class UsuarioVotante(models.Model):
    user_id=models.IntegerField(primary_key=True)
    location = models.TextField(null=True)
    edad= models.IntegerField(null=True)

class LibroVotado(models.Model):
    isbn = models.TextField(primary_key=True)
    titulo = models.TextField()
    autor = models.TextField()
    anyopublicacion = models.TextField()
    urlImg = models.URLField()
    def __str__(self):
        return self.titulo

class LibroUsuarioRating(models.Model):
    user_id = models.ForeignKey(UsuarioVotante, on_delete=models.CASCADE)
    isbn = models.ForeignKey(LibroVotado, on_delete=models.CASCADE)
    book_rating = models.IntegerField()
