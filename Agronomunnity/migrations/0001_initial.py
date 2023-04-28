# Generated by Django 4.1 on 2023-04-25 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calibre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numCalibre', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Calibre',
                'verbose_name_plural': 'Calibres',
                'db_table': 'calibre',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Calidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcionCalidad', models.CharField(blank=True, max_length=500)),
                ('numCalidad', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Calidad',
                'verbose_name_plural': 'Calidades',
                'db_table': 'calidad',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CamionTransporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidadTransporte', models.CharField(blank=True, max_length=20)),
                ('placaTransporte', models.CharField(blank=True, max_length=20)),
                ('modeloTransporte', models.CharField(blank=True, max_length=50)),
                ('tipoTransporte', models.CharField(blank=True, max_length=50)),
                ('descripcionTransporte', models.CharField(blank=True, max_length=200)),
                ('candadoTransporte', models.CharField(blank=True, max_length=20)),
                ('estatusTransporte', models.CharField(choices=[('C_A', 'Activo'), ('C_I', 'Inactivo'), ('C_M', 'Mantenimiento')], default='Activo', max_length=3)),
            ],
            options={
                'verbose_name': 'CamionTransporte',
                'verbose_name_plural': 'CamionesTransporte',
                'db_table': 'camiontransporte',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCliente', models.CharField(blank=True, max_length=40)),
                ('apellidoPCliente', models.CharField(blank=True, max_length=20)),
                ('apellidoMCliente', models.CharField(blank=True, max_length=20)),
                ('rfcCliente', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cuadrilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCuadrilla', models.CharField(blank=True, max_length=50)),
                ('ubicacionCuadrilla', models.CharField(blank=True, max_length=50)),
                ('estatusCuadrilla', models.CharField(choices=[('C_A', 'Activa'), ('C_I', 'Inactiva')], default='Activa', max_length=3)),
            ],
            options={
                'verbose_name': 'Cuadrilla',
                'verbose_name_plural': 'Cuadrillas',
                'db_table': 'cuadrilla',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Huerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreHuerta', models.CharField(blank=True, max_length=50)),
                ('frutaHuerta', models.CharField(blank=True, max_length=30)),
                ('ubicacionHuerta', models.CharField(blank=True, max_length=50)),
                ('localizacionHuerta', models.CharField(blank=True, max_length=300)),
                ('claveSagarpaHuerta', models.CharField(blank=True, max_length=100)),
                ('estatusInocuidadHuerta', models.CharField(blank=True, max_length=100)),
                ('estatusHuerta', models.CharField(choices=[('H_A', 'Activo'), ('H_I', 'Inactivo')], default='Activo', max_length=3)),
            ],
            options={
                'verbose_name': 'Huerta',
                'verbose_name_plural': 'MHuertas',
                'db_table': 'huerta',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OrdenCorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaOrden', models.DateField()),
                ('numeroOrden', models.CharField(blank=True, max_length=20)),
                ('cantidadFruta', models.FloatField(blank=True, max_length=10)),
                ('tipoFruta', models.CharField(blank=True, max_length=20)),
                ('calidadFruta', models.CharField(blank=True, max_length=20)),
                ('tipoCorte', models.CharField(blank=True, max_length=20)),
                ('estatusOrden', models.CharField(choices=[('O_P', 'Pendiente'), ('O_T', 'Terminado')], default='Pendiente', max_length=3)),
                ('idHuerta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.huerta')),
            ],
            options={
                'verbose_name': 'OrdenCorte',
                'verbose_name_plural': 'OrdenesCorte',
                'db_table': 'ordenCorte',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroPedido', models.CharField(blank=True, max_length=20)),
                ('fechaPedido', models.DateField()),
                ('totalKilosPedido', models.IntegerField(blank=True)),
                ('totalPalletsPedido', models.IntegerField(blank=True)),
                ('mercadoPedido', models.CharField(blank=True, max_length=20)),
                ('destinoPedido', models.CharField(blank=True, max_length=20)),
                ('estatusPedido', models.CharField(choices=[('P_P', 'Pendiente'), ('P_T', 'Terminado')], default='Pendiente', max_length=3)),
                ('idCliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Productor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20)),
                ('apellidoP', models.CharField(blank=True, max_length=30)),
                ('apellidoM', models.CharField(blank=True, max_length=30)),
                ('telefono', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'Productor',
                'verbose_name_plural': 'Productores',
                'db_table': 'productor',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RolTrabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomenclaturaRol', models.CharField(blank=True, max_length=3)),
                ('nombreRol', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'RolTrabajador',
                'verbose_name_plural': 'RolesTrabajador',
                'db_table': 'roltrabajador',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ViajeCorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaViaje', models.DateField()),
                ('horaSalida', models.TimeField(blank=True, max_length=20)),
                ('horaLlegada', models.TimeField(blank=True, max_length=20)),
                ('puntoReunion', models.CharField(blank=True, max_length=500)),
                ('estatusViaje', models.CharField(choices=[('V_P', 'No terminado'), ('V_T', 'Terminado')], default='No terminado', max_length=3)),
                ('idCamionSecundarioTransporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secundario', to='Agronomunnity.camiontransporte')),
                ('idCamionTransporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='principal', to='Agronomunnity.camiontransporte')),
                ('idCuadrilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.cuadrilla')),
                ('idOrdenCorte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.ordencorte')),
            ],
            options={
                'verbose_name': 'ViajeCorte',
                'verbose_name_plural': 'ViajesCorte',
                'db_table': 'viajecorte',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(blank=True, max_length=10)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.roltrabajador')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Trabajador',
                'verbose_name_plural': 'Trabajadores',
                'db_table': 'trabajador',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ReporteCorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('documento', models.FileField(upload_to='Reportes/Corte')),
                ('cajasCortadas', models.IntegerField(blank=True)),
                ('observacionesReporte', models.CharField(blank=True, max_length=500)),
                ('idCuadrilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.cuadrilla')),
            ],
            options={
                'verbose_name': 'ReporteCorte',
                'verbose_name_plural': 'ReporteCortes',
                'db_table': 'reportecorte',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PedidoCalibreCalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadCC', models.IntegerField(blank=True)),
                ('idCalibre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.calibre')),
                ('idCalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.calidad')),
                ('idPedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.pedido')),
            ],
            options={
                'verbose_name': 'PedidoCalibreCalidad',
                'verbose_name_plural': 'PedidosCalibreCalidad',
                'db_table': 'pedidocalibrecalidad',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='pedido',
            name='idTrabajador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.trabajador'),
        ),
        migrations.CreateModel(
            name='MiembroCuadrilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20)),
                ('apellidoP', models.CharField(blank=True, max_length=30)),
                ('apellidoM', models.CharField(blank=True, max_length=30)),
                ('noImss', models.CharField(blank=True, max_length=30)),
                ('idCuadrilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.cuadrilla')),
            ],
            options={
                'verbose_name': 'MiembroC',
                'verbose_name_plural': 'MiembrosC',
                'db_table': 'miembroc',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='huerta',
            name='idProductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.productor'),
        ),
        migrations.AddField(
            model_name='cuadrilla',
            name='idGerenteCuadrilla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gerente', to='Agronomunnity.trabajador'),
        ),
        migrations.AddField(
            model_name='cuadrilla',
            name='idJefeCuadrilla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jefe', to='Agronomunnity.trabajador'),
        ),
        migrations.AddField(
            model_name='camiontransporte',
            name='idChoferTransporte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.trabajador'),
        ),
    ]
