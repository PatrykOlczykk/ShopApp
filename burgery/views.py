from django.shortcuts import render, redirect
from django.views import View
from burgery.models import Product
from burgery.forms import AddNewProductForm, RegisterNewUserForm, LoginForm, AddCommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ShowAllProducts(View):
    def get(self, request):
        product = Product.objects.all()
        return render(request, 'ShowAllBurgers.html', {'product': product})

class AddProduct(View):

    def get(self,request):
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
    def post(self,request):
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
        return render (request, 'form.html',{'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ''
        if form.is_valid():
            username= form.cleaned_data['username']
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

    def post(self, request, product_pk):
        form = AddCommentForm(request.POST)
        product = Product.objects.get(pk=product_pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            return redirect('detail_product', product_pk)

class ShowDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        comments = product.comment_set.filter(author=request.user)
        form = AddCommentForm()
        return render(request, 'detail_product.html', {'product': product, 'form': form})