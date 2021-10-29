from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import CalificacionesModel, UsuarioModel, CursoModel, AlumnosModel
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

class RegistroSerializer(serializers.ModelSerializer):

    usuarioFoto = serializers.CharField(max_length=250)
    
    def save(self):

        usuarioNombre = self.validated_data.get('usuarioNombre')
        usuarioApellido = self.validated_data.get('usuarioApellido')
        usuarioTipo = self.validated_data.get('usuarioTipo')
        usuarioCorreo = self.validated_data.get('usuarioCorreo')
        usuarioFoto = self.validated_data.get('usuarioFoto')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(usuarioNombre=usuarioNombre,usuarioApellido=usuarioApellido,usuarioTipo=usuarioTipo,usuarioCorreo=usuarioCorreo,usuarioFoto=usuarioFoto)

        nuevoUsuario.set_password(password)
        nuevoUsuario.save()

        return nuevoUsuario

    class Meta:

        model = UsuarioModel

        exclude = ['groups','user_permissions','is_superuser','last_login','is_staff','is_active']

        extra_kwargs = {
            'password':{
                'write_only':True,
            }
        }

        

class CalificacionesSeriealizer(serializers.ModelSerializer):
    
    class Meta:
        model = CalificacionesModel
        fields = '__all__'
        # exclude=['password']

class CalificacionesSeriealizer0(serializers.ModelSerializer):
    
    class Meta:
        model = CalificacionesModel
        fields = ['usuario']
        # exclude=['password']

class CursoSerializer0(serializers.ModelSerializer):

    class Meta:
        model = CursoModel
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):

    cursoCalificacion = CalificacionesSeriealizer(many=True)

    class Meta:
        model = CursoModel
        fields = '__all__'
        # depth = 1

class UsuarioSerializer0(serializers.ModelSerializer):

    class Meta:
        model = UsuarioModel
        fields = ['usuarioId','usuarioNombre','usuarioApellido','usuarioCorreo','matricula']

class UsuarioSerializer(serializers.ModelSerializer):
    usuarioCalificacion = CalificacionesSeriealizer(many=True)

    class Meta:
        model = UsuarioModel
        # exclude = ['usuaioId']
        # fields = '__all__'
        exclude=['password','is_staff','is_active','groups','user_permissions','last_login','is_superuser']

class UsuarioCursoSerializer(serializers.ModelSerializer):

    cursoCalificacion = CalificacionesSeriealizer0(many=True)

    class Meta:
        model = CursoModel
        fields='__all__'

class AlumnoSerializer(serializers.ModelSerializer):

    class Meta:

        model = AlumnosModel
        fields = '__all__'

class ImagenSerializer(serializers.Serializer):

    archivo: InMemoryUploadedFile = serializers.ImageField(max_length=250, use_url=True)