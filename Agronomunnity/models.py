from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Trabajador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=10, blank = True)
    rol = models.ForeignKey('RolTrabajador', on_delete=models.CASCADE)
    
    def Mostrar(self):
        return "{} {} - {}".format(self.usuario.first_name, self.usuario.last_name, self.rol.nombreRol)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Trabajador'
        verbose_name_plural= 'Trabajadores'
        db_table= 'trabajador'
        ordering= ['id']

class RolTrabajador(models.Model):
    nomenclaturaRol = models.CharField(max_length=3, blank = True)
    nombreRol = models.CharField(max_length=50, blank = True)

    def Mostrar(self):
        return "{} - {}".format(self.nomenclaturaRol, self.nombreRol)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'RolTrabajador'
        verbose_name_plural= 'RolesTrabajador'
        db_table= 'roltrabajador'
        ordering= ['id']

class CamionTransporte(models.Model):
    idChoferTransporte = models.ForeignKey('Trabajador', on_delete=models.CASCADE)
    capacidadTransporte = models.CharField(max_length=20, blank = True)
    placaTransporte = models.CharField(max_length=20, blank = True)
    modeloTransporte = models.CharField(max_length=50, blank = True)
    tipoTransporte = models.CharField(max_length=50, blank = True)
    descripcionTransporte = models.CharField(max_length=200, blank = True)
    candadoTransporte = models.CharField(max_length=20, blank = True)
    estatusCamion = (
        ('C_A', 'Activo'),
        ('C_I', 'Inactivo'),
        ('C_M', 'Mantenimiento'),
    )
    estatusTransporte = models.CharField(max_length=3, choices=estatusCamion, default='Activo')
    

    def Mostrar(self):
        return "{} - {}".format(self.modeloTransporte, self.placaTransporte)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'CamionTransporte'
        verbose_name_plural= 'CamionesTransporte'
        db_table= 'camiontransporte'
        ordering= ['id']

class MiembroCuadrilla(models.Model):
    nombre = models.CharField(max_length=20, blank = True)
    apellidoP = models.CharField(max_length=30, blank = True)
    apellidoM = models.CharField(max_length=30, blank = True)
    noImss = models.CharField(max_length=30, blank = True)
    idCuadrilla = models.ForeignKey('Cuadrilla', on_delete=models.CASCADE)

    def Mostrar(self):
        return "{} {} {}".format(self.nombre, self.apellidoP, self.apellidoM)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'MiembroC'
        verbose_name_plural= 'MiembrosC'
        db_table= 'miembroc'
        ordering= ['id']

class Cuadrilla(models.Model):
    idGerenteCuadrilla = models.ForeignKey('Trabajador', related_name='gerente', on_delete=models.CASCADE)
    idJefeCuadrilla = models.ForeignKey('Trabajador', related_name='jefe', on_delete=models.CASCADE)
    nombreCuadrilla = models.CharField(max_length=50, blank = True)
    ubicacionCuadrilla = models.CharField(max_length=50, blank = True)
    estatus = (
        ('C_L', 'Libre'),
        ('C_O', 'Ocupada'),
    )
    estatusCuadrilla = models.CharField(max_length=3, choices=estatus, default='Activa')

    def Mostrar(self):
        return "{} - {}".format(self.nombreCuadrilla, self.get_estatusCuadrilla_display())

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cuadrilla'
        verbose_name_plural= 'Cuadrillas'
        db_table= 'cuadrilla'
        ordering= ['id']

class Productor(models.Model):
    nombre = models.CharField(max_length=20, blank = True)
    apellidoP = models.CharField(max_length=30, blank = True)
    apellidoM = models.CharField(max_length=30, blank = True)
    telefono = models.CharField(max_length=10, blank = True)

    def Mostrar(self):
        return "{} {} {}".format(self.nombre, self.apellidoP, self.apellidoM)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Productor'
        verbose_name_plural= 'Productores'
        db_table= 'productor'
        ordering= ['id']

class Huerta(models.Model):
    idProductor = models.ForeignKey('Productor', on_delete=models.CASCADE)
    nombreHuerta = models.CharField(max_length=50, blank = True)
    ubicacionHuerta = models.CharField(max_length=50, blank = True)
    localizacionHuerta = models.CharField(max_length=300, blank = True)
    claveSagarpaHuerta = models.CharField(max_length=100, blank = True)
    estatusInocuidadHuerta = models.CharField(max_length=100, blank = True)
    estatus = (
        ('H_D', 'Con fruta Disponible'),
        ('H_S', 'Sin fruta disponible'),
    )
    estatusHuerta = models.CharField(max_length=3, choices=estatus, default='Activo')

    municipio = (
        ('UPN','Uruapan'),
        ('SES','Salvador Escalante'),
        ('TAN','Tancítaro'),
        ('PER','Peribán'),
        ('TCM','Tacámbaro'),
        ('ADR','Ario de Rosales')
    )
    ubicacionHuerta = models.CharField(max_length=3, choices=municipio, default='UPN')

    fruta = (
        ('AGT', 'Aguacate'),
    )
    frutaHuerta = models.CharField(max_length=3, choices=fruta, default='AGT')

    def Mostrar(self):
        return "{}, {}".format(self.nombreHuerta, self.get_estatusHuerta_display())

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Huerta'
        verbose_name_plural= 'MHuertas'
        db_table= 'huerta'
        ordering= ['id']

