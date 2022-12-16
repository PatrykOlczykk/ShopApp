import pytest
from django.test import Client
from django.urls import reverse

from Shop_app.models import Category, Size, Color, Product, Comment, Customer, ShoppingCart, ShoppingCartItems, ShippingAdress
from Shop_app.forms import AddNewProductForm, RegisterNewUserForm, LoginForm, AddCommentForm, AddSizeForm, AddColorForm, AddCategoryForm

from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user("mama")
    assert user.objects.get(username='mama')


@pytest.mark.django_db
def test_main_view():
    client = Client()
    url = reverse('show_all_products')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_product_get():
    client = Client()
    url = reverse('add_product')
    response = client.get(url)
    assert response.status_code == 302

# @pytest.mark.django_db
# def test_add_product_post(tags, color, size):
# client = Client()
#     data = {
#         'name': 'kozaki',
#         'price': 22,
#         'sale': True,
#         'description': 'nice shoes',
#         'tags': tags[0],
#         'color': color[0],
#         'available_size': size[0]
#     }
#     url = reverse('add_product')
#     response = client.post(url, data)
#     assert response.status_code == 302
#     assert Product.objects.get(name='kozaki')


@pytest.mark.django_db
def test_add_product_post(product):
    client = Client()
    url = reverse('add_product')
    response = client.post(url, product)
    assert response.status_code == 302
    assert Product.objects.get(name='korki')


# @pytest.mark.django_db
# def test_detail_product_get(product, id):
#     return True

@pytest.mark.django_db
def test_shopping_cart_get():
    client = Client()
    url = reverse('shopping_cart')
    response = client.post(url)
    assert response.status_code == 405

@pytest.mark.django_db
def test_add_size_get():
    client = Client()
    url = reverse('add_size')
    response = client.post(url)
    assert response.status_code == 302
    assert isinstance(response.context['form'], AddSizeForm)


@pytest.mark.django_db
def test_add_size_post_valid():
    client = Client()
    url = reverse('add_size')
    data = {
            'size': 12
        }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Size.objects.count() == 1
    assert Size.objects.get(**data)










@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user("mama")
    assert user.username == "mama"


# Create your tests here.
