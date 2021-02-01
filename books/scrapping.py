from bs4 import BeautifulSoup
import urllib.request
import datetime
import re

from .models import *

def extraer_libros_planeta(url, titulo, recomendado):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")
    l = s.find_all("div", class_=["rotador","rotador-300"])
    contador=0
    PlanetaLibros.objects.filter(recomendado=recomendado).all().delete()
    #por si alguna vez no fuera el primer div
    for i in l:
        if(i.find("h2",class_="titol")!=None):
            if(i.find("h2",class_="titol").string==titulo):
                l1 = i.find_all("li")
                for i1 in l1:
                    href = i1.find("a", class_="tagmanager")["href"]
                    titulo = i1.find("div", class_="titol").string
                    print(titulo)
                    isbn = i1.find("a", class_="tagmanager")["data-isbn"]
                    autor = i1.find("div", class_="autors").string
                    if(autor==None):
                        autor = "Autor no registrado"
                    print(autor)
                    urlCompra = i1.find("span", class_="btn-comprar")["data-fancybox-href"]
                    f2 = urllib.request.urlopen(href)
                    s2 = BeautifulSoup(f2,"lxml")
                    descripcionesP = s2.find("div", class_="sinopsi").find_all("p")
                    parrafos = []
                    for descripciones in descripcionesP:
                        parrafos.append(str(descripciones))
                    descripcion = "<br>".join(parrafos)
                    fecha = s2.find("span", itemprop="datePublished").string
                    cats = []
                    for c in s2.find("div",class_="tematica").find_all("a"):
                        cats.append(c.string)
                    precio = s2.find("div",class_="preu_format").string
                    categorias=",".join(cats)
                    urlImagen = s2.find("img", class_="photo")["src"]
                    year=int(fecha.split("/")[2])
                    mes = int(fecha.split("/")[1])
                    dia=int(fecha.split("/")[0])
                    PL = PlanetaLibros(isbn=isbn,titulo=titulo,autor=autor,urlImagen=urlImagen,
                    fechapublicacion=datetime.datetime(year, mes, dia), precio=precio, categorias=categorias, descripcionHTML=descripcion ,urlCompra=urlCompra, 
                    recomendado=recomendado)
                    PL.save()
                    contador+=1
    return contador

def extraer_unico_libro(isbn):
    ttl = TodosTusLibros(titulo="No se ha encontrado resultados.", urlImagen="https://www.forewordreviews.com/books/covers/beyond-success.jpg")
    try:
        f = urllib.request.urlopen("https://www.todostuslibros.com/busquedas?keyword="+isbn)
        print("https://www.todostuslibros.com/busquedas?keyword="+isbn)
        s = BeautifulSoup(f,"lxml")
        l= s.find_all("li", class_=["book", "row"])
        for b in l:
            isbn = b.find("p", class_=["data"]).string.strip().split("/")[1].replace("-", "").strip()
            precio = b.find("div",class_=["book-price"]).find("strong").string.strip()
            titulo = b.find("h2", class_=["title"]).find("a").string.strip()  
            autor = b.find("h3", class_=["author"]).string.strip()
            urlLibro = b.find("h2", class_=["title"]).find("a")["href"]
            f1 = urllib.request.urlopen(urlLibro)
            s1 = BeautifulSoup(f1,"lxml")
            itdt = 0
            urlImagen = s1.find("div", class_="book-image").find("img")["src"]
            fechapublidt = s1.find_all("dt")
            fechapubli = s1.find_all("dd")
            listacategorias = []
            for fpdt in fechapublidt:
                if(fpdt.string=="Fecha publicación :"):
                    fechapublicacion = fechapubli[itdt].string

                if(fpdt.string.strip()=="Materias:"):
                    materias = fechapubli[itdt].find_all("a")
                    for materia in materias:
                        listacategorias.append(materia.string)
                itdt+=1
            categorias = ", ".join(listacategorias)
            print(fechapublicacion)
            year=int(fechapublicacion.split("-")[2])
            mes = int(fechapublicacion.split("-")[1])
            dia=int(fechapublicacion.split("-")[0])
            try:
                descripcion = s1.find("div", id="synopsis").find("div", class_=["col-md-9", "synopsis"]).find("p").string
            except: 
                descripcion = "sin descripción"
            ttl = TodosTusLibros(isbn=isbn,titulo=titulo,autor=autor,urlImagen=urlImagen,fechapublicacion=datetime.datetime(year, mes, dia),
                    precio=precio,descripcion=descripcion, urlCompra=urlLibro, categorias=categorias)
    except:
        print("no encontrado")
    return ttl

