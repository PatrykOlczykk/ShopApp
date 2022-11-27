"""Shop URL Configuration

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
from Shop_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowAllProducts.as_view(), name='show_all_products'),
    path('add_product/', views.AddProduct.as_view(), name='add_product'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('detail_product/<int:pk>/', views.ShowDetailView.as_view(), name='detail_product'),
    path('add_comment/<int:pk>/', views.AddCommentView.as_view(), name='add_comment'),
    path('delate_product/<int:pk>/', views.DelateProductView.as_view(), name='delate_product'),
    path('confirm_delate_product/<int:pk>/', views.ConfirmDelateProductView.as_view(), name='confirm_delate_product'),
    path('delate_product/<int:pk>/', views.DelateCommentView.as_view(), name='delate_comment'),
    path('confirm_delate_comment/<int:pk>/', views.ConfirmDelateComment.as_view(), name='confirm_delate_comment'),
    path('edit_product/<int:pk>', views.EditProduct.as_view(), name='edit_product'),
    path('my_shoppingcart/<int:pk>', views.ShowShoppingCart.as_view(), name='show_shoppingcart'),
    path('about_me/', views.AboutMe.as_view(), name='about_me'),
    path('add/', views.Add.as_view(), name='add'),
    path('add_category/', views.AddCategory.as_view(), name='add_category'),
    path('add_color/', views.AddColor.as_view(), name='add_color'),
    path('add_size/', views.AddSize.as_view(), name='add_size'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
