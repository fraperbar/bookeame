from django.shortcuts import render, redirect
from .models import Genero, Libro, LibrosNuevosGeneros, LibrosLeidosSemana, TodosTusLibros
from .scrapping import *
import re
from django.contrib.auth.models import Group
from .recommendations import  transformPrefs, getRecommendations, topMatches, getRecommendedItems,calculateSimilarItems
import shelve
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from .Whoosh import *
from .forms import *
import datetime
from django.shortcuts import render, get_object_or_404
#Cargas en la bd desde GoodReads, desde todos tus libros y desde el dataset, borrado de la bd (el dataset no debido a su tamaño)

def carga_bd(request):
    group = Group.objects.get(name="librero")
    if (not request.user.is_superuser and not (group in request.user.groups.all()) ):
        return redirect("/error")

    return render(request, 'cargar.html')

def carga_planeta_recomendados(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_libros_planeta("https://www.planetadelibros.com/seleccion-editorial/libros-recomendados/132",
            "Descubre nuestra selección de libros recomendados para leer durante este 2021", True)
            mensaje="Se han almacenado: " + str(libros) +" libros. "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def carga_planeta_nuevos(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_libros_planeta("https://www.planetadelibros.com/libros-novedades",
            "Últimas novedades en libros", False)
            mensaje="Se han almacenado: " + str(libros) +" libros. "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')


def carga_generos(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            generos = extraer_generos()
            mensaje="Se han almacenado: " + str(generos) +" generos, "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def carga_libros(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_libros_nuevos()
            mensaje="Se han almacenado: " + str(libros) +" libros "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')



def carga_libros_leidos(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_libros_leidos()
            mensaje="Se han almacenado: " + str(libros) +" libros "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def carga_ttl(request):
    group = Group.objects.get(name="librero")
    if (not request.user.is_superuser and not (group in request.user.groups.all()) ):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_precios()
            mensaje="Se han almacenado: " + str(libros) +" libros "
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def borrar_ttl(request):
    group = Group.objects.get(name="librero")
    if (not request.user.is_superuser and not (group in request.user.groups.all()) ):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST: 
            c = TodosTusLibros.objects.all().count()     
            TodosTusLibros.objects.all().delete()
            mensaje = "Se han borrado "+ str(c) + " libros de TodosTusLibros."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionborrar.html')

def carga_libros_dataset(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = extraer_libros_dataset()
            usuarios = extraer_usuarios_dataset()
            bookRatings = extraer_bookrating_dataset()
            mensaje="Se han almacenado: " + str(libros) +" libros votados, "+ str(usuarios)+" votantes, "+bookratings+"votaciones"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def borrar_bd(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:  
            contador=0    
            todostuslibros=TodosTusLibros.objects.all()
            contador+= todostuslibros.count()
            libros = PlanetaLibros.objects.all()
            contador +=libros.count()

            todostuslibros.delete()
            libros.delete()
            mensaje="Se han borrado: " + str(contador) +" entradas"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionborrar.html')
    
#Indexar con Whoosh, primero con los de goodreads y despues con los de todos tus libros
def indexa_libros(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = indexar_datos_libros()
            mensaje="Se han indexado: " + str(libros) +" libros."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
def indexa_librosGeneral(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = indexar_buscador_general()
            mensaje="Se han indexado: " + str(libros) +" libros."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
def indexa_librosTtl(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            libros = indexar_datos_ttl()
            mensaje="Se han indexado: " + str(libros) +" libros."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
#CARGAR LA RS-----------------------
def cargar_rs(request):
    if (not request.user.is_superuser):
        return redirect("/error")
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            loadDict()
            mensaje="Se ha cargado el RS"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')


#---------------------------Mostrar datos--------------------------------------------
def planeta_libros(request):
    libros_nuevos = PlanetaLibros.objects.filter(recomendado=False).all()
    libros_recomendados = PlanetaLibros.objects.filter(recomendado=True).all()

    return render(request, 'planetalibros.html', {"libros_nuevos":libros_nuevos,"libros_recomendados":libros_recomendados})

def inicio(request):
    lista_libros=[]
    for g in Genero.objects.all():
        i=0
        #Mostramos 5 libros al principio por genero
        while(i<5):
            ls = Libro.objects.filter(genero=g).all()[i]
            lista_libros.append(ls)
                
            i+=1

    return render(request, 'index.html', {"libs":lista_libros})
#Una forma de hacer el paginado de TodosTusLibros
class todostuslibros(ListView):
    template_name="todostuslibroslist.html"
    model = TodosTusLibros
    paginate_by = 10
    context_object_name="libros"
#Generos más detallados
def mostrar_genero(request, nombre_genero):
    genero =  get_object_or_404(Genero, nombre=nombre_genero)
    lls=[]
    mensaje=""
    if(nombre_genero!="Ebooks"):
        lls = LibrosLeidosSemana.objects.get(genero=genero).libros.all()
    else:
        mensaje = "No cuenta con libros más leidos"   
    lng = LibrosNuevosGeneros.objects.get(genero=genero).libros.all()

    return render(request, 'showgenero.html',{"lls":lls,"lng":lng, "msj":mensaje})

#Libro de goodreads detallado
def mostrar_libro(request, libro_id):
    libro  = get_object_or_404(Libro, pk=libro_id)

    return render(request, 'showlibro.html', {'libro':libro})
#--------------------------Recomendaciones----------------------------------------
def loadDict_user(user_id):
    '''actualiza los datos con las votaciones del usuario'''
    Prefs={}   
    shelf = shelve.open("dataRS.dat")
    ratings = LibroUsuarioRating.objects.filter(user_id=user_id).all()
    for r in ratings:
        user = int(r.user_id.user_id)
        itemid = str(r.isbn.isbn)
        book_rating = int(r.book_rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = book_rating
    temp = shelf['Prefs']
    temp.update(Prefs)
    shelf['Prefs'] = temp
    temp2 = shelf['ItemsPrefs']
    temp2.update(transformPrefs(Prefs))
    shelf['ItemsPrefs'] = temp2
    shelf.close()

def loadDict():
    Prefs={}  
    shelf = shelve.open("dataRS.dat")
    ratings = LibroUsuarioRating.objects.all()
    for r in ratings:
        user = int(r.user_id.user_id)
        itemid = str(r.isbn.isbn)
        book_rating = int(r.book_rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = book_rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def misvotaciones(request, page):
    '''Muestra las votaciones de cada usuario'''
    if (not request.user.is_authenticated):
        return redirect("/error")
    pagination = (page-1)*10
    votaciones = LibroUsuarioRating.objects.filter(user_id=278858+request.user.pk).all()[pagination:page*10]

    return render(request, 'recomendaciones/misvotaciones.html', {"votaciones":votaciones,"page0":page-1, "page1":page+1})


def recomendaciones(request):
    if (not request.user.is_authenticated):
        return redirect("/error")
    try:
        user_id = 278858+request.user.pk
        shelf = shelve.open("dataRS.dat")
        Prefs = shelf['Prefs']
        shelf.close()
        items={}
        rankings = getRecommendations(Prefs,int(user_id))
        recommended = rankings[:100]
        libros = []
        scores = []
        for re in recommended:
            libros.append(LibroVotado.objects.get(pk=re[1]))
            scores.append(re[0])
        items= zip(libros,scores)
    except:
        print("sin recomendaciones")
    
    return render(request,'recomendaciones/recomendaciones.html', {'items': items})

def libros_similares(request, isbn):
    '''En mis votacionse muestra los libros similares a los que se han votado'''
    if (not request.user.is_authenticated):
        return redirect("/error")
    libro = LibroVotado.objects.get( isbn=isbn)
    shelf = shelve.open("dataRS.dat")
    ItemsPrefs = shelf['ItemsPrefs']
    shelf.close()
    recommended = topMatches(ItemsPrefs, str(isbn),n=10)
    libros = []
    similar = []
    for re in recommended:
        libros.append(LibroVotado.objects.get(pk=re[1]))
        similar.append(re[0])
    items= zip(libros,similar)
    return render(request,'recomendaciones/libros_similares.html', {'libro': libro,'items': items})

def verRecomendacionesUsuarios(request):
    '''el super user puede ver las recomendaciones que se le hacen a los distintos usuarios '''
    if (not request.user.is_superuser):
        return redirect("/error")
    items = {}
    user = None
    if request.method=='GET':
        formusuario = id_form_user(request.GET)
        if formusuario.is_valid():
            user_id = formusuario.cleaned_data['id_user']
            user = get_object_or_404(UsuarioVotante, user_id=user_id)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()

            rankings = getRecommendations(Prefs,int(user_id))
            recommended = rankings[:2]
            libros = []
            scores = []
            for re in recommended:
                libros.append(LibroVotado.objects.get(isbn=re[1]))
                scores.append(re[0])
            items = zip(libros, scores)
    formusuario = id_form_user()
    return render(request, 'recomendaciones/todosusuarios.html',{'user': user, 'items': items,"formusuario":formusuario})


def ver_recomendaciones_user(request):
    if (not request.user.is_authenticated):
        return redirect("/error")
    try:
        user_id = UsuarioVotante.objects.get(user_id=278858+request.user.pk)
        loadDict_user(user_id)
    except:
        print("Aun no se ha hecho ningun voto")
        
    return redirect("/recomendaciones")

def crear_usuarios_votantes(request, page):
    '''Cuando un usuario vota, se crea un usuario votante si no lo estuviera ya para que le salgan las recomendaciones '''
    if (not request.user.is_authenticated):
        return redirect("/error")
    formVotante = votante_rating()
    if request.method=='POST':
        #le damos el ultimo id de los usuarios + el propio id del usuario
        user, created = UsuarioVotante.objects.get_or_create(user_id=278858+request.user.pk)
        if(not created):
            user.save()
        libroVotado = LibroVotado.objects.get(isbn=request.POST.get("isbn",""))
        libroRating = LibroUsuarioRating(isbn=libroVotado, user_id=user, book_rating=request.POST.get("rating",""))
        
        libroRating.save()

    pagination = (page-1)*10
    libros = LibroVotado.objects.all()[pagination:page*10]
    if request.method=="GET":
        if(request.GET.get("tit")):
            libros = LibroVotado.objects.filter(titulo__contains=request.GET.get("tit")).all()[0:10]
        if(request.GET.get("autor")):
            libros = LibroVotado.objects.filter(autor__contains=request.GET.get("autor")).all()[0:10]
        if(request.GET.get("isbn")):
            libros = LibroVotado.objects.filter(isbn=request.GET.get("isbn")).all()
                
    return render(request, 'recomendaciones/votar.html', {"formVotante":formVotante,"libros":libros,"page0":page-1, "page1":page+1})
#-------------------Buscadores----------------------------------
def buscador_general(request):
    if(request.method=='GET'):
        pks = buscartituloOisbn(request.GET["titulo_isbn"], "IndexGeneral")
        librosdtst = []
        librosttl=[]
        librosgr = []
        librospl = []
        for pk in pks:
            if(pk[1]=="dtst"):
                librosdtst.append(LibroVotado.objects.get(isbn=pk[0]))
            if(pk[1]=="ttl"):
                librosttl.append(TodosTusLibros.objects.get(pk=pk[0]))
            if(pk[1]=="gr"):

                librosgr.append(Libro.objects.get(pk=pk[0]))
            if(pk[1]=="pl"):
                librospl.append(PlanetaLibros.objects.get(pk=pk[0]))
    return render(request,'buscadorgeneral.html',{"librosdtst":librosdtst,"librosttl":librosttl,"librosgr":librosgr,
    "librospl":librospl})
def buscadoresttl(request):
    
    formtext = libro_text_form()
    listalibros = []
    formautor = libro_autor_form()
    formisbn = libro_isbn_form()
    formfecha =  libro_fecha_form()
    formprecio= libro_precio_form()
    formgenero= libro_generottl_form()
    errores = []
    if request.method=='GET':
        formulario_texto = libro_text_form(request.GET)
        formulario_autor = libro_autor_form(request.GET)
        formulario_isbn = libro_isbn_form(request.GET)
        formulario_precio = libro_precio_form(request.GET)
        formulario_fecha = libro_fecha_form(request.GET)
        formulario_genero = libro_generottl_form(request.GET)

        if(formulario_texto.is_valid()):
            res = buscartituloOdescripcion(formulario_texto.cleaned_data['text'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)

        if(formulario_autor.is_valid()):
            res = buscarAutor(formulario_autor.cleaned_data['autor'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)

        if(formulario_isbn.is_valid()):
            res = buscarISBN(formulario_isbn.cleaned_data['isbn'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)
            if(len(listalibros)==0):
                print(extraer_unico_libro(formulario_isbn.cleaned_data['isbn']))
                listalibros.append(extraer_unico_libro(formulario_isbn.cleaned_data['isbn']))
        
        if(formulario_fecha.is_valid()):
            res = buscarFechas(formulario_fecha.cleaned_data['fechaInicio'],formulario_fecha.cleaned_data['fechaFinal'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)

        if(formulario_precio.is_valid()):
            res = buscarPrecio(formulario_precio.cleaned_data['precio'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)
        if(formulario_genero.is_valid()):
            res = buscarGenero(formulario_genero.cleaned_data['genero'],"IndexTtl")
            for r in res:
                libro = TodosTusLibros.objects.get(pk=int(r))
                listalibros.append(libro)
        

    return render(request, 'buscadorttl.html', {"formtext":formtext,"errores":errores, "formautor":formautor, "libros":listalibros,
    "formisbn":formisbn,"formfecha":formfecha,"formprecio":formprecio,"formgenero":formgenero})
def buscadores(request):
    
    formtext = libro_text_form()
    listalibros = []
    formautor = libro_autor_form()
    formisbn = libro_isbn_form()
    formrating = libro_rating_form()
    formfecha =  libro_fecha_form()
    formgenero =  libro_genero_form()
    errores = []
    if request.method=='GET':
        formulario_texto = libro_text_form(request.GET)
        formulario_autor = libro_autor_form(request.GET)
        formulario_isbn = libro_isbn_form(request.GET)
        formulario_rating = libro_rating_form(request.GET)
        formulario_fecha = libro_fecha_form(request.GET)
        formulario_genero = libro_genero_form(request.GET)
        if(formulario_texto.is_valid()):
            res = buscartituloOdescripcion(formulario_texto.cleaned_data['text'],"IndexLibro")
            for r in res:
                libro = Libro.objects.get(pk=int(r))
                listalibros.append(libro)
        if(formulario_autor.is_valid()):
            res = buscarAutor(formulario_autor.cleaned_data['autor'],"IndexLibro")
            for r in res:
                libro = Libro.objects.get(pk=int(r))
                listalibros.append(libro)

        if(formulario_isbn.is_valid()):
            res = buscarISBN(formulario_isbn.cleaned_data['isbn'],"IndexLibro")
            if(len(res)>0):
                return redirect("/libros/"+str(res[0]))

        if(formulario_rating.is_valid()):
            res = buscarRating(formulario_rating.cleaned_data['rating'],"IndexLibro")
            if(float(formulario_rating.cleaned_data['rating'])<0.0):
                errores.append("El rating tiene que ser mayor o igual a 0")
            elif (float(formulario_rating.cleaned_data['rating']>5.0)):
                errores.append("El rating tiene que ser menor o igual a 5")
            for r in res:
                libro = Libro.objects.get(pk=int(r))
                listalibros.append(libro)
        
        if(formulario_fecha.is_valid()):
            res = buscarFechas(formulario_fecha.cleaned_data['fechaInicio'],formulario_fecha.cleaned_data['fechaFinal'],"IndexLibro")
            for r in res:
                libro = Libro.objects.get(pk=int(r))
                listalibros.append(libro)

        if(formulario_genero.is_valid()):
            res = buscarGenero(formulario_genero.cleaned_data['genero'],"IndexLibro")
            for r in res:
                libro = Libro.objects.get(pk=int(r))
                listalibros.append(libro)

    return render(request, 'buscador.html', {"formtext":formtext,"errores":errores, "formautor":formautor, "libros":listalibros,
    "formisbn":formisbn,"formrating":formrating,"formfecha":formfecha,"formgenero":formgenero})
#-------------------Gestión usuario-----------------------------
def error(request):
    return render(request, "error.html")
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        x = form.fields['username']
        x.label = "Nombre de usuario"
        x.help_text = ""
        
        x = form.fields['password1']
        x.label = "Contraseña"
        x.help_text = ""
        x = form.fields['password2']
        x.label = "Confirma la contraseña"
        x.help_text = ""
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        x = form.fields['username']
        x.label = "Nombre de usuario"
        x.help_text = ""
        
        x = form.fields['password1']
        x.label = "Contraseña"
        x.help_text = ""
        x = form.fields['password2']
        x.label = "Confirma la contraseña"
        x.help_text = ""
    return render(request, 'registration/signup.html', {'form': form})


