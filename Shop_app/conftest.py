import pytest
from django.contrib.auth.models import User, Permission
import media
from Shop_app.models import Category, Size, Color, Product, Comment, Customer, ShoppingCart, ShoppingCartItems, ShippingAdress


@pytest.fixture
def tags():
    # lst = []
    # for n in range(10):
    #     p = Category.objects.create(name=f'{n}')
    #     lst.append(p)
    # print(lst)
    # return lst
    t = Category.objects.create(name='someText')
    return t


@pytest.fixture
def color():
    c = Color.objects.create(name='someText')
    return c

@pytest.fixture
def size2():
    s = Size.objects.create(size=22)
    return s

@pytest.fixture
def size():
    s = Size.objects.create(size=22)
    return s

@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client

@pytest.fixture
def product_item(size, color, tags):
    product = Product.objects.create(name='someText', price=99, sale=True, description='someText', color=color)
    return product

@pytest.fixture
def user():
    u = User.objects.create(username='user')
    return u

@pytest.fixture
def author_comment():
    author_comment = User.objects.create(username='someText')
    return author_comment

@pytest.fixture
def super_user():
    su = User.objects.create(username='superUser', is_superuser=True)
    return su

@pytest.fixture
def comment(author_comment, product_item):
    comment = Comment.objects.create(text='someText', author=author_comment, vote=5, product=product_item)
    return comment