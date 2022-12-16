import pytest
from django.contrib.auth.models import User, Permission
import media
from Shop_app.models import Category, Size, Color, Product, Comment, Customer, ShoppingCart, ShoppingCartItems, ShippingAdress


@pytest.fixture
def tags():
    lst = []
    for n in range(10):
        p = Category.objects.create(name=f'{n}')
        lst.append(p)
    return lst


@pytest.fixture
def color():
    lst = []
    for n in range(10):
        p = Color.objects.create(name=f'{n}')
        lst.append(p)
    return lst


@pytest.fixture
def size():
    lst = []
    for n in range(10):
        p = Size.objects.create(size=f'{n}')
        lst.append(p)
    return lst

@pytest.fixture
def product(tags, color, size):
    return Product.objects.create(name='korki',
                price=2022, sale=False, description='asd', tags=tags[0], color= color[0], available_size=size[0])