"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import mainapp.views as mainapp
import authapp.views as authapp
import basketapp.views as basketapp
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('product/<int:pk>', mainapp.product, name='product'),
    path('catalog/', mainapp.catalog, name='catalog'),
    path('products/', mainapp.products, name='products'),
    path('products/page/<int:page>/', mainapp.products, name='page'),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('strollers/', mainapp.strollers, name='strollers'),
    path('chears/', mainapp.chears, name='chears'),
    path('carseats/', mainapp.carseats, name='carseats'),
    path('black_grey/', mainapp.black_grey, name='black_grey'),
    path('black_red/', mainapp.black_red, name='black_red'),
    path('black_stars/', mainapp.black_stars, name='black_stars'),
    path('admin/', admin.site.urls),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('basket/', basketapp.basket, name='basket'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
    path('basket/edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit'),
    path('myadmin/', include('adminapp.urls', namespace='myadmin')),
    path('auth', include('authapp.urls', namespace='auth')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order')),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)