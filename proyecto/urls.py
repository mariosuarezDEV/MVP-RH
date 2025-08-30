"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("unicorn/", include("django_unicorn.urls")),
    path("martor/", include("martor.urls")),
    path("", include("base.urls")),
    path("sentry-debug/", trigger_error),
    path("incidencias/", include("incidencias.urls")),
    path("horarios/", include("horarios.urls")),
    path("empresas/", include("empresas.urls")),
    path("sucursales/", include("sucursales.urls")),
    path("puestos/", include("puestos.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
