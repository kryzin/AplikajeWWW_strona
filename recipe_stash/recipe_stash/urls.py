from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('markdownx/', include('markdownx.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
