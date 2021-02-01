from django.contrib import admin
from .models import *

admin.site.register(Genero)
class LibroAdmin(admin.ModelAdmin):
    search_fields=["href", "titulo"]
admin.site.register(Libro, LibroAdmin)
admin.site.register(LibrosNuevosGeneros)
admin.site.register(LibrosLeidosSemana)

class TodosTusLibrosAdmin(admin.ModelAdmin):
    search_fields=["isbn"]

class LibroVotadoAdmin(admin.ModelAdmin):
    search_fields=["isbn"]

admin.site.register(TodosTusLibros, TodosTusLibrosAdmin)
admin.site.register(LibroVotado, LibroVotadoAdmin)
admin.site.register(LibroUsuarioRating)
admin.site.register(UsuarioVotante)
admin.site.register(PlanetaLibros)