def extraer_precios():
    '''Obtiene los libros de TodosTusLibros.com'''
    pagina=1
    it=0
    while(pagina<11):
        f = urllib.request.urlopen("https://www.todostuslibros.com/mas_vendidos?page="+str(pagina))
        pagina+=1

        s = BeautifulSoup(f,"lxml")
        l= s.find_all("li", class_=["book", "row"])
        for b in l:
            isbn = b.find("p", class_=["data"]).string.strip().split("/")[1].replace("-", "").strip()
            if(not TodosTusLibros.objects.filter(isbn=isbn).exists()):
                precio = b.find("div",class_=["book-price"]).find("strong").string.strip()
                titulo = b.find("h2", class_=["title"]).find("a").string.strip()
                print(titulo)
                autor = b.find("h3", class_=["author"]).string.strip()
                urlLibro = b.find("h2", class_=["title"]).find("a")["href"]
                f1 = urllib.request.urlopen(urlLibro)
                s1 = BeautifulSoup(f1,"lxml")
                itdt = 0
                urlImagen = s1.find("div", class_="book-image").find("img")["src"]
                fechapublidt = s1.find_all("dt")
                fechapubli = s1.find_all("dd")
                
                listacategorias = []
                for fpdt in fechapublidt:
                    if(fpdt.string=="Fecha publicación :"):
                        fechapublicacion = fechapubli[itdt].string

                    if(fpdt.string.strip()=="Materias:"):
                        materias = fechapubli[itdt].find_all("a")
                        for materia in materias:
                            listacategorias.append(materia.string)
                    itdt+=1
                categorias = ", ".join(listacategorias)
                year=int(fechapublicacion.split("-")[2])
                mes = int(fechapublicacion.split("-")[1])
                dia=int(fechapublicacion.split("-")[0])
                try:
                    descripcion = s1.find("div", id="synopsis").find("div", class_=["col-md-9", "synopsis"]).find("p").string
                except:
                    descripcion = "sin título"
                ttl = TodosTusLibros(isbn=isbn,titulo=titulo,autor=autor,urlImagen=urlImagen,fechapublicacion=datetime.datetime(year, mes, dia),
                precio=precio,descripcion=descripcion, urlCompra=urlLibro, categorias=categorias)
                ttl.save()
                it+=1
    return it

