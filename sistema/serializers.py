from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import CalificacionesModel, UsuarioModel, CursoModel

class RegistroSerializer(serializers.ModelSerializer):

    
    def save(self):

        usuarioNombre = self.validated_data.get('usuarioNombre')
        usuarioApellido = self.validated_data.get('usuarioApellido')
        usuarioTipo = self.validated_data.get('usuarioTipo')
        usuarioCorreo = self.validated_data.get('usuarioCorreo')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(usuarioNombre=usuarioNombre,usuarioApellido=usuarioApellido,usuarioTipo=usuarioTipo,usuarioCorreo=usuarioCorreo)

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

class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CursoModel
        fields = '__all__'
        # depth = 1
        

class CalificacionesSeriealizer(serializers.ModelSerializer):
    
    class Meta:
        model = CalificacionesModel
        fields = '__all__'