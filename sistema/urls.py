from django.urls import path
from .views import RegistroController, CursosController, CursoController, CalificacionesController,BuscadorCursoController, BuscadorCalificacionController
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('registro', RegistroController.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('refresh-session', TokenRefreshView.as_view()),

    path('cursos', CursosController.as_view()),
    path('curso/<int:id>', CursoController.as_view()),
    path('buscar-curso',BuscadorCursoController.as_view()),

    path('calificaciones', CalificacionesController.as_view()),
    path('buscar-calificacion',BuscadorCalificacionController.as_view()),

]