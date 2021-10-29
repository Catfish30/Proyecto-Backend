
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework import schemas
# from rest_framework_swagger.views import get_swagger_view

# schemas_view = get_swagger_view(title='Proyecto G9')


# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Proyecto G9 API",
#         default_version='v1',
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('doc/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('sistema/', include('sistema.urls')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

