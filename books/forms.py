from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Genero, TodosTusLibros
class libro_text_form(forms.Form):
    text = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Palabras relacionadas','class': 'form-control'}))

class libro_autor_form(forms.Form):
    autor = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Nombre autor','class': 'form-control'}))

class libro_isbn_form(forms.Form):
    isbn = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'ISBN','class': 'form-control'}))

class libro_rating_form(forms.Form):
    rating = forms.FloatField(label='',widget=forms.TextInput(attrs={'placeholder': 'Rating <= 5','class': 'form-control'}))

class libro_genero_form(forms.Form):
    lista=[(g.nombre, g.nombre) for g in Genero.objects.all()]
    genero = forms.ChoiceField(label="", choices=lista)

class libro_precio_form(forms.Form):
    precio = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Precio máximo','class': 'form-control'}))

class libro_fecha_form(forms.Form):
    fechaInicio = forms.CharField(label='Desde', widget= forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy','class': 'form-control',"style":"margin-left:10px; margin-right:10px;"}))
    fechaFinal = forms.CharField(label='Hasta', widget= forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy','class': 'form-control',"style":"margin-left:10px;"}))
class libro_generottl_form(forms.Form):
    lista=[]
    for libro in TodosTusLibros.objects.all():
        generos =  libro.categorias.split(", ")
        for genero in generos:
            if (genero, genero) not in lista:
                lista.append((genero, genero))
    genero = forms.ChoiceField(label="", choices=lista)
class id_form_user(forms.Form):
    id_user = forms.IntegerField(label="",widget= forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy','class': 'form-control',"style":"margin-left:10px; margin-right:10px;"}))
class votante_rating(forms.Form):
    i=0
    lista = []
    while(i<11):
        lista.append((i,i))
        i+=1
    rating = forms.ChoiceField(label="", choices=lista)