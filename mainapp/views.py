import datetime
import random
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product
from mainapp.models import ProductCategory
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def main(request):
    context = {
       'page_title':'главная',
        'date':datetime.datetime.now(),
    }
    return render(request, 'mainapp/index.html', context)

def catalog(request):
    context = {
        'page_title': 'каталог',
    }
    return render(request, 'mainapp/catalog.html', context)


def product(request, pk):
    context = {
        'title': 'продукты',
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', context)

def products(request, page=1):
    products_list = Product.objects.filter(is_active=True).order_by('price')
    paginator = Paginator(products_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'продукты',
        'products_list': products_paginator,
    }
    return render(request, 'mainapp/products_list.html', context)

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]
    return same_products


def contacts(request):
    location = {
        'phone': '89513385409',
        'adress': 'г. Курск, ул. К. Маркса 65а',
        'email': 'ArKooot@mail.ru',
        'work': 'Пн-Вс, с 10.00 до 20.00',
    }
    context = {
        'page_title': 'контакты',
        'location': location,
    }
    return render(request, 'mainapp/contacts.html', context)

def strollers(request):
    products = Product.objects.all()
    context = {
        'page_title': 'прогулочные коляски',
        'product': products,
    }
    return render(request, 'mainapp/categories/Strollers.html', context)

def chears(request):
    context = {
        'page_title': 'стульчики для кормления',
    }
    return render(request, 'mainapp/categories/Chears.html', context)

def carseats(request):
    context = {
        'page_title': 'автокресла',
    }
    return render(request, 'mainapp/categories/Carseats.html', context)

def black_grey(request):
    context = {
        'title': 'yoya plus 3 серая на черной раме',
    }
    return render(request, 'mainapp/products/Black_grey.html', context)

def black_red(request):
    context = {
        'title': 'yoya plus 3 красная на черной раме',
    }
    return render(request, 'mainapp/products/Black_red.html', context)

def black_stars(request):
    context = {
        'title': 'yoya plus 3 звезды на черной раме',
    }
    return render(request, 'mainapp/products/Black_stars.html', context)

def get_basket(request):
    if request.user.is_authenticated:
        return  Basket.objects.all().order_by('product__category')
    else:
        return []