class Cliente(models.Model):
    nombreCliente = models.CharField(max_length=40, blank = True)
    apellidoPCliente = models.CharField(max_length=20, blank = True) 
    apellidoMCliente = models.CharField(max_length=20, blank = True)
    rfcCliente = models.CharField(max_length=20, blank = True)

    def Mostrar(self):
        return "{} {} {}".format(self.nombreCliente, self.apellidoPCliente, self.apellidoMCliente)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Cliente'
        verbose_name_plural= 'Clientes'
        db_table= 'cliente'
        ordering= ['id']

class Pedido(models.Model):
    idTrabajador = models.ForeignKey('Trabajador', on_delete=models.CASCADE)
    idCliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    numeroPedido = models.CharField(max_length=20, blank = True)
    fechaPedido = models.DateField()
    totalKilosPedido = models.IntegerField(blank=True)
    totalPalletsPedido = models.IntegerField(blank=True)
    destinoPedido = models.CharField(max_length=50, blank = True)
    observacionPedido = models.CharField(max_length=500, blank = True)
    mercado = (
        ('M_N', 'Nacional'),
        ('M_E', 'Exportación'),
        ('M_O', 'Otros destinos'),
    )
    mercadoPedido = models.CharField(max_length=3, choices=mercado, default='Nacional')
    estatus = (
        ('P_I', 'Iniciado'),
        ('P_O', 'Ordenado'),
        ('P_V', 'En viaje'),
        ('P_C', 'Completado'),
    )
    estatusPedido = models.CharField(max_length=3, choices=estatus, default='Pendiente')

    def Mostrar(self):
        return "Pedido: {} - {}".format(self.numeroPedido, self.get_estatusPedido_display())

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Pedido'
        verbose_name_plural= 'Pedidos'
        db_table= 'pedido'
        ordering= ['id']

class Calibre(models.Model):
    numCalibre = models.IntegerField(blank=True)
    descripcionCalibre = models.CharField(max_length=500, blank = True)

    def Mostrar(self):
        return "Calibre: {}".format(self.numCalibre)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Calibre'
        verbose_name_plural= 'Calibres'
        db_table= 'calibre'
        ordering= ['id']

class Calidad(models.Model):
    descripcionCalidad = models.CharField(max_length=500, blank = True)
    numCalidad = models.IntegerField(blank=True)

    def Mostrar(self):
        return "Calidad: {}".format(self.numCalidad)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Calidad'
        verbose_name_plural= 'Calidades'
        db_table= 'calidad'
        ordering= ['id']

class PedidoCalibreCalidad(models.Model):
    idPedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    idCalibre = models.ForeignKey('Calibre', on_delete=models.CASCADE)
    idCalidad = models.ForeignKey('Calidad', on_delete=models.CASCADE)
    cantidadCC = models.IntegerField(blank=True)

    def Mostrar(self):
        return "Pedido: {} - {} kg.".format(self.idPedido, self.cantidadCC)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PedidoCalibreCalidad'
        verbose_name_plural= 'PedidosCalibreCalidad'
        db_table= 'pedidocalibrecalidad'
        ordering= ['id']

class OrdenCorte(models.Model):
    fechaOrden = models.DateField()
    numeroOrden = models.CharField(max_length=20, blank = True)
    corte = (
        ('','(Seleccione)'),
        ('AVN', 'Aventajado'),
        ('FLC', 'Flor loca'),
    )
    tipoCorte = models.CharField(max_length=3, choices=corte, default='')
    idPedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, null=True)
    idHuerta = models.ForeignKey('Huerta', on_delete=models.CASCADE, null=True)

    def Mostrar(self):
        return "Orden: {} - {}".format(self.numeroOrden, self.fechaOrden)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'OrdenCorte'
        verbose_name_plural= 'OrdenesCorte'
        db_table= 'ordencorte'
        ordering= ['id']

class ViajeCorte(models.Model):
    fechaViaje = models.DateField()
    idCamionTransporte = models.ForeignKey('CamionTransporte', related_name='principal', on_delete=models.CASCADE)
    idCamionSecundarioTransporte = models.ForeignKey('CamionTransporte', related_name='secundario', on_delete=models.CASCADE)
    horaSalida = models.TimeField(max_length=20, blank = True)
    horaLlegada = models.TimeField(max_length=20, blank = True, null=True)
    idOrdenCorte = models.ForeignKey('OrdenCorte', on_delete=models.CASCADE)
    idCuadrilla = models.ForeignKey('Cuadrilla', on_delete=models.CASCADE)
    puntoReunion = models.CharField(max_length=500, blank = True)

    def Mostrar(self):
        return "Viaje del dia: {} - {}".format(self.fechaViaje, self.horaSalida)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ViajeCorte'
        verbose_name_plural= 'ViajesCorte'
        db_table= 'viajecorte'
        ordering= ['id']

