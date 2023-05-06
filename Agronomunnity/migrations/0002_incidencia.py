# Generated by Django 4.1 on 2023-04-29 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Agronomunnity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcionIncidencia', models.CharField(blank=True, max_length=500)),
                ('fechaIncidencia', models.DateField()),
                ('descripcionSolucion', models.CharField(blank=True, max_length=500)),
                ('estatusIncidencia', models.CharField(choices=[('I_P', 'Pendiente'), ('I_R', 'Resuelta')], default='Pendiente', max_length=3)),
                ('idTrabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.trabajador')),
            ],
            options={
                'verbose_name': 'Incidencia',
                'verbose_name_plural': 'Incidencias',
                'db_table': 'incidencia',
                'ordering': ['id'],
            },
        ),
    ]