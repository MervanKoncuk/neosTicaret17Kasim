"""neosTicaret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from urunler.views import *
from user.views import *

# media klasörü için gerekli importlar
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('urun/<int:urunId>', urun, name='urun'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),
    path('olustur/', olustur, name='olustur'),
    path('sepet/', sepet, name='sepet'),
    path('odeme/', payment, name='payment'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('fail/', fail, name='failure')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) \
 + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# media klasöründeki resimlerin sayfamızda görüntülenebilmesi için
