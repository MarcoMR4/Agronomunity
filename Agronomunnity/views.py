from django.urls import reverse
from django.shortcuts import redirect, render
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, AddWorker, AddProducer, AddTransport, AddSquad, AddOrchard, AddSquadMember, AddOrder, AddClient, AddCaliber, AddQuality, AddTrip
from django.contrib.auth import authenticate, logout, login
from .models import Trabajador, RolTrabajador, User, CamionTransporte, Cuadrilla, Productor, Huerta, MiembroCuadrilla, Cliente, Pedido, Calibre, Calidad, PedidoCalibreCalidad, OrdenCorte, ViajeCorte, ReporteCorte
from django.contrib.auth.hashers import make_password

#dashboard 
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

#Encargado de bitacora
#Trabajador
@login_required
def worker(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        #Consultas necesarias para mostrar en plantilla
        form = AddWorker()
        trabajadores = Trabajador.objects.all()
        ntrabajadores = Trabajador.objects.count()
        roles = RolTrabajador.objects.all().order_by('nombreRol')
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Trabajador'] = request.POST['Trabajador']
                    url = reverse('wd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('w')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombres'] = request.POST['Nombre']
                    request.session['Apellidos'] = request.POST['AP']+' '+request.POST['AM']
                    request.session['Telefono'] = request.POST['Telefono']
                    request.session['Correo'] = request.POST['Correo']
                    request.session['Rol'] = request.POST['Rol']
                    url = reverse('wr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('w')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Trabajador'] = request.POST['Trabajador']
                    request.session['Nusuario'] = request.POST['Nusuario']
                    request.session['Nombres'] = request.POST['Nombre']
                    request.session['Apellidos'] = request.POST['Apellidos']
                    request.session['Telefono'] = request.POST['Telefono']
                    request.session['Correo'] = request.POST['Correo']
                    request.session['Rol'] = request.POST['Rol']
                    url = reverse('wm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('w')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, "user_enc_bit/worker.html", {
                    'form':form,
                    'trabajadores': trabajadores,
                    'ntrabajadores': ntrabajadores,
                    'roles' : roles,
                    "mensaje": request.session['Mensaje']
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, "user_enc_bit/worker.html", {
                    'form':form,
                    'trabajadores': trabajadores,
                    'ntrabajadores': ntrabajadores,
                    'roles' : roles,
                    "error": request.session['Error']
                })
            else:
                return render(request, "user_enc_bit/worker.html", {
                    'form':form,
                    'trabajadores': trabajadores,
                    'ntrabajadores': ntrabajadores,
                    'roles' : roles
                })
    else: 
        return render(request, 'denied.html')

@login_required
def workerDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:
            #Se obtiene el trabajador y elimina
            trabajador = request.session.get('Trabajador')
            t = Trabajador.objects.get(id=trabajador)
            u = User.objects.get(id = t.usuario.id)
            u.delete() 
            t.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Trabajador eliminado correctamente."
        except Exception as e:

            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('w')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def workerRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:
            nombres=request.session.get('Nombres')
            apellidos=request.session.get('Apellidos')
            palabras = nombres.split() + apellidos.split()
            iniciales = []
            for palabra in palabras:
                iniciales.append(palabra[0].upper())
            nusuario = ''.join(iniciales)
            usuario = User.objects.create(
                username='Agro-'+nusuario,
                first_name=request.session.get('Nombres'),
                last_name=request.session.get('Apellidos'),
                password= make_password(request.session.get('Telefono')),
                email = request.session.get('Correo')
            )

            r = RolTrabajador.objects.get(nombreRol=request.session.get('Rol'))
            Trabajador.objects.create(
                telefono=request.session.get('Telefono'),
                rol=r,
                usuario=usuario
            )
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Trabajador registrado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('w')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def workerModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:
            #Se obtienen los datos y se modifican
            trabajador = Trabajador.objects.get(id=request.session.get('Trabajador'))
            usuario = User.objects.get(id=trabajador.usuario.id)
            rol = RolTrabajador.objects.get(nombreRol=request.session.get('Rol'))
            usuario.username=request.session.get('Nusuario')
            usuario.first_name =request.session.get('Nombres')
            usuario.last_name=request.session.get('Apellidos')
            usuario.email=request.session.get('Correo')
            usuario.save()
            trabajador.telefono=request.session.get('Telefono')
            trabajador.rol=rol
            trabajador.save()

            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('w')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

#Productor
@login_required
def producer(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        #Consultas necesarias para mostrar en plantilla
        form = AddProducer()
        productores = Productor.objects.all()
        nproductores = Productor.objects.count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Productor'] = request.POST['Productor']
                    url = reverse('pd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('p')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['Telefono'] = request.POST['Telefono']
                    url = reverse('pr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('p')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Productor'] = request.POST['Productor']
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['Telefono'] = request.POST['Telefono']
                    url = reverse('pm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('p')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/producer.html', {
                    'form':form,
                    "mensaje": request.session['Mensaje'],
                    'productores': productores,
                    'nproductores': nproductores
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/producer.html', {
                    'form':form,
                    "error": request.session['Error'],
                    'productores': productores,
                    'nproductores': nproductores
                })
            else:
                return render(request, "user_enc_bit/producer.html", {
                    'form':form,
                    'productores': productores,
                    'nproductores': nproductores
                })
    else: 
        return render(request, 'denied.html')

@login_required
def producerRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:

            Productor.objects.create(
                nombre=request.session.get('Nombre'),
                apellidoP=request.session.get('AP'),
                apellidoM=request.session.get('AM'),
                telefono=request.session.get('Telefono'),
            )

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Productor registrado correctamente."

        except Exception as e:
            
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."

        url = reverse('p')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def producerDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:
            #Se obtiene el trabajador y elimina
            productor = request.session.get('Productor')
            p = Productor.objects.get(id=productor)
            p.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Productor eliminado correctamente."
        except Exception as e:

            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('p')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def producerModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_B':
        try:
            #Se obtienen los datos y se modifican
            productor = Productor.objects.get(id=request.session.get('Productor'))
            productor.nombre=request.session.get('Nombre')
            productor.apellidoP=request.session.get('AP')
            productor.apellidoM=request.session.get('AM')
            productor.telefono=request.session.get('Telefono')
            productor.save()

            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            print(e)

            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('p')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

#Cuadrillas
@login_required
def squad(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        form = AddSquad()
        cuadrillas = Cuadrilla.objects.all()
        ncuadrillas = Cuadrilla.objects.all().count()
        numJefGer = Trabajador.objects.filter(Q(rol__nomenclaturaRol__exact='G_C') | Q(rol__nomenclaturaRol__exact='J_C')).count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Cuadrilla'] = request.POST['Cuadrilla']
                    url = reverse('sd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('s')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['Gerente'] = request.POST['Gerente']
                    request.session['Jefe'] = request.POST['Jefe']
                    request.session['Ubicacion'] = request.POST['Ubicacion']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('sr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('s')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Cuadrilla'] = request.POST['Cuadrilla']
                    url = reverse('sm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('s')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/squad.html', {
                    'form':form,
                    'numJefGer':numJefGer,
                    'ncuadrillas':ncuadrillas,
                    "mensaje": request.session['Mensaje'],
                    'cuadrillas': cuadrillas
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/squad.html', {
                    'form':form,
                    'numJefGer':numJefGer,
                    'ncuadrillas':ncuadrillas,
                    "error": request.session['Error'],
                    'cuadrillas': cuadrillas
                })
            else:
                return render(request, 'user_enc_bit/squad.html', {
                    'form':form,
                    'numJefGer':numJefGer,
                    'ncuadrillas':ncuadrillas,
                    'cuadrillas': cuadrillas
                })
    else: 
        return render(request, 'denied.html')

@login_required
def squadDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            #Se obtiene la cuadrilla y elimina
            cuadrilla = request.session.get('Cuadrilla')
            c = Cuadrilla.objects.get(id=cuadrilla)
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Cuadrilla eliminada correctamente."
        except Exception as e:

            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('s')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def squadRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            #Se obtienen los datos y se crea la cuadrilla
            print(request.session.get('Gerente'))
            gerente=Trabajador.objects.get(id=request.session.get('Gerente'))
            jefe=Trabajador.objects.get(id=request.session.get('Jefe'))
            Cuadrilla.objects.create(
                nombreCuadrilla=request.session.get('Nombre'),
                ubicacionCuadrilla=request.session.get('Ubicacion'),
                estatusCuadrilla=request.session.get('Estatus'),
                idJefeCuadrilla= jefe,
                idGerenteCuadrilla=gerente
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Cuadrilla registrada correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('s')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def squadModify(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        cuadrilla = Cuadrilla.objects.get(id=request.session.get('Cuadrilla'))
        formm = AddSquadMember()
        miembros = MiembroCuadrilla.objects.filter(idCuadrilla=cuadrilla.id)
        trabajadores = Trabajador.objects.filter(Q(rol__nomenclaturaRol__exact='G_C') | Q(rol__nomenclaturaRol__exact='J_C'))
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Miembro'] = request.POST['Miembro']
                    url = reverse('smd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('sm')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['noImss'] = request.POST['noImss']
                    url = reverse('smr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('sm')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['Ubicacion'] = request.POST['Ubicacion']
                    request.session['Estatus'] = request.POST['Estatus']
                    request.session['Gerente'] = request.POST['Gerente']
                    request.session['Jefe'] = request.POST['Jefe']
                    url = reverse('sms')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('sm')
                    return redirect(url)
            elif request.POST['Id']=='editar':
                try:
                    request.session['Miembro'] = request.POST['Miembro']
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['noImss'] = request.POST['noImss']
                    url = reverse('smm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo guardar los datos, intente de nuevo."
                    url = reverse('sm')
                    return redirect(url)
        else:

            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/squadModify.html', {
                    'formm':formm,
                    'cuadrilla':cuadrilla,
                    "mensaje": request.session['Mensaje'],
                    'trabajadores' : trabajadores,
                    'miembros': miembros
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/squadModify.html', {
                    'formm':formm,
                    'cuadrilla':cuadrilla,
                    "error": request.session['Error'],
                    'trabajadores' : trabajadores,
                    'miembros': miembros
                })
            else:
                return render(request, 'user_enc_bit/squadModify.html', {
                    'formm':formm,
                    'cuadrilla':cuadrilla,
                    'trabajadores' : trabajadores,
                    'miembros': miembros
                })
    else: 
        return render(request, 'denied.html')

@login_required
def squadMemberSave(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            #Se obtienen los datos y se modifican
            gerente=Trabajador.objects.get(id=request.session.get('Gerente'))
            jefe=Trabajador.objects.get(id=request.session.get('Jefe'))

            cuadrilla = Cuadrilla.objects.get(id=request.session.get('Cuadrilla'))
            cuadrilla.nombreCuadrilla=request.session.get('Nombre')
            cuadrilla.estatusCuadrilla=request.session.get('Estatus')
            cuadrilla.ubicacionCuadrilla=request.session.get('Ubicacion')
            cuadrilla.idJefeCuadrilla=jefe
            cuadrilla.idGerenteCuadrilla=gerente
            cuadrilla.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron los datos correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('sm')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def squadMemberDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            #Se obtiene el miembro y elimina
            miembro = request.session.get('Miembro')
            m = MiembroCuadrilla.objects.get(id=miembro)
            m.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Miembro eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('sm')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def squadMemberModify(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            #Se obtienen los datos y se modifican
            miembro = MiembroCuadrilla.objects.get(id=request.session.get('Miembro'))
            miembro.nombre=request.session.get('Nombre')
            miembro.apellidoP=request.session.get('AP')
            miembro.apellidoM=request.session.get('AM')
            miembro.noImss = request.session.get('noImss')
            miembro.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('sm')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def squadMemberRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'G_C'):
        try:
            cuadrilla = Cuadrilla.objects.get(id=request.session.get('Cuadrilla'))
            #Se obtienen los datos y se crea el miembro
            MiembroCuadrilla.objects.create(
                nombre=request.session.get('Nombre'),
                apellidoP=request.session.get('AP'),
                apellidoM=request.session.get('AM'),
                noImss = request.session.get('noImss'),
                idCuadrilla=cuadrilla
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Miembro registrado correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('sm')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

#Encargado de transporte
@login_required
def transport(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_T':
        form = AddTransport()
        camiones = CamionTransporte.objects.all()
        ncamiones = camiones.count()
        choferes = Trabajador.objects.filter(rol__nomenclaturaRol__exact='C_T')
        nchoferes = choferes.count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Camion'] = request.POST['Camion']
                    url = reverse('td')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('t')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Chofer'] = request.POST['Chofer']
                    request.session['Placa'] = request.POST['Placa']
                    request.session['Modelo'] = request.POST['Modelo']
                    request.session['Capacidad'] = request.POST['Capacidad']
                    request.session['Tipo'] = request.POST['Tipo']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    request.session['Candado'] = request.POST['Candado']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('tr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('t')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Camion'] = request.POST['Camion']
                    request.session['Chofer'] = request.POST['Chofer']
                    request.session['Placa'] = request.POST['Placa']
                    request.session['Modelo'] = request.POST['Modelo']
                    request.session['Capacidad'] = request.POST['Capacidad']
                    request.session['Tipo'] = request.POST['Tipo']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    request.session['Candado'] = request.POST['Candado']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('tm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('t')
                    return redirect(url)
        else:

            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_trans/transport.html', {
                    'form':form,
                    "mensaje": request.session['Mensaje'],
                    'choferes': choferes,
                    'camiones': camiones,
                    'nchoferes': nchoferes,
                    'ncamiones': ncamiones
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_trans/transport.html', {
                    'form':form,
                    "error": request.session['Error'],
                    'choferes': choferes,
                    'camiones': camiones,
                    'nchoferes': nchoferes,
                    'ncamiones': ncamiones
                })
            else:
                return render(request, 'user_enc_trans/transport.html', {
                    'form':form,
                    'choferes': choferes,
                    'camiones': camiones,
                    'nchoferes': nchoferes,
                    'ncamiones': ncamiones
                })
    else: 
        return render(request, 'denied.html')

@login_required
def transportDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_T':
        try:
            #Se obtiene el miembro y elimina
            camion = request.session.get('Camion')
            c = CamionTransporte.objects.get(id=camion)
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Vehiculo eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('t')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def transportRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_T':
        try:
            chofer = Trabajador.objects.get(id=request.session.get('Chofer'))
            #Se obtienen los datos y se crea el miembro
            CamionTransporte.objects.create(
                capacidadTransporte=request.session.get('Capacidad'),
                placaTransporte=request.session.get('Placa'),
                tipoTransporte=request.session.get('Tipo'),
                descripcionTransporte=request.session.get('Descripcion'),
                modeloTransporte=request.session.get('Modelo'),
                candadoTransporte=request.session.get('Candado'),
                estatusTransporte=request.session.get('Estatus'),
                idChoferTransporte=chofer
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Vehiculo registrado correctamente."
        except Exception as e:

            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('t')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def transportModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_T':
        try:
            #Se obtienen los datos y se modifican
            chofer = Trabajador.objects.get(id=request.session.get('Chofer'))
            camion = CamionTransporte.objects.get(id=request.session.get('Camion'))
            camion.idChoferTransporte=chofer
            camion.placaTransporte =request.session.get('Placa')
            camion.modeloTransporte =request.session.get('Modelo')
            camion.tipoTransporte =request.session.get('Tipo')
            camion.descripcionTransporte =request.session.get('Descripcion')
            camion.candadoTransporte =request.session.get('Candado')
            camion.capacidadTransporte =request.session.get('Capacidad')
            camion.estatusTransporte = request.session.get('Estatus')
            camion.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('t')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

def orchard(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T', 'I_C'):
        form = AddOrchard()
        huertas = Huerta.objects.all()
        nhuertas = Huerta.objects.all().count()
        productores = Productor.objects.all().order_by('apellidoP')
        nproductores = Productor.objects.all().count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Huerta'] = request.POST['Huerta']
                    url = reverse('od')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('o')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['Fruta'] = request.POST['Fruta']
                    request.session['Ubicacion'] = request.POST['Ubicacion']
                    request.session['Localizacion'] = request.POST['Localizacion']
                    request.session['Clave'] = request.POST['Clave']
                    request.session['Inocuidad'] = request.POST['Inocuidad']
                    request.session['Productor'] = request.POST['Productor']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('or')
                    return redirect(url)
                except Exception as e:
                    print(e)
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('o')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Huerta'] = request.POST['Huerta']
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['Fruta'] = request.POST['Fruta']
                    request.session['Ubicacion'] = request.POST['Ubicacion']
                    request.session['Localizacion'] = request.POST['Localizacion']
                    request.session['Clave'] = request.POST['Clave']
                    request.session['Inocuidad'] = request.POST['Inocuidad']
                    request.session['Productor'] = request.POST['Productor']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('om')
                    return redirect(url)
                except Exception as e:
                    print(e)
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('o')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/orchard.html', {
                    'form':form,
                    "mensaje": request.session['Mensaje'],
                    'huertas': huertas,
                    'nhuertas': nhuertas,
                    'nproductores': nproductores,
                    'productores': productores
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/orchard.html', {
                    'form':form,
                    "error": request.session['Error'],
                    'huertas': huertas,
                    'nhuertas': nhuertas,
                    'nproductores': nproductores,
                    'productores': productores
                })
            else:
                return render(request, 'user_enc_bit/orchard.html', {
                    'form':form,
                    'huertas': huertas,
                    'nhuertas': nhuertas,
                    'nproductores': nproductores,
                    'productores': productores
                })
    else: 
        return render(request, 'denied.html')

@login_required
def orchardDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T', 'I_C'):
        try:
            #Se obtiene el miembro y elimina
            huerta = request.session.get('Huerta')
            h = Huerta.objects.get(id=huerta)
            h.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Huerta eliminada correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('o')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def orchardRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T', 'I_C'):
        try:
            #Se obtienen los datos y se crea el miembro
            productor = Productor.objects.get(nombre=request.session.get('Productor'))
            print(productor)
            Huerta.objects.create(
                nombreHuerta=request.session.get('Nombre'),
                frutaHuerta=request.session.get('Fruta'),
                ubicacionHuerta=request.session.get('Ubicacion'),
                localizacionHuerta=request.session.get('Localizacion'),
                claveSagarpaHuerta=request.session.get('Clave'),
                estatusInocuidadHuerta=request.session.get('Inocuidad'),
                estatusHuerta=request.session.get('Estatus'),
                idProductor=productor
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Vehiculo registrado correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('o')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def orchardModify(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T', 'I_C'):
        try:
            #Se obtienen los datos y se modifican
            productor=Productor.objects.get(id=request.session.get('Productor'))

            huerta = Huerta.objects.get(id=request.session.get('Huerta'))
            huerta.nombreHuerta=request.session.get('Nombre')
            huerta.frutaHuerta=request.session.get('Fruta')
            huerta.ubicacionHuerta=request.session.get('Ubicacion')
            huerta.localizacionHuerta=request.session.get('Localizacion')
            huerta.claveSagarpaHuerta=request.session.get('Clave')
            huerta.estatusInocuidadHuerta=request.session.get('Inocuidad')
            huerta.estatusHuerta=request.session.get('Estatus')
            huerta.idProductor=productor
            huerta.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('o')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

def trip(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T'):
        form = AddTrip()
        viajes = ViajeCorte.objects.all()
        nviajes = ViajeCorte.objects.all().count()
        camiones = CamionTransporte.objects.all().order_by('placaTransporte')
        ordenes = OrdenCorte.objects.filter(estatusOrden='O_P')
        cuadrillas = Cuadrilla.objects.all()
        elementos = True
        if camiones.count()==0 or ordenes.count()==0 or cuadrillas.count()==0:
            elementos = False

        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Viaje'] = request.POST['Viaje']
                    url = reverse('ctd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('ct')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Fecha'] = request.POST['Nombre']
                    request.session['Camion1'] = request.POST['Camion1']
                    request.session['Camion2'] = request.POST['Camion2']
                    request.session['Salida'] = request.POST['Salida']
                    request.session['Llegada'] = request.POST['Llegada']
                    request.session['Orden'] = request.POST['Orden']
                    request.session['Cuadrilla'] = request.POST['Cuadrilla']
                    request.session['Punto'] = request.POST['Punto']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('ctr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('ct')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Viaje'] = request.POST['Viaje']
                    request.session['Fecha'] = request.POST['Nombre']
                    request.session['Camion1'] = request.POST['Camion1']
                    request.session['Camion2'] = request.POST['Camion2']
                    request.session['Salida'] = request.POST['Salida']
                    request.session['Llegada'] = request.POST['Llegada']
                    request.session['Orden'] = request.POST['Orden']
                    request.session['Cuadrilla'] = request.POST['Cuadrilla']
                    request.session['Punto'] = request.POST['Punto']
                    request.session['Estatus'] = request.POST['Estatus']
                    url = reverse('ctm')
                    return redirect(url)
                except Exception as e:
                    print(e)
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('ct')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/trip.html', {
                    'form':form,
                    "mensaje": request.session['Mensaje'],
                    'nviajes': nviajes,
                    'viajes': viajes,
                    'camiones': camiones,
                    'ordenes': ordenes,
                    'cuadrillas': cuadrillas,
                    'elementos': elementos
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_bit/trip.html', {
                    'form':form,
                    "error": request.session['Error'],
                    'nviajes': nviajes,
                    'viajes': viajes,
                    'camiones': camiones,
                    'ordenes': ordenes,
                    'cuadrillas': cuadrillas,
                    'elementos': elementos
                })
            else:
                return render(request, 'user_enc_bit/trip.html', {
                    'form':form,
                    'nviajes': nviajes,
                    'viajes': viajes,
                    'camiones': camiones,
                    'ordenes': ordenes,
                    'cuadrillas': cuadrillas,
                    'elementos': elementos
                })
    else: 
        return render(request, 'denied.html')

@login_required
def tripDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T'):
        try:
            #Se obtiene el miembro y elimina
            v = ViajeCorte.objects.get(id=request.session.get('Viaje'))
            v.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Viaje eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('ct')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def tripRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T'):
        try:
            #Se obtienen los datos y se crea el miembro
            camion1 = CamionTransporte.objects.get(id=request.session.get('Camion1'))
            camion2 = CamionTransporte.objects.get(id=request.session.get('Camion2'))
            orden = OrdenCorte.objects.get(id=request.session.get('Orden'))
            cuadrilla = OrdenCorte.objects.get(id=request.session.get('Cuadrilla'))
            CamionTransporte.objects.create(
                fechaViaje=request.session.get('Fecha'),
                idCamionTransporte=camion1,
                idCamionSecundarioTransporte=camion2,
                horaSalida=request.session.get('Salida'),
                horaLlegada=request.session.get('Llegada'),
                idOrdenCorte=orden,
                idCuadrilla=cuadrilla,
                puntoReunion=request.session.get('Punto'),
                estatusViaje=request.session.get('Estatus')
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Viaje registrado correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('ct')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def tripModify(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'E_T'):
        try:
            #Se obtienen los datos y se modifican
            camion1 = CamionTransporte.objects.get(id=request.session.get('Camion1'))
            camion2 = CamionTransporte.objects.get(id=request.session.get('Camion2'))
            orden = OrdenCorte.objects.get(id=request.session.get('Orden'))
            cuadrilla = OrdenCorte.objects.get(id=request.session.get('Cuadrilla'))

            viaje = ViajeCorte.objects.get(id=request.session.get('Viaje'))
            viaje.fechaViaje=request.session.get('Fecha')
            viaje.idCamionTransporte=camion1
            viaje.idCamionSecundarioTransporte=camion2
            viaje.horaSalida=request.session.get('Salida')
            viaje.horaLlegada=request.session.get('Llegada')
            viaje.idOrdenCorte = orden
            viaje.idCuadrilla = cuadrilla
            viaje.puntoReunion=request.session.get('Punto')
            viaje.estatusViaje=request.session.get('Estatus')
            viaje.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('ct')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def order(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        form = AddOrder()
        pedidos = Pedido.objects.all()
        npedidos = pedidos.count()
        nclientes = Cliente.objects.all().count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Pedido'] = request.POST['Pedido']
                    url = reverse('sod')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('so')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Numero'] = request.POST['Numero']
                    request.session['Kilos'] = request.POST['Kilos']
                    request.session['Mercado'] = request.POST['Mercado']
                    request.session['Destino'] = request.POST['Destino']
                    request.session['Cliente'] = request.POST['Cliente']
                    url = reverse('sor')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('so')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Pedido'] = request.POST['Pedido']
                    request.session['Kilos'] = request.POST['Kilos']
                    request.session['Mercado'] = request.POST['Mercado']
                    request.session['Destino'] = request.POST['Destino']
                    url = reverse('som')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('so')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/order.html', {
                    "mensaje": request.session['Mensaje'],
                    'form':form,
                    'pedidos': pedidos,
                    'npedidos': npedidos,
                    'nclientes': nclientes
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/order.html', {
                    "error": request.session['Error'],
                    'form':form,
                    'pedidos': pedidos,
                    'npedidos': npedidos,
                    'nclientes': nclientes
                })
            else:
                return render(request, 'user_enc_ventas/order.html', {
                    'form':form,
                    'pedidos': pedidos,
                    'npedidos': npedidos,
                    'nclientes': nclientes
                })
    else: 
        return render(request, 'denied.html')

@login_required
def orderDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtiene el miembro y elimina
            p = Pedido.objects.get(id=request.session.get('Pedido'))
            p.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Pedido eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('so')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def orderRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se crea el miembro
            cliente = Cliente.objects.get(id=request.session.get('Cliente'))
            kilos = float(request.session.get('Kilos'))
            pallets = int(kilos // 1000)
            Pedido.objects.create(
                idTrabajador=request.user.trabajador,
                idCliente = cliente,
                numeroPedido=request.session.get('Numero'),
                fechaPedido= date.today(),
                totalKilosPedido=kilos,
                totalPalletsPedido = pallets, 
                mercadoPedido=request.session.get('Mercado'),
                destinoPedido=request.session.get('Destino'),
                estatusPedido='P_P'
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Pedido registrado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('so')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def orderModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se modifican
            kilos = float(request.session.get('Kilos'))
            pallets = int(kilos // 1000)

            pedido = Pedido.objects.get(id=request.session.get('Pedido'))
            pedido.mercadoPedido = request.session.get('Mercado')
            pedido.destinoPedido = request.session.get('Destino')
            pedido.totalKilosPedido = kilos
            pedido.totalPalletsPedido = pallets
            pedido.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('so')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def client(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        form = AddClient()
        clientes = Cliente.objects.all()
        nclientes = clientes.count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminar':
                try:
                    request.session['Cliente'] = request.POST['Cliente']
                    url = reverse('cd')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('c')
                    return redirect(url)
            elif request.POST['Id']=='agregar':
                try:
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['RFC'] = request.POST['RFC']
                    url = reverse('cr')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('c')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Cliente'] = request.POST['Cliente']
                    request.session['Nombre'] = request.POST['Nombre']
                    request.session['AP'] = request.POST['AP']
                    request.session['AM'] = request.POST['AM']
                    request.session['RFC'] = request.POST['RFC']
                    url = reverse('cm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('c')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/client.html', {
                    "mensaje": request.session['Mensaje'],
                    'form':form,
                    'clientes': clientes,
                    'nclientes': nclientes
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/client.html', {
                    "error": request.session['Error'],
                    'form':form,
                    'clientes': clientes,
                    'nclientes': nclientes
                })
            else:
                return render(request, 'user_enc_ventas/client.html', {
                    'form':form,
                    'clientes': clientes,
                    'nclientes': nclientes
                })
    else: 
        return render(request, 'denied.html')

@login_required
def clientDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtiene el miembro y elimina
            c = Cliente.objects.get(id=request.session.get('Cliente'))
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Cliente eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('c')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def clientRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se crea el miembro
            Cliente.objects.create(
                nombreCliente=request.session.get('Nombre'),
                apellidoPCliente=request.session.get('AP'),
                apellidoMCliente=request.session.get('AM'),
                rfcCliente=request.session.get('RFC')
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Cliente registrado correctamente."
        except Exception as e:
            print(e)
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('c')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def clientModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se modifican

            cliente = Cliente.objects.get(id=request.session.get('Cliente'))
            cliente.nombreCliente = request.session.get('Nombre')
            cliente.apellidoPCliente = request.session.get('AP')
            cliente.apellidoMCliente = request.session.get('AM')
            cliente.rfcCliente = request.session.get('RFC')
            cliente.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('c')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def quality(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        formcalibre = AddCaliber()
        formcalidad = AddQuality()
        calidades = Calidad.objects.all()
        ncalidades = calidades.count()
        calibres = Calibre.objects.all()
        ncalibres = calibres.count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminarcalibre':
                try:
                    request.session['Calibre'] = request.POST['Calibre']
                    url = reverse('qdc')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            if request.POST['Id']=='eliminarcalidad':
                try:
                    request.session['Calidad'] = request.POST['Calidad']
                    url = reverse('qdq')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='agregarcalibre':
                try:
                    request.session['Numero'] = request.POST['Numero']
                    url = reverse('qrc')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='agregarcalidad':
                try:
                    request.session['Numero'] = request.POST['Numero']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    url = reverse('qrq')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Calidad'] = request.POST['Calidad']
                    request.session['Numero'] = request.POST['Numero']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    url = reverse('qm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/quality.html', {
                    "mensaje": request.session['Mensaje'],
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/quality.html', {
                    "error": request.session['Error'],
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
            else:
                return render(request, 'user_enc_ventas/quality.html', {
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
    else: 
        return render(request, 'denied.html')

@login_required
def qualityDeleteQuality(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtiene el miembro y elimina
            c = Calidad.objects.get(id=request.session.get('Calidad'))
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calidad eliminada correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def qualityDeleteCaliber(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtiene el miembro y elimina
            c = Calibre.objects.get(id=request.session.get('Calibre'))
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calibre eliminado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def qualityRegisterQuality(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se crea el miembro
            Calidad.objects.create(
                numCalidad=request.session.get('Numero'),
                descripcionCalidad=request.session.get('Descripcion')
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calidad registrada correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def qualityRegisterCaliber(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se crea el miembro
            Calibre.objects.create(
                numCalibre=request.session.get('Numero')
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calibre registrado correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def qualityModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se modifican

            calidad = Calidad.objects.get(id=request.session.get('Calidad'))
            calidad.numCalidad = request.session.get('Numero')
            calidad.descripcionCalidad = request.session.get('Descripcion')
            calidad.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def courtOrder(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        formcalibre = AddCaliber()
        formcalidad = AddQuality()
        calidades = Calidad.objects.all()
        ncalidades = calidades.count()
        calibres = Calibre.objects.all()
        ncalibres = calibres.count()
        #si se envia un formulario
        if request.method == 'POST':
            if request.POST['Id']=='eliminarcalibre':
                try:
                    request.session['Calibre'] = request.POST['Calibre']
                    url = reverse('qdc')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            if request.POST['Id']=='eliminarcalidad':
                try:
                    request.session['Calidad'] = request.POST['Calidad']
                    url = reverse('qdq')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='agregarcalibre':
                try:
                    request.session['Numero'] = request.POST['Numero']
                    url = reverse('qrc')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='agregarcalidad':
                try:
                    request.session['Numero'] = request.POST['Numero']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    url = reverse('qrq')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
            elif request.POST['Id']=='modificar':
                try:
                    request.session['Calidad'] = request.POST['Calidad']
                    request.session['Numero'] = request.POST['Numero']
                    request.session['Descripcion'] = request.POST['Descripcion']
                    url = reverse('qm')
                    return redirect(url)
                except Exception as e:
                    request.session['Operacion'] = 0
                    request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
                    url = reverse('q')
                    return redirect(url)
        else:
            if request.session.get('Operacion')==1:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/quality.html', {
                    "mensaje": request.session['Mensaje'],
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
            elif request.session.get('Operacion')==0:
                request.session['Operacion'] = -1
                return render(request, 'user_enc_ventas/quality.html', {
                    "error": request.session['Error'],
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
            else:
                return render(request, 'user_enc_ventas/quality.html', {
                    'formcalidad':formcalidad,
                    'formcalibre':formcalibre,
                    'calidades': calidades,
                    'ncalidades': ncalidades,
                    'calibres': calibres,
                    'ncalibres': ncalibres
                })
    else: 
        return render(request, 'denied.html')

@login_required
def courtOrderDelete(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtiene el miembro y elimina
            c = Calidad.objects.get(id=request.session.get('Calidad'))
            c.delete()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calidad eliminada correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar la eliminación, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def courtOrderRegister(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se crea el miembro
            Calidad.objects.create(
                numCalidad=request.session.get('Numero'),
                descripcionCalidad=request.session.get('Descripcion')
            )
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen

            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Calidad registrada correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo realizar el registro, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def courtOrderModify(request):
    if request.user.trabajador.rol.nomenclaturaRol == 'E_V':
        try:
            #Se obtienen los datos y se modifican

            calidad = Calidad.objects.get(id=request.session.get('Calidad'))
            calidad.numCalidad = request.session.get('Numero')
            calidad.descripcionCalidad = request.session.get('Descripcion')
            calidad.save()
            #Se guarda en memoria la operacion exitosa y redirige a la url de origen
            
            request.session['Operacion'] = 1
            request.session['Mensaje'] = "Se guardaron las modificaciones correctamente."
        except Exception as e:
            request.session['Operacion'] = 0
            request.session['Error'] = "No se pudo modificar los datos, intente de nuevo."
            
        url = reverse('q')
        return redirect(url)
    else: 
        return render(request, 'denied.html')

@login_required
def viewOrder(request):
    if request.user.trabajador.rol.nomenclaturaRol in ('E_B', 'I_C'):
        pedidos = Pedido.objects.all()
        p = Pedido.objects.filter(estatusPedido='P_P')
        npedidosp = p.count()
        p = Pedido.objects.filter(estatusPedido='P_T')
        npedidost = p.count()

        return render(request, 'user_enc_bit/viewOrder.html', {
            'pedidos': pedidos,
            'npedidosp': npedidosp,
            'npedidost': npedidost
        })
    else: 
        return render(request, 'denied.html')
