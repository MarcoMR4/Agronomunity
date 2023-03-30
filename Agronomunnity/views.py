from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, AddEmplooye, AddTransport, AddCuadrilla, AddHuerta, AddProductor, AddMiembroCuadrilla, ChangeCuadrilla
from django.contrib.auth import authenticate, logout, login
from django.template import RequestContext
from .models import Trabajador, User, Camion, Cuadrilla, Productor, Huerta, MiembroCuadrilla
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

@login_required
def index(request):
    return render(request, 'index.html')

def li(request):
    if request.method == 'GET':
        return render(request, "login.html",{
            "form": UserLoginForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "login.html",{
                "form": UserLoginForm,
                "error": "Usuario o contraseña incorrectos."
            })
        else:
            login(request, user)
            return redirect('index')

def lo(request):
    logout(request)
    return redirect('login')

@login_required
def workerRegister(request):
    if request.user.trabajador.rol == 'E_B':
        form = AddEmplooye()
        trabajadores = Trabajador.objects.all()
        if request.method == 'POST':
            try:
                usuario = User.objects.create(
                    username=request.POST['Nombre'],
                    last_name=request.POST['AP']+' '+request.POST['AM'],
                    password= make_password(request.POST['Telefono'])
                )
                trabajador = Trabajador.objects.create(
                    telefono=request.POST['Telefono'],
                    correoPersonal=request.POST['Correo'],
                    rol=request.POST['Tipo'],
                    Usuario_id=usuario.id
                )
                return render(request, "user_enc_bit/workerRegister.html", {
                    'form':form,
                    "mensaje": "Trabajador Registrado exitosamente",
                    'trabajadores': trabajadores
                })
            except Exception as e:
                return render(request, "user_enc_bit/workerRegister.html", {
                    'form':form,
                    "error": e,
                    'trabajadores': trabajadores
                })
        else:
            return render(request, "user_enc_bit/workerRegister.html", {'form':form, 'trabajadores': trabajadores})
    else: 
        return render(request, 'denied.html')
    
@login_required
def transportRegister(request):
    if request.user.trabajador.rol == 'E_B':
        form = AddTransport()
        camiones = Camion.objects.all()
        if request.method == 'POST':
            try:
                chofer=Trabajador.objects.get(Usuario_id=request.POST['ElegirChofer'])
                camion = Camion.objects.create(
                    placa=request.POST['Placa'],
                    modelo=request.POST['Modelo'],
                    capacidad='8',
                    estatus=request.POST['EstatusTransporte'],
                    idChofer=chofer
                )
                return render(request, 'user_enc_bit/transportRegister.html', {
                    'form':form,
                    "mensaje": "Camión Registrado exitosamente",
                    'camiones': camiones})
            except Exception as e:
                print(e)
                return render(request, 'user_enc_bit/transportRegister.html', {
                    'form':form,
                    "error": e,
                    'camiones': camiones})
        else:
            return render(request, 'user_enc_bit/transportRegister.html', {'form':form, 'camiones': camiones})
    else: 
        return render(request, 'denied.html')
    
def squadRegister(request):
    if request.user.trabajador.rol == 'E_B':
        form = AddCuadrilla()
        cuadrillas = Cuadrilla.objects.all()
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    c = Cuadrilla.objects.get(id=request.POST['Cuadrilla']) 
                    c.delete()
                    return render(request, 'user_enc_bit/squadRegister.html', {
                        'form':form,
                        "mensaje": "Cuadrilla Eliminada exitosamente",
                        'cuadrillas': cuadrillas})
                except Exception as e:
                    print(e)
                    return render(request, 'user_enc_bit/squadRegister.html', {
                        'form':form,
                        "error": "No se pudo borrar la cuadrilla, intentalo de nuevo",
                        'cuadrillas': cuadrillas})
            elif request.POST['Id']=='agregar':
                try:
                    gerente=Trabajador.objects.get(Usuario_id=request.POST['ElegirGerente'])
                    capataz=Trabajador.objects.get(Usuario_id=request.POST['ElegirCapataz'])
                    Cuadrilla.objects.create(
                        nombre=request.POST['Nombre'],
                        idCapatazCuadrilla=capataz,
                        idGerenteCuadrilla=gerente
                    )
                    return render(request, 'user_enc_bit/squadRegister.html', {
                        'form':form,
                        "mensaje": "Cuadrilla Registrada exitosamente",
                        'cuadrillas': cuadrillas})
                except Exception as e:
                    print(e)
                    return render(request, 'user_enc_bit/squadRegister.html', {
                        'form':form,
                        "error": 'No se pudo registrar la cuadrilla, intentalo de nuevo',
                        'cuadrillas': cuadrillas})
            elif request.POST['Id']=='modificar':
                try:
                    cuadrilla=request.POST['Cuadrilla']
                    request.session['cuadrilla'] = cuadrilla
                    url = reverse('sm')
                    return redirect(url)
                except Exception as e:
                    print(e)
                    return render(request, 'user_enc_bit/squadRegister.html', {
                        'form':form,
                        "error": "A ocurrido un error, intentalo de nuevo",
                        'cuadrillas': cuadrillas})
        else:
            return render(request, 'user_enc_bit/squadRegister.html', {'form':form, 'cuadrillas': cuadrillas})
    else: 
        return render(request, 'denied.html')

def squadModify(request):
    if request.user.trabajador.rol == 'E_B':
        c = request.session.get('cuadrilla')
        formc = ChangeCuadrilla(cuadrilla=c)
        formm = AddMiembroCuadrilla()
        miembros = MiembroCuadrilla.objects.filter(idCuadrilla_id=c)
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    m = MiembroCuadrilla.objects.get(id=request.POST['Miembro']) 
                    m.delete()
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formm':formm,
                        'formc':formc,
                        "mensaje": "Miembro eliminado exitosamente",
                        'miembros': miembros})
                except Exception as e:
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formm':formm,
                        'formc':formc,
                        "error": "No se pudo borrar al miembro, intentalo de nuevo",
                        'miembros': miembros})
            elif request.POST['Id']=='agregar':
                try:
                    MiembroCuadrilla.objects.create(
                        nombre=request.POST['Nombre'],
                        apellidoP=request.POST['AP'],
                        apellidoM=request.POST['AM'],
                        idCuadrilla_id=c
                    )
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formc':formc,
                        'formm':formm,
                        "mensaje": "Miembro Registrado exitosamente",
                        'miembros': miembros})
                except Exception as e:
                    print(e)
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formc':formc,
                        'formm':formm,
                        "error": "No se pudo agregar el miembro, intentalo de nuevo",
                        'miembros': miembros})
            elif request.POST['Id']=='modificar':
                try:
                    gerente=Trabajador.objects.get(Usuario_id=request.POST['ElegirGerente'])
                    capataz=Trabajador.objects.get(Usuario_id=request.POST['ElegirCapataz'])
                    cuadrilla = Cuadrilla.objects.get(id = c)
                    cuadrilla.nombre = request.POST['Nombre']
                    cuadrilla.idCapatazCuadrilla = capataz
                    cuadrilla.idGerenteCuadrilla = gerente
                    cuadrilla.save()
                    formc = ChangeCuadrilla(cuadrilla=c)
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formc':formc,
                        'formm':formm,
                        "mensaje": "Se modificacion los datos",
                        'miembros': miembros})
                except Exception as e:
                    print(e)
                    return render(request, 'user_enc_bit/squadModify.html', {
                        'formc':formc,
                        'formm':formm,
                        "error": "No se pudo modificar los datos, intentalo de nuevo",
                        'miembros': miembros})
        else:
            return render(request, 'user_enc_bit/squadModify.html', {
                'formc':formc,
                'formm':formm,
                'miembros': miembros})
    else: 
        return render(request, 'denied.html')

