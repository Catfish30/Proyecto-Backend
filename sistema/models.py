from django import db
from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser

class ManejoUsuario(BaseUserManager):

    def create_user(self,correo,nombre,apellido,tipo,password):

        if not correo:
            raise ValueError('Ingresar un correo valido')

        correo = self.normalize_email(correo)

        usuarioCreado = self.model(usuarioCorreo=correo,usuarioNombre=nombre, usuarioApellido=apellido, usuarioTipo= tipo)

        usuarioCreado.set_password(password)

        usuarioCreado.save(using=self._db)

        return usuarioCreado

    def create_superuser(self,usuarioCorreo,usuarioNombre,usuarioApellido,usuarioTipo,password):

        nuevoUsuario = self.create_user(usuarioCorreo,usuarioNombre,usuarioApellido,usuarioTipo,password)

        nuevoUsuario.is_superuser = True
        nuevoUsuario.is_staff = True
        nuevoUsuario.save(using=self._db)


class UsuarioModel(AbstractBaseUser,PermissionsMixin):

    tipo_usuario = [(1,'ADMINISTRADOR'),(2,'DOCENTE'),(3,'ALUMNO')]

    usuarioId= models.AutoField(primary_key=True,db_column='id',unique=True,null=False,verbose_name='ID')

    usuarioNombre = models.CharField(max_length=100,db_column='nombre',verbose_name='Nombre del usuario')

    usuarioApellido = models.CharField(max_length=100,db_column='apellido',verbose_name='Apellido del usuario')

    usuarioCorreo = models.EmailField(max_length=200,db_column='correo',unique=True,verbose_name='Correo del usuario')

    usuarioTipo = models.IntegerField(choices=tipo_usuario,db_column='tipo',verbose_name='Tipo del usuario')

    password = models.TextField(null=False,verbose_name='contraseña del Usuario')

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)


    objects = ManejoUsuario()

    USERNAME_FIELD = 'usuarioCorreo'

    REQUIRED_FIELDS = ['usuarioNombre','usuarioApellido','usuarioTipo']

    class Meta:
        db_table = 'usuarios'


class CursoModel(models.Model):

    cursoId = models.AutoField(primary_key=True,null=False,unique=True, db_column='id')

    cursoNombre= models.CharField(max_length=100, null=False, db_column='nombre')

    cursoSemestre=models.IntegerField(db_column='semestre', null=False )

    docente= models.ForeignKey(to=UsuarioModel,db_column='usuario_id', on_delete=models.PROTECT, related_name='docenteCurso', null=False)

    class Meta:

        db_table = 'cursos'

class CalificacionesModel(models.Model):

    tipo_nota = [(1,'EXAMEN'),(2,'TAREA')]
    
    calificacionId = models.AutoField(primary_key=True,null=False,unique=True,db_column='id')

    calificacionDetalle = models.TextField(max_length=200, null=True, db_column='detalle')

    calificacionFecha = models.DateTimeField(auto_now_add=True, db_column='fecha')

    calificacionTipo = models.IntegerField(choices=tipo_nota,db_column='tipo', null=False)

    calificacionNota = models.DecimalField(max_digits=4,decimal_places=2,db_column='nota',null=False)

    curso = models.ForeignKey(to=CursoModel, db_column='curso_id', on_delete=models.PROTECT, related_name='cursoCalificacion', null=False)

    usuario = models.ForeignKey(to=UsuarioModel, db_column='usuario_id', on_delete=models.PROTECT, related_name='usuarioCalificacion', null=False)

    class Meta:

        db_table = 'calificaciones'
