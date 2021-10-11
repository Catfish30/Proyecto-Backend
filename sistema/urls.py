from django.urls import path
from .views import RegistroController, CursosController, CursoController
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('registro', RegistroController.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('refresh-session', TokenRefreshView.as_view()),

    path('cursos', CursosController.as_view()),
    path('curso/<int:id>', CursoController.as_view())
]