from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from Shop.models import Product, Comment
from Shop.forms import AddNewProductForm, RegisterNewUserForm, LoginForm, AddCommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ShowAllProducts(View):
    def get(self, request):
        product = Product.objects.all()
        return render(request, 'Show_All_Products.html', {'product': product})


class AddProduct(PermissionRequiredMixin, View):
    permission_required = ['Shop.add_product']

    def get(self, request):
        form = AddNewProductForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddNewProductForm(request.POST)
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
            return redirect('index')
        return render(request, 'form.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render (request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ''
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            message = 'niepoprawne haslo lub/i login'
            return render(request, 'form.html', {'form': form, 'message': message})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


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
        if product_score != 0 :
            product_score = product_score/comments.count()
        return render(request, 'detail_product.html', {'product': product, 'form': form, 'product_score': product_score})


class DelateProductView(PermissionRequiredMixin, View):
    permission_required = ('Shop.delate_product')

    def get(self, request, pk):
        return redirect(f'/confirm_delate_product/{pk}')


class ConfirmDelateProductView(PermissionRequiredMixin, View):
    permission_required = ['Shop.delate_product']

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'confirm_delate_product.html', {'product': product})

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('show_all_products')


class DelateCommentView(View):

    def get(self, request, pk):
        return redirect(f'/confirm_delate_comment/{pk}')


class ConfirmDelateComment(View):

    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if request.user == comment.author:
            product = Product.objects.get(comment=comment)
            return render(request, 'confirm_delate_comment.html', {'comment': comment, 'product': product})
        else:
            return redirect('index')

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        product = Product.objects.get(comment=comment)
        return redirect(f'/detail_product/{product.pk}')

class EditProduct(PermissionRequiredMixin, View):
    permission_required = ['Shop.add_product']

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