def producerRegister(request):
    if request.user.trabajador.rol == 'E_B':
        form = AddProductor()
        productores = Productor.objects.all()
        if request.method == 'POST':
            try:
                Productor.objects.create(
                    nombre=request.POST['Nombre'],
                    apellidoP=request.POST['AP'],
                    apellidoM=request.POST['AM'],
                    telefono=request.POST['Telefono']
                )
                return render(request, 'user_enc_bit/producerRegister.html', {
                    'form':form,
                    "mensaje": "Productor Registrado exitosamente",
                    'productores': productores})
            except Exception as e:
                print(e)
                return render(request, 'user_enc_bit/producerRegister.html', {
                    'form':form,
                    "error": e,
                    'productores': productores})
        else:
            return render(request, 'user_enc_bit/producerRegister.html', {'form':form, 'productores': productores})
    else: 
        return render(request, 'denied.html')
    
def orchardRegister(request):
    if request.user.trabajador.rol == 'E_B':
        form = AddHuerta()
        huertas = Huerta.objects.all()
        if request.method == 'POST':
            try:
                productor=Trabajador.objects.get(Usuario_id=request.POST['ElegirProductor'])
                Huerta.objects.create(
                    nombre=request.POST['nombre'],
                    ubicacion=request.POST['ubicacion'],
                    fruta=request.POST['fruta'],
                    estatus=request.POST['EstatusHuerta'],
                    idProductor=productor
                )
                return render(request, 'user_enc_bit/orchardRegister.html', {
                    'form':form,
                    "mensaje": "Huerta Registrada exitosamente",
                    'huertas': huertas})
            except Exception as e:
                print(e)
                return render(request, 'user_enc_bit/orchardRegister.html', {
                    'form':form,
                    "error": e,
                    'huertas': huertas})
        else:
            return render(request, 'user_enc_bit/orchardRegister.html', {'form':form, 'huertas': huertas})
    else: 
        return render(request, 'denied.html')