def extraer_libros_nuevos():
    '''extrae los libros por genero de la seccion de nuevos del genero, guardamos el href para que la 
    actualización sea más rápida'''
    generos= Genero.objects.all()
    LibrosNuevosGeneros.objects.all().delete()
    
    counter=0
    for g in generos:
        f = urllib.request.urlopen("https://www.goodreads.com"+g.href)
        s = BeautifulSoup(f,"lxml")
        l = s.find("div",class_="bigBoxBody").find_all("div", class_=["coverRow"])
        lib_n = LibrosNuevosGeneros(genero=g)
        lib_n.save()
        for i in l:
            l2 =i.find_all("div", class_=["leftAlignedImage", "bookBox"])
            for j in l2:
                guardar=True
                href= j.find("a")['href']
                print(href)
                #Para poder actualizar la lista más rapido y que no entre en todos los libros si ya están agredados
                if(not Libro.objects.filter(href=href).exists()):
                    f1 = urllib.request.urlopen("https://www.goodreads.com/"+href)
                    s1 = BeautifulSoup(f1,"lxml")
                    
                    try:
                        #Debido a una razón desconocida estos atributos que antes no fallaban(en diciembre) han fallado (en enero) pero solo en algunos libros,
                        #además estos libros no proporcionan un sitio que se le pueda hacer bien scrapping, si no que usan javascript.
                        #la decision tomada es no guardar estos libros
                        isbn = s1.find("meta", property="books:isbn")["content"]
                        if(isbn=="null"):
                            isbn=0
                        autor = s1.find("a", class_=["authorName"]).find("span", itemprop="name").string
                        titulo = s1.find("h1", id="bookTitle").string.strip()
                        rating = s1.find("span", itemprop="ratingValue").string
                        urlImagen = s1.find("img", id="coverImage")["src"]
                    except: 
                        guardar=False
                    try:
                        fechapublicacion = formatear_fecha(s1.find("div", id="details").find_all("div")[1].string.split("\n")[2].strip())
                    except:
                        fechapublicacion= None
                    try:
                        descripcion = str(s1.find("div", id="description").find_all("span")[1])
                    except:
                        descripcion = "sin descripción"
                    if(guardar):
                        lib = Libro(isbn=isbn, titulo=titulo, autor=autor, href=href, genero=g,descripcionHTML=descripcion,urlImagen=urlImagen,rating=rating, fechapublicacion=fechapublicacion)
                        lib.save()
                        lib_n.libros.add(lib)
                else:
                    lib = Libro.objects.get(href=href)
                    lib_n.libros.add(lib)
                counter +=1

    return counter
def extraer_libros_leidos():
    '''extrae los libros mas leidos por genero de goodreads, guardamos el href para que la 
    actualización sea más rápida'''
    generos= Genero.objects.all()
    LibrosLeidosSemana.objects.all().delete()
    
    counter=0
    for g in generos:
        #Ebooks no tiene mas leidos
        if(g.nombre!="Ebooks"):
            f = urllib.request.urlopen("https://www.goodreads.com"+g.href)
            s = BeautifulSoup(f,"lxml")
            filtro = s.find_all("div",class_=["coverBigBox","clearFloats","bigBox"])
            lib_n = LibrosLeidosSemana(genero=g)
            lib_n.save()
            l=[]
            for fil in filtro:
                filt  = fil.find("h2", class_="brownBackground").string
                if(str(filt).split(" ")[0]=='Most'):
                    l=fil.find("div", class_="bigBoxBody").find_all("div", class_=["coverRow"])
    
            for i in l:
                l2 =i.find_all("div", class_=["leftAlignedImage", "bookBox"])
                for j in l2:
                    href= j.find("a")['href']
                    print(href)
                    #Para poder actualizar la lista más rapido y que no entre en todos los libros si ya están agredados
                    if(not Libro.objects.filter(href=href).exists()):
                        f1 = urllib.request.urlopen("https://www.goodreads.com/"+href)
                        s1 = BeautifulSoup(f1,"lxml")
                        isbn = s1.find("meta", property="books:isbn")["content"]
                        if(isbn=="null"):
                            isbn=0
                        autor = s1.find("a", class_=["authorName"]).find("span", itemprop="name").string
                        titulo = s1.find("h1", id="bookTitle").string.strip()
                        print(titulo)
                        try:
                            fechapublicacion = formatear_fecha(s1.find("div", id="details").find_all("div")[1].string.split("\n")[2].strip())
                        except:
                            fechapublicacion= None
                        urlImagen = s1.find("img", id="coverImage")["src"]
                        try:
                            descripcion = str(s1.find("div", id="description").find_all("span")[1])
                        except:
                            descripcion = "sin descripción"
                        rating = s1.find("span", itemprop="ratingValue").string
                        lib = Libro(isbn=isbn, titulo=titulo, autor=autor, href=href, genero=g,descripcionHTML=descripcion,urlImagen=urlImagen,rating=rating, fechapublicacion=fechapublicacion)
                        lib.save()
                        lib_n.libros.add(lib)
                    else:
                        lib = Libro.objects.get(href=href)
                        lib_n.libros.add(lib)
                    counter +=1

    return counter
