from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import *
from .forms import *

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
#--------------------------------------------------------------------------HOME
def home(request):
    return render(request, "Clientes/home.html")

#--------------------------------------------------------------------------PAGOS
class PagoList(LoginRequiredMixin, ListView):
    model = Pago

class PagoCreate(LoginRequiredMixin, CreateView):
    model = Pago
    fields = ['tarjetaCredito', 'tarjetaDebito', 'transferencia', 'efectivo']
    success_url = reverse_lazy('mediosPago')   

class PagoUpdate(LoginRequiredMixin, UpdateView):
    model = Pago
    fields = ['tarjetaCredito', 'tarjetaDebito', 'transferencia', 'efectivo']
    success_url = reverse_lazy('mediosPago')
    
class PagoDelete(LoginRequiredMixin, DeleteView):
    model = Pago
    success_url = reverse_lazy('mediosPago')

#--------------------------------------------------------------------------PRODUCTOS
@login_required
def buscar(request):
    return render(request, "Clientes/buscar.html")

@login_required
def buscar_productos(request):
    if request.GET["buscar"]:
        patron = request.GET["buscar"]
        productos = Producto.objects.filter(producto__icontains=patron)
        contexto = {"producto_list": productos }
        return render(request, "Clientes/producto_list.html", contexto)
    return HttpResponse("No se ingresaron patrones de busqueda")


class ProductoList(LoginRequiredMixin, ListView):
    model = Producto


class ProductoCreate(LoginRequiredMixin, CreateView):
    model = Producto
    fields = ['producto', 'cantidad', 'color', 'precio']
    success_url = reverse_lazy('productos')    


class ProductoUpdate(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = ['producto', 'cantidad', 'color', 'precio']
    success_url = reverse_lazy('productos')    


class ProductoDelete(LoginRequiredMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy('productos')

#--------------------------------------------------------------------------SUCURSAL
class SucursalList(LoginRequiredMixin, ListView):
    model = Sucursal


class SucursalCreate(LoginRequiredMixin, CreateView):
    model = Sucursal
    fields = ['direccion', 'numero', 'ciudad']
    success_url = reverse_lazy('sucursal')


class SucursalUpdate(LoginRequiredMixin, UpdateView):
    model = Sucursal
    fields = ['direccion', 'numero', 'ciudad']
    success_url = reverse_lazy('sucursal')


class SucursalDelete(LoginRequiredMixin, DeleteView):
    model = Sucursal
    success_url = reverse_lazy('sucursal')


#--------------------------------------------------------------------------Login, Registro  
def login_request(request):
    if request.method == "POST":
        usuario = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return render(request, "Clientes/home.html")
        else:
            return redirect(reverse_lazy('login'))
        
    miForm = AuthenticationForm()

    return render(request, "Clientes/login.html", {"form": miForm })


def register(request):
    if request.method == "POST":
        miForm = RegistroForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get("username")
            miForm.save()
            return redirect(reverse_lazy('home'))

    else:    
        miForm = RegistroForm()

    return render(request, "Clientes/registro.html", {"form": miForm })  