class Incidencia(models.Model):
    descripcionIncidencia = models.CharField(max_length=500, blank = True)
    idTrabajador = models.ForeignKey('Trabajador', on_delete=models.CASCADE)
    fechaIncidencia = models.DateField()
    descripcionSolucion = models.CharField(max_length=500, blank = True)

    temas = (
        ('B_T','Bitacoras'),
        ('C_M','Camiones'),
        ('C_A','Calidad'),
        ('C_L','Clientes'),
        ('C_D','Cuadrillas'),
        ('D_C','Documentos'),
        ('E_N','Encargados'),
        ('G_R','Gerentes'),
        ('H_R','Huertas'),
        ('G_F','Jefes'),
        ('O_C','Ordenes de corte'),
        ('P_D','Pedidos'),
        ('P_T','Productores'),
        ('T_B','Trabajadores'),
        ('T_P','Transportes'),
        ('V_J','Viajes'),
    )
    temaIncidencia = models.CharField(max_length=3, choices=temas, default='B_T')

    estatus = (
        ('I_P', 'Pendiente'),
        ('I_R', 'Resuelta'),
    )
    estatusIncidencia = models.CharField(max_length=3, choices=estatus, default='I_P')

    def Mostrar(self):
        return "Incidencia: {} - {}".format(self.id, self.get_estatusIncidencia_display())

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'Incidencia'
        verbose_name_plural= 'Incidencias'
        db_table= 'incidencia'
        ordering= ['id']

class PrecioAutorizado(models.Model):
    precioFijo = models.FloatField(blank=True)
    descripcion = models.CharField(max_length=500, blank = True)
    precioActual = models.FloatField(blank=True)
    vigencia = models.DateField()

    estados = (
        ('AGS', 'Aguascalientes'),
        ('BC', 'Baja California'),
        ('BCS', 'Baja California Sur'),
        ('CAM', 'Campeche'),
        ('CHIS', 'Chiapas'),
        ('CHIH', 'Chihuahua'),
        ('CDMX', 'Ciudad de México'),
        ('COAH', 'Coahuila'),
        ('COL', 'Colima'),
        ('DGO', 'Durango'),
        ('GTO', 'Guanajuato'),
        ('GRO', 'Guerrero'),
        ('HGO', 'Hidalgo'),
        ('JAL', 'Jalisco'),
        ('MEX', 'México'),
        ('MIC', 'Michoacán'),
        ('MOR', 'Morelos'),
        ('NAY', 'Nayarit'),
        ('NL', 'Nuevo León'),
        ('OAX', 'Oaxaca'),
        ('PUE', 'Puebla'),
        ('QRO', 'Querétaro'),
        ('QR', 'Quintana Roo'),
        ('SLP', 'San Luis Potosí'),
        ('SIN', 'Sinaloa'),
        ('SON', 'Sonora'),
        ('TAB', 'Tabasco'),
        ('TAMPS', 'Tamaulipas'),
        ('TLAX', 'Tlaxcala'),
        ('VER', 'Veracruz'),
        ('YUC', 'Yucatán'),
        ('ZAC', 'Zacatecas'),
    )

    estadoAplica = models.CharField(max_length=5, choices=estados, default='')

    def Mostrar(self):
        return "Precio de: {} - Autorizado para: {}".format(self.precioActual, self.get_estadoAplica_display())

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'PrecioAutorizado'
        verbose_name_plural= 'PreciosAutorizados'
        db_table= 'precioautorizado'
        ordering= ['id']

class FrutaHuerta(models.Model):
    idHuerta = models.OneToOneField('Huerta', on_delete=models.CASCADE)
    descripcionFruta = models.CharField(max_length=500, blank=True)
    precioFruta = models.FloatField(blank=True)

    def Mostrar(self):
        return "Huerta: {} - Fruta: {}".format(self.idHuerta.nombreHuerta, self.descripcionFruta)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name = 'FrutaHuerta'
        verbose_name_plural = 'FrutaHuertas'
        db_table = 'frutahuerta'
        ordering = ['id']

class ReporteCorte(models.Model):
    fecha = models.DateField()
    idViaje = models.OneToOneField('ViajeCorte', on_delete=models.CASCADE, null=True, unique=True)
    observacionesReporte = models.CharField(max_length=500, blank = True)
    cajasCortadas = models.IntegerField(blank=True)
    def Mostrar(self):
        return "Reporte del dia: {} - {} cajas cortadas.".format(self.fecha, self.cajasCortadas)

    def __str__(self):
        return self.Mostrar()

    class Meta:
        verbose_name= 'ReporteCorte'
        verbose_name_plural= 'ReportesCorte'
        db_table= 'reportecorte'
        ordering= ['id']