def extraer_generos():
    '''Extrae los generos y su link'''
    f = urllib.request.urlopen("https://www.goodreads.com/")
    s = BeautifulSoup(f,"lxml")
    l = s.find("div", id="browseBox").find("div", class_=["u-defaultType"]).find_all("a", class_=["gr-hyperlink"])
    counter=0
    for i in l:
        if(i.string!="More genres" and not Genero.objects.filter(nombre=i.string).exists()):
            g = Genero(nombre=i.string, href=i["href"])
            g.save()
            counter+=1
    return counter
#Extraer datos de datasets
path = "data"

def extraer_libros_dataset():
    fil = open(path+"\\BX-Books.csv")
    i=0
    counter = 0
    listaObjetos = []
    for line in fil.readlines():
        if(i!=0):

            lsplit = line.split(";")
            isbn = lsplit[0].replace('"','')
            titulo = lsplit[1].replace('"','')
            autor = lsplit[2].replace('"','')
            publicacion = lsplit[3].replace('"','')
            urlImg = lsplit[5].replace('"','')
            if(not LibroVotado.objects.filter(isbn=isbn).exists()):
                lv = LibroVotado(isbn=isbn, titulo=titulo, autor=autor, anyopublicacion=publicacion, urlImg=urlImg)
                listaObjetos.append(lv)
            counter+=1
        i+=1
    LibroVotado.objects.bulk_create(listaObjetos)
            

        
    return counter
def extraer_usuarios_dataset():
    
    fil = open(path+"\\BX-Users.csv")
    i=0
    counter=0
    listaObjetos = []
    for line in fil.readlines():
        if(i!=0):
            
            lsplit = line.split(";")
            user_id = int(lsplit[0].replace('"',''))
            #la location tiene el problema de que tiene algunos ";" por lo que hay veces que se guarda mal
            location = lsplit[1].replace('"','')
            #por lo anterior cogemos el ultimo elemento de la lista en lugar del 2
            edad = lsplit[-1].replace('"','')
            if(edad == "NULL\n"):
                edad = None
            else: 
                edad = int(edad)
            if(not UsuarioVotante.objects.filter(user_id=user_id).exists()):
                user = UsuarioVotante(user_id=user_id,location=location, edad=edad)
                listaObjetos.append(user)
            print(user_id)
            print(location)
            print(edad)
            print("-----------------")
            counter+=1
        i+=1
    UsuarioVotante.objects.bulk_create(listaObjetos)
    return counter
def extraer_bookrating_dataset():
    fil = open(path+"\\BX-Book-Ratings.csv")
    i=0
    counter=0
    listaObjetos = []
    for line in fil.readlines():
        if(i!=0):

            lsplit = line.split(";")
            user_id = int(lsplit[0].replace('"',''))
            isbn = lsplit[1].replace('"','').strip()
            bookRating = int(lsplit[2].replace('"',''))
            try:
                lur = LibroUsuarioRating(isbn=LibroVotado.objects.get(isbn=isbn), user_id=UsuarioVotante.objects.get(user_id=user_id), book_rating=bookRating)
                listaObjetos.append(lur)
                counter+=1
            except:
                #Habia isbn en este dataset que no estaban en el otro dataset
                print("isbn no existente en el dataset")
        i+=1
    LibroUsuarioRating.objects.bulk_create(listaObjetos)
    return counter
    
#funciones auxiliares
def formatear_fecha(fecha):
    meses = {"January": 1, "February":2, "March":3, "April":4,"May":5,"June":6, "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    dias = {"1st": 1, "2nd":2,"3rd":3,"21st":21,"22nd":22,"23rd":23}
    i=4
    while(i<32):
        if(i!=21 and i!=22 and i!=23):
            dias[str(i)+"th"]=i
        i+=1
    res = fecha.split(" ")

    mes = meses[res[0]]
    dia = dias[res[1]]
    year = int(res[2])
    date = datetime.datetime(year, mes, dia)
    return date