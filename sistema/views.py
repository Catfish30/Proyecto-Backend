from functools import partial
from logging import error
from django.utils.translation import check_for_language
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cloudinary.uploader import upload

from sistema.models import AlumnosModel, CalificacionesModel, CursoModel, UsuarioModel
from .serializers import CalificacionesSeriealizer, ImagenSerializer, RegistroSerializer, CursoSerializer, UsuarioSerializer, CursoSerializer0,UsuarioSerializer0, UsuarioCursoSerializer,AlumnoSerializer,CursoSerializer01

class RegistroController(CreateAPIView):
    
    serializer_class = RegistroSerializer

    def post(self,request: Request):
        data = self.serializer_class(data = request.data)

        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Usuario creado exitosamente',
                'content':data.data
            })
        else:
            return Response(data={
                'message':'Error al crear la ruta',
                'content': data.errors
            })

class UsuarioController(RetrieveUpdateDestroyAPIView):

    serializer_class = UsuarioSerializer
    queryset = UsuarioModel.objects.all()

    permission_classes = (IsAuthenticated,)

    def patch(self,request,id):
        usuarioEncontrado = self.get_queryset().filter(usuarioId=id).first()

        if not usuarioEncontrado:
            return Response(data={
                'message':'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        serializador = UsuarioSerializer(UsuarioModel,data=request.data,partial=True)
        if serializador.is_valid():
            serializador.update(instance=usuarioEncontrado, validated_data=serializador.validated_data)

            return Response(data={
                'message':'Usuario actualizado exitosamente',
                'content': serializador.validated_data
            },status=status.HTTP_200_OK)
        else:
            return Response(data={
                'message':'Error al actualizar el usuario',
                'content':serializador.errors
            },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id):
        usuarioEncontrado = self.get_queryset().filter(usuarioId=id).first()

        if not usuarioEncontrado:
            return Response(data={
                'message':'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = self.serializer_class(instance=usuarioEncontrado)

        return Response(data={
            'content': data.data
        },status=status.HTTP_200_OK)

    def delete(self,request,id):

        usuarioEncontrado = self.get_queryset().filter(usuarioId=id).first()

        if not usuarioEncontrado:
            return Response(data={
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        data = UsuarioModel.objects.filter(usuarioId=id).delete()
  
        return Response(data={
            'message': 'Usuario eliminado exitosamente'
        })


class CursosController(ListCreateAPIView):

    serializer_class = CursoSerializer0
    serializer_class01 =CursoSerializer01
    queryset = CursoModel.objects.all().order_by('docente')

    # permission_classes = (IsAuthenticated,)

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Curso creado exitosamente',
                'content':data.data
            },status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al crear el curso',
                'content':data.errors
            },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        data = self.serializer_class01(instance=self.get_queryset(),many=True)
        return Response(data={
                "message":None,
                "content":data.data
            })

    

class CursoController(RetrieveUpdateDestroyAPIView):

    serializer_class = CursoSerializer
    queryset = CursoModel.objects.all()

    # permission_classes = (IsAuthenticated,)

    def put(self,request,id):
        cursoEncontrado = self.get_queryset().filter(cursoId=id).first()

        if not cursoEncontrado:
            return Response(data={
                'message':'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        serializador = CursoSerializer(data=request.data)
        if serializador.is_valid():
            serializador.update(instance=cursoEncontrado, validated_data=serializador.validated_data)

            return Response(data={
                'message':'Curso actualizado exitosamente',
                'content': serializador.data
            },status=status.HTTP_200_OK)
        else:
            return Response(data={
                'message':'Error al actualizar el curso',
                'content':serializador.errors
            },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,id):
        cursoEncontrado = self.get_queryset().filter(cursoId=id).first()

        if not cursoEncontrado:
            return Response(data={
                'message':'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = self.serializer_class(instance=cursoEncontrado)

        return Response(data={
            'content': data.data
        },status=status.HTTP_200_OK)

    def delete(self,request,id):

        cursoEncontrado = self.get_queryset().filter(cursoId=id).first()

        if not cursoEncontrado:
            return Response(data={
                'message': 'Curso no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

        data = CursoModel.objects.filter(cursoId=id).delete()
  
        return Response(data={
            'message': 'Curso eliminado exitosamente'
        })


class BuscadorCursoController(RetrieveAPIView):
    
    serializer_class = CursoSerializer

    def get(self,request: Request):
        
        
        semestre = request.query_params.get('semestre')
        curso = request.query_params.get('docente')

        if semestre:
            cursosEncontrado = CursoModel.objects.filter(cursoSemestre__contains = semestre).all()

            data =  self.serializer_class(instance=cursosEncontrado, many=True)

            return Response({
                'content':data.data
            })
    
        # if curso:
        #     cursosEncontrado = CursoModel.objects.filter(cursoId = curso).first()
            
        #     data =  self.serializer_class_usuario(instance=cursosEncontrado)
            
        #     return Response({
        #         'content':data.data
        #     })
        

class CalificacionesController(CreateAPIView):
    serializer_class = CalificacionesSeriealizer
    queryset = CalificacionesModel.objects.all()

    queryset_u = UsuarioModel.objects.all()

    # permission_classes = (IsAuthenticated,)

    

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)

        
        if data.is_valid():

            usuario = data.data.get('usuario')
            usuarioEncontrado = UsuarioModel.objects.filter(usuarioId = usuario)
            estado = usuarioEncontrado.values_list('matricula', flat=True).get()
            
            if estado == False :             
                return Response(data={
                    'message':'Nota creada exitosamente',
                    'content':data.data
                },status=status.HTTP_201_CREATED)
                
            else:
                return Response(data={
                    'message':'Alumno no matriculado',
                    'content':data.errors
                },status=status.HTTP_400_BAD_REQUEST)

class BuscadorCalificacionController(RetrieveAPIView):
    
    serializer_class_curso = CursoSerializer
    serializer_class_usuario = UsuarioSerializer

    def get(self,request: Request):
        
        curso = request.query_params.get('curso')

        usuario = request.query_params.get('usuario')

        if curso:
            calificacionesEncontradas = CursoModel.objects.filter(cursoId = curso).first()
            data =  self.serializer_class_curso(instance=calificacionesEncontradas)

            return Response({
                'content':data.data
            })

        if usuario:
            calificacionesEncontradas = UsuarioModel.objects.filter(usuarioId = usuario).first()
            data =  self.serializer_class_usuario(instance=calificacionesEncontradas)

            return Response({
                'content':data.data
            })

class BuscarUsuariosController(RetrieveAPIView):

    serializer_class = UsuarioSerializer0

    def get(self,request: Request):

        matricula = request.query_params.get('matricula')

        if matricula:
            usuariosEncontrados = UsuarioModel.objects.filter(matricula = matricula).all()
            data = self.serializer_class(instance=usuariosEncontrados, many=True)
            print(data)
            return Response({
                'content':data.data
            })

class BuscarUsuariosCursoController(RetrieveAPIView):

    serializer_class = UsuarioCursoSerializer

    def get(self,request: Request):

        curso = request.query_params.get('curso')

        if curso:
            cursosEcontrados = CursoModel.objects.filter(cursoId = curso).first()
            data = self.serializer_class(instance=cursosEcontrados)
            print(data)
            return Response({
                'content':data.data
            })

class AlumnoController(CreateAPIView):

    serializer_class = AlumnoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Alumno registrado exitosamente',
                'content':data.data
            },status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al regsitrar alumno',
                'content':data.errors
            },status=status.HTTP_400_BAD_REQUEST)

class AlumnoCursosController(RetrieveAPIView):
    
    serializer_class = AlumnoSerializer

    def get(self,request: Request):
        
        curso = request.query_params.get('curso')

        alumno = request.query_params.get('alumno')

        if curso:
            alumnosEncontrado = AlumnosModel.objects.filter(curso = curso).all()

            data =  self.serializer_class(instance=alumnosEncontrado, many=True)

            return Response({
                'content':data.data
            })

        if alumno:
            cursosEncontrado = AlumnosModel.objects.filter(alumno = alumno).all()

            data =  self.serializer_class(instance=cursosEncontrado, many=True)

            return Response({
                'content':data.data
            })

class ImagenController(CreateAPIView):
    
    serializer_class = ImagenSerializer

    def post(self, request:Request):

        imagen = request.FILES.get('archivo')
        resultado = upload(imagen)
        url = resultado.get('secure_url')

        if imagen:
            return Response(data={
                'message':'Archivo subido exitosamente',
                'content':url
            },status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al subir archivo'
            })