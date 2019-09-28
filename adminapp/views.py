from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'список пользователей'
        return context

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
    
#class ProductCategoryUpdateView(UpdateView):
#     model = ProductCategory
#    template_name = 'adminapp/category_update.html'
#    success_url = reverse_lazy('admin:categories')
#    form_class = ProductCategoryEditForm
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = 'категории/редактирование'
#        return context

#class ProductCategoryDeleteView(DeleteView):
#    model = ProductCategory
#    template_name = 'adminapp/category_delete.html'
#    success_url = reverse_lazy('admin:categories')
#
#    def delete(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        self.object.is_active = False
#        self.object.save()
#        return HttpResponseRedirect(self.get_success_url())
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = 'категории/удаление'
#        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    #@user_passes_test(lambda u: u.is_superuser)
#def users(request):
#    title = 'админка/пользователи'
#    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#    context = {
#        'title': title,
#        'objects': users_list,
#    }
#    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('myadmin:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {'title': title,
               'update_form': user_form,
               }
    return render(request, 'adminapp/user_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('myadmin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)
    context = {'title': title,
               'update_form': edit_form,
               }
    return render(request, 'adminapp/user_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('myadmin:users'))

    context = {'title': title,
               'user_to_delete': user,
               }

    return render(request, 'adminapp/user_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    context = {
        'title': title,
        'objects': categories_list,
    }
    return render(request, 'adminapp/categories.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('myadmin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     context = {'title': title,
#                'create_form': category_form,
#                }
#
#     return render(request, 'adminapp/category_create.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('myadmin:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#     context = {'title': title,
#                'update_form': edit_form,
#                }
#     return render(request, 'adminapp/category_update.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         # category.delete()
#         # вместо удаления лучше сделаем неактивным
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('myadmin:categories'))
#     context = {'title': title,
#                'category_to_delete': category,
#                }
#     return render(request, 'adminapp/category_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    context = {
        'title': 'админка/продукт',
        'category': category,
        'object_list': category.product_set.all(),
    }
    return render(request, 'adminapp/products.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products', kwargs={"pk":pk}))
    else:
        form = ProductEditForm(initial={'category': category})
    context = {'title': 'продукт/создание',
               'form': form,
               'category': category,
               }
    return render(request, 'adminapp/product_update.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'продукт/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {'title': title, 'object': product, }
#
#     return render(request, 'adminapp/product_read.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('myadmin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    context = {'title': 'продукт/редактирование',
               'form': edit_form,
               'category': edit_product.category,
               }
    return render(request, 'adminapp/product_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('myadmin:products',
                                            kwargs={"pk":product.category.pk}))
    context = {'title': 'продукт/удаление',
               'object': product,
               }
    return render(request, 'adminapp/product_delete.html', context)

