from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, NUMERIC, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh import qparser
from whoosh.query import *
from .models import Libro, TodosTusLibros, PlanetaLibros, LibroVotado

import re, os, shutil

def indexar_datos_libros():
    #isbn como texto debido a que supera el rango de whoosh
    esquema= Schema(id=NUMERIC(stored=True), isbn=TEXT, titulo=TEXT, autor=TEXT,genero=ID,descripcion=TEXT,rating=NUMERIC(numtype=float),fechapublicacion=DATETIME)
    if os.path.exists("IndexLibro"):
        shutil.rmtree("IndexLibro")
    os.mkdir("IndexLibro")
    ix = create_in("IndexLibro", schema=esquema)
    writer = ix.writer()
    it=0
    for libro in Libro.objects.all():
        #ponemos a genero así para aquellos que tengan más de dos palabras.
        writer.add_document(id=libro.pk, isbn = str(libro.isbn), autor=libro.autor, genero=libro.genero.nombre.replace(" ",""), descripcion=libro.descripcionHTML, rating=libro.rating,fechapublicacion=libro.fechapublicacion)
        it+=1
    writer.commit()
    return it

def indexar_datos_ttl():
    #isbn como texto debido a que supera el rango de whoosh
    esquema= Schema(id=NUMERIC(stored=True), isbn=TEXT, titulo=TEXT, autor=TEXT,genero=KEYWORD(commas=True),descripcion=TEXT,fechapublicacion=DATETIME, precio=NUMERIC(numtype=float))
    if os.path.exists("IndexTtl"):
        shutil.rmtree("IndexTtl")
    os.mkdir("IndexTtl")
    ix = create_in("IndexTtl", schema=esquema)
    writer = ix.writer()
    it=0
    for libro in TodosTusLibros.objects.all():
        writer.add_document(id=libro.pk, isbn = str(libro.isbn), autor=libro.autor, genero=libro.categorias.replace(" ",""), descripcion=libro.descripcion, fechapublicacion=libro.fechapublicacion, precio= float(libro.precio.replace("€","")))
        it+=1
    writer.commit()
    return it
def indexar_buscador_general():
    #isbn como texto debido a que supera el rango de whoosh
    #ID guardado como texto debido a que  los ids del dataset son los isbn
    esquema= Schema(id=TEXT(stored=True), procedencia=ID, titulo=TEXT, isbn=TEXT)
    if os.path.exists("IndexGeneral"):
        shutil.rmtree("IndexGeneral")
    os.mkdir("IndexGeneral")
    ix = create_in("IndexGeneral", schema=esquema)
    writer = ix.writer()
    it=0
    for libro in TodosTusLibros.objects.all():
        writer.add_document(id=str(libro.pk), procedencia = "ttl", titulo=libro.titulo, isbn=str(libro.isbn))
        it+=1
    for libro in Libro.objects.all():
        writer.add_document(id=str(libro.pk), procedencia = "gr", titulo=libro.titulo, isbn=str(libro.isbn))
        it+=1
    for libro in PlanetaLibros.objects.all():
        writer.add_document(id=str(libro.pk), procedencia = "pl", titulo=libro.titulo, isbn=str(libro.isbn))
        it+=1
    for libro in LibroVotado.objects.all():
        writer.add_document(id=str(libro.isbn), procedencia = "dtst", titulo=libro.titulo, isbn=str(libro.isbn))
        it+=1
        
    writer.commit()
    return it

def buscartituloOisbn(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        entradas  = str(entrada).split(" ")
        terminos = []
        for entrada in entradas:
            terminos.append(Term("titulo", entrada.lower()))
            terminos.append(Term("isbn", entrada.lower()))
        querydtst = And([Term("procedencia", "dtst"), Or(terminos)])
        queryttl = And([Term("procedencia", "ttl"), Or(terminos)])
        querygr = And([Term("procedencia", "gr"), Or(terminos)])
        querypl = And([Term("procedencia", "pl"), Or(terminos)])
        res = buscador.search(querydtst, limit=40)
        for r in res:
            listaPks.append([r["id"], "dtst"])
        res = buscador.search(queryttl, limit=20)
        for r in res:
            listaPks.append([r["id"], "ttl"])
        res = buscador.search(querygr, limit=20)
        for r in res:
            listaPks.append([r["id"], "gr"])
        res = buscador.search(querypl, limit=20)
        for r in res:
            listaPks.append([r["id"], "pl"])    

    return listaPks
def buscartituloOdescripcion(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        query = MultifieldParser(["titulo","descripcion"],indx.schema, group=OrGroup).parse(str(entrada))
        res = buscador.search(query)
        for r in res:
            listaPks.append(r["id"])
    return listaPks

def buscarAutor(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        query = QueryParser("autor", indx.schema).parse(str(entrada))
        res = buscador.search(query)
        print(res)
        for r in res:
            listaPks.append(r["id"])
    return listaPks

def buscarISBN(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        query = QueryParser("isbn", indx.schema).parse(str(entrada))
        res = buscador.search(query)
        for r in res:
            listaPks.append(r["id"])
    return listaPks
def buscarRating(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        query = NumericRange("rating", float(entrada), 20.0)
        res = buscador.search(query)
        for r in res:
            listaPks.append(r["id"])
    return listaPks

def buscarFechas(entrada1, entrada2, index):
    listaPks = []
    fecha1=formateafecha(entrada1)
    fecha2=formateafecha(entrada2)
    indx=open_dir(index)
    with indx.searcher() as buscador:
        rango_fecha = '['+ fecha1 + ' TO ' + fecha2 +']'
        query = QueryParser("fechapublicacion", indx.schema).parse(rango_fecha)
        res = buscador.search(query)
        for r in res:
            listaPks.append(r["id"])
    return listaPks

def buscarGenero(entrada, index):
    listaPks = []
    indx=open_dir(index)
    print(entrada)
    with indx.searcher() as buscador:
        query = QueryParser("genero", indx.schema).parse(str(entrada).replace(" ", ""))
        res = buscador.search(query)
        print(res)
        for r in res:
            listaPks.append(r["id"])
    return listaPks
def buscarPrecio(entrada, index):
    listaPks = []
    indx=open_dir(index)
    with indx.searcher() as buscador:
        query = NumericRange("precio", 0.0, float(entrada))
        #limitamos a 20 porque es posible que quieran buscar más y tampoco se puede afinar más
        res = buscador.search(query, limit=20)
        for r in res:
            listaPks.append(r["id"])
    return listaPks
def formateafecha(entrada):
    res = entrada.split("/")
    return str(res[2])+str(res[1])+str(res[0])

