from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from Shop_app.models import Product, Comment, Category, Size, Color, ShippingAdress, ShoppingCartItems, ShoppingCart
from Shop_app.forms import AddNewProductForm, RegisterNewUserForm, LoginForm, AddCommentForm, AddSizeForm, AddColorForm, AddCategoryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
import json

def is_valid_queryparm(parm):
    return parm != '' and parm is not None


class ShowAllProductsView(View):
    def get(self, request):

        qs = Product.objects.order_by('name')
        categories = Category.objects.all()
        sizes = Size.objects.all()
        colors = Color.objects.all()


        name_contains_query = request.GET.get('name_contains')
        description_contains_query = request.GET.get('description_contains')
        price_count_max = request.GET.get('PriceMax')
        price_count_min = request.GET.get('PriceMin')
        category = request.GET.get('Category')
        size = request.GET.get('Size')
        color = request.GET.get('Color')
        sort_value = request.GET.get('Sort')


        if is_valid_queryparm(name_contains_query):
            qs = qs.filter(name__icontains=name_contains_query)

        if is_valid_queryparm(description_contains_query):
            qs = qs.filter(name__icontains=description_contains_query)

        if is_valid_queryparm(price_count_max):
            qs = qs.filter(price__lt=price_count_max)

        if is_valid_queryparm(price_count_min):
            qs = qs.filter(price__gte=price_count_min)

        if is_valid_queryparm(category) and category != 'Choose...':
            qs = qs.filter(tags__name=category)

        if is_valid_queryparm(size) and size != 'Choose...':
            qs = qs.filter(available_size=size)

        if is_valid_queryparm(color) and color != 'Choose...':
            qs = qs.filter(color__name=color)

        if is_valid_queryparm(sort_value) and sort_value == 'ATOZ':
            qs = qs.order_by('name')

        if is_valid_queryparm(sort_value) and sort_value == 'ZTOA':
            qs = qs.order_by('-name')



        p = Paginator(qs, 4)
        page = request.GET.get('page')
        paginator = p.get_page(page)


        context = {
            'queryset': qs,
            'paginator': paginator,
            'categories': categories,
            'sizes': sizes,
            'colors': colors,
        }

        return render(request, 'show_all_products.html', context)


class AddProduct(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request):
        form = AddNewProductForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddNewProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'form.html', {'form': form})


class RegisterUserView(View):

    def get(self, request):
        form = RegisterNewUserForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.set_password(form.cleaned_data['password'])
            u.save()
            return redirect('/')
        return render(request, 'form.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            message = 'niepoprawne haslo lub/i login'
            return render(request, 'form.html', {'form': form, 'message': message})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class AddCommentView(View):

    def post(self, request, pk):
        form = AddCommentForm(request.POST)
        product = Product.objects.get(pk=pk)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect('detail_product', pk)
            else:
                return redirect('login')


class ShowDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        form = AddCommentForm()
        comments = Comment.objects.filter(product=product)
        product_score = 0
        for comment in comments:
            product_score += comment.vote
        if product_score != 0:
            product_score = product_score/comments.count()
        return render(request, 'detail_product.html', {'product': product, 'form': form, 'product_score': product_score})


class DelateProductView(PermissionRequiredMixin, View):
    permission_required = ('Shop_app.delate_product')

    def get(self, request, pk):
        return redirect(f'/confirm_delate_product/{pk}')


class ConfirmDelateProductView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.delate_product']

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'confirm_delate_product.html', {'product': product})

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('/')


class DelateCommentView(View):

    def get(self, request, pk):
        return redirect(f'/confirm_delate_comment/{pk}')


class ConfirmDelateCommentView(View):

    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if request.user == comment.author:
            product = Product.objects.get(comment=comment)
            return render(request, 'confirm_delate_comment.html', {'comment': comment, 'product': product})
        else:
            return redirect('/')

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        product = Product.objects.get(comment=comment)
        return redirect(f'/detail_product/{product.pk}')

class EditProductView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = AddNewProductForm()
        message = f"You're editing {product}"
        return render(request, 'form.html', {'message': message, 'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = AddNewProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(f'/detail_product/{product.pk}')

class ShowShoppingCartView(View):
    def get(self, request):
        products = Product.objects.order_by('name')
        user = request.User
        return render(request, 'shopping_cart.html', {'products': products})

class AboutMeView(View):

    def get(self, request):
        return render(request, 'about_me.html')

class AddView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request):
        category = Category.objects.order_by('name')
        size = Size.objects.order_by('size')
        color = Color.objects.order_by('name')
        return render(request, 'admin_panel.html', {'category': category, 'size': size, 'color': color})


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request):
        form = AddCategoryForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        return render(request, 'form.html', {'form': form})


class AddColorView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request):
        form = AddColorForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        return render(request, 'form.html', {'form': form})


class AddSizeView(PermissionRequiredMixin, View):
    permission_required = ['Shop_app.add_product']

    def get(self, request):
        form = AddSizeForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        return render(request, 'form.html', {'form': form})

class ShowShoppingCartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user. customer
            shoppingCart, created = ShoppingCart.objects.get_or_create(customer=customer, completed=False)
            items = shoppingCart.shoppingcartitems_set.all()
        else:
            items = []
        return render(request, 'shopping_cart.html', {'items': items})

class UpdateCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action', action)
        print('productId', productId)

        customer = request.user.customer
        product = Product.objects.get(id=productId)

        shoppingCart, created = ShoppingCart.objects.get_or_create(customer=customer, completed=False)
        shoppingCartItem, created = ShoppingCartItems.objects.get_or_create(cart=shoppingCart, product=product)

        if action == 'add':
            shoppingCartItem.quantity += 1
            shoppingCartItem.save()

        return JsonResponse('Item added', safe=False)