from logging import error
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from sistema.models import CalificacionesModel, CursoModel
from .serializers import CalificacionesSeriealizer, RegistroSerializer, CursoSerializer

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

class UsuarioController(CreateAPIView):
    pass

class CursosController(ListCreateAPIView):

    serializer_class = CursoSerializer
    queryset = CursoModel.objects.all().order_by('docente')

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
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
                "message":None,
                "content":data.data
            })

class CursoController(RetrieveUpdateDestroyAPIView):

    serializer_class = CursoSerializer
    queryset = CursoModel.objects.all()

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
        # docente = request.query_params.get('docente')

        if semestre:
            cursosEncontrado = CursoModel.objects.filter(cursoSemestre__contains = semestre).all()

            data =  self.serializer_class(instance=cursosEncontrado, many=True)

            return Response({
                'content':data.data
            })
    
        # if docente:
        #     cursosEncontrado = CursoModel.objects.filter(docente__contains = docente).all()
        #     print(cursosEncontrado)
        #     data =  self.serializer_class(instance=cursosEncontrado, many=True)
        #     print(data)
        #     return Response({
        #         'content':data.data
        #     })
        

class CalificacionesController(CreateAPIView):
    serializer_class = CalificacionesSeriealizer
    queryset = CalificacionesModel.objects.all()

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Nota creado exitosamente',
                'content':data.data
            },status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al crear nota',
                'content':data.errors
            },status=status.HTTP_400_BAD_REQUEST)

class BuscadorCalificacionController(RetrieveAPIView):
    
    serializer_class = CursoSerializer

    def get(self,request: Request):
        
        curso = request.query_params.get('curso')

        if curso:
            calificacionesEncontradas = CursoModel.objects.filter(cursoId = curso).first()
            print(calificacionesEncontradas)
            data =  self.serializer_class(instance=calificacionesEncontradas)

            return Response({
                'content':data.data
            })