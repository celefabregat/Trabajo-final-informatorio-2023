"""
URL configuration for INFO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import index
from apps.post import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name= "index"),
    path("Acerca de nosotros", views.acerca_de, name="acerca_de_nosotros"),
    path("", include("apps.post.urls")),
    path("", include("apps.contacto.urls")),
    path("", include("apps.usuario.urls")),
    path("", include("django.contrib.auth.urls")),
]+static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)


# path(): sirve para indicarle a Django la ruta url que va a
# usar al momento de generar una respuesta a una
# solicitud HTTP.
# '': las comillas simples, sin nada adentro, significa que
# cuando se acceda a la página principal o inicial (como lo
# dijimos en el ejemplo de la página de oficina de empleo)
# va a mostrar el archivo html al que hacemos referencia
# (el que vamos a crear en el siguiente paso) que en este
# caso, va a ser el archivo index.html definido en nuestra
# views.py. Si por el contrario, quisieramos definir,
# supongamos la página de "contacto" (la cual veremos al
# avanzar más en el curso), deberemos colocar "contacto"
# dentro de éstas comillas simples.
# index: hace referencia al nombre de la función que
# creamos en el archivo views.py y que importamos en
# este archivo para poder usar.
# name='index': nos servirá para hacer referencia a la
# página index, cuando incrustemos código Django en
# nuestros archivos html.
