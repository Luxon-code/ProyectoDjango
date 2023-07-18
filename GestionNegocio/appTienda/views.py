from django.shortcuts import render,redirect
from appTienda.models import Categoria,Producto
from django.db import Error
import os
from rest_framework import generics
from appTienda.serializers import CategoriaSerializer,ProductoSerializer
# Create your views here.
def inicio(request):
    return render(request, 'listarProductos.html')
def vistaCategorias(request):
    categorias = Categoria.objects.all()
    retorno = {"listaCategorias": categorias}
    return render(request, 'frmAgregarCategoria.html',retorno)
def agregarCategoria(request):
    nombre = request.POST["txtNombre"]
    try: 
        categoria = Categoria(catNombre=nombre) 
        categoria.save()
        mensaje="Categoria agregada correctamente"
        categorias= Categoria.objects.all()
    except:
        mensaje="Problemas a la hora de agregar la categoría" 
    retorno = {"mensaje":mensaje,"listaCategorias":categorias}
    return render(request,"frmAgregarCategoria.html",retorno)
def listarProductos (request):
    try: 
        productos = Producto.objects.all() 
        mensaje="" 
        print (productos) 
    except:
        mensaje="Problemas al obtener los productos" 
    retorno = {"mensaje":mensaje, "listaProductos": productos} 
    return render(request,"listarProductos.html",retorno)
def vistaProducto(request):
    try:
        categorias = Categoria.objects.all()
        mensaje=""
    except:
        mensaje="Problemas al obtener las categorias"
    retorno = {"mensaje":mensaje, "listaCategorias": categorias, "producto": None} 
    return render(request, "frmAgregarProducto.html", retorno)
def agregarProducto(request):
    nombre = request.POST["txtNombre"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"]) 
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES["fileFoto"]
    try:
        #obtener la categoria de acuerdo a su id
        categoria = Categoria.objects.get(id=idCategoria)
        #crear el producto
        producto = Producto (proNombre = nombre, proCodigo=codigo,proPrecio=precio, proCategoria=categoria,
                             profoto = archivo)
        #registrarlo en la base de datos
        producto.save()
        mensaje="Producto Agregado Correctamente"
        return redirect("/inicio/")
    except Error as error:
        mensaje=f"Problemas al realizar el proceso de agregar un producto. {error}"
    #obtener las categorias
    categorias = Categoria.objects.all()
    retorno = {"mensaje" :mensaje, "listaCategorias": categorias, "producto": producto}
    return render(request, "frmAgregarProducto.html", retorno)
def consultarProducto (request, id): 
    try:
        producto = Producto.objects.get(id=id) 
        categorias = Categoria.objects.all()
        mensaje=""
    except Error as error: 
        mensaje=f"Problemas {error}"
    retorno = {"mensaje": mensaje, "producto":producto, "listaCategorias": categorias} 
    return render(request, "frmEditarProducto.html", retorno)
def actualizarProducto (request):
    idProducto = int(request.POST["idProducto"])
    nombre = request.POST["txtNombre"]
    codigo = int(request.POST["txtCodigo"])
    precio = int(request.POST["txtPrecio"])
    idCategoria = int(request.POST["cbCategoria"])
    archivo = request.FILES.get("fileFoto", False)
    try:
        #obtener la categoria de acuerdo a su id 
        categoria = Categoria.objects.get(id=idCategoria)
        #actualizar el producto. PRIMERO SE CONSULTA
        producto = Producto.objects.get(id=idProducto)
        producto.proNombre=nombre
        producto.proPrecio=precio
        producto.procategoria=categoria
        producto.proCodigo=codigo
        if(archivo):
            os.remove('./media/'+str(producto.profoto))
            producto.profoto=archivo
        producto.save()
        mensaje="Producto actualizado correctamente"
        return redirect("/inicio/")
    except Error as error:
        mensaje= f"Problemas al realizar el proceso de actualizar el producto {error}"
    categorias = Categoria.objects.all()
    retorno = {"mensaje":mensaje, "listaCategorias": categorias, "producto":producto} 
    return render(request, "frmEditarProducto.html", retorno)
def eliminarProducto(request,id):
    try: 
        producto = Producto.objects.get(id=id)
        producto.delete()
        os.remove('./media/'+str(producto.profoto))
        mensaje="Producto Eliminado"
    except Error as error:
        mensaje=f"Problemas al eliminar el producto {error}"
    retorno = {"mensaje":mensaje} 
    return redirect("/inicio/",retorno)

class CategoriaList(generics.ListCreateAPIView):
    queryset=Categoria.objects.all()
    serializer_class=CategoriaSerializer
    
class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Categoria.objects.all()
    serializer_class=CategoriaSerializer
    
class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Producto.objects.all()
    serializer_class = ProductoSerializer