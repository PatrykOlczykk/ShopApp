import pytest
from django.test import Client
from django.urls import reverse
from Shop_app.conftest import *
from Shop_app.models import Category, Size, Color, Product, Comment, Customer, ShoppingCart, ShoppingCartItems, ShippingAdress
from Shop_app.forms import AddNewProductForm, RegisterNewUserForm, LoginForm, AddCommentForm, AddSizeForm, AddColorForm, AddCategoryForm

from django.contrib.auth.models import User

client = Client()

@pytest.mark.django_db
def test_login_get():
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_form_post_correct():
    User.objects.create_user(username='someText', password='someText')
    url = reverse('login')
    response = client.post(url, {'username': 'someText', 'password': 'someText'})
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_form_pos_incorrect():
    User.objects.create_user(username='someText', password='someText')
    url = reverse('login')
    response = client.post(url, {'username': 'someText2', 'password': 'someText2'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_get():
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_register_post_correct():
    url = reverse('register')
    response = client.post(url, {'username': 'someText', 'password': 'someText', 'confirm_password':'someText'})
    assert response.status_code == 302
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_register_post_incorrect():
    url = reverse('register')
    response = client.post(url, {'username': 'someText', 'password': 'someText', 'confirm_password':'someText2'})
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_main_view():
    url = reverse('show_all_products')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_product_get_without_permission(admin_client):
    url = reverse('add_product')
    response = admin_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_product_get_with_permission():
    url = reverse('add_product')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_product_post(admin_client):
    url = reverse('add_product')
    data = {
        'name': 'someText',
        'price': 99,
        "description": 'someText',
        'tags': tags,
        'color': color,
        'available_size': size
    }
    response = admin_client.post(url, data)
    assert response.status_code == 200
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_detail_product_get(product_item):
    url = reverse('detail_product', args=(product_item.id,))
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_comment_with_permission(admin_client, product_item):
    url = reverse('add_comment', args=(product_item.id,))
    data = {
        'text': 'someText',
        'vote': 1
    }
    response = admin_client.post(url, data)
    assert response.status_code == 302
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_add_comment_without_permission(product_item):
    client = Client()
    url = reverse('add_comment', args=(product_item.id,))
    data = {
        'text': 'someText',
        'vote': 1
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_delate_product_get_with_permission(admin_client, product_item):
    url = reverse('delate_product', args=(product_item.id,))
    response = admin_client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_delate_product_get_without_permission(product_item):
    url = reverse('delate_product', args=(product_item.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_confirm_delate_product_get_without_permission(product_item):
    url = reverse('confirm_delate_product', args=(product_item.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_confirm_delate_product_get_with_permission(admin_client, product_item):
    url = reverse('confirm_delate_product', args=(product_item.id,))
    response = admin_client.get(url)
    assert response.status_code == 200
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_confirm_delate_product_post_without_permission(product_item):
    url = reverse('confirm_delate_product', args=(product_item.id,))
    response = client.post(url)
    assert response.status_code == 302
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_confirm_delate_product_post_without_permission(admin_client, product_item):
    url = reverse('confirm_delate_product', args=(product_item.id,))
    response = admin_client.post(url)
    assert response.status_code == 302
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_confirm_delate_comment_get_with_permission(author_comment, comment):
    url = reverse('confirm_delate_comment', args=(comment.id,))
    client.force_login(author_comment)
    response = client.get(url)
    assert response.status_code == 200
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_confirm_delate_comment_get_without_permission(user, comment):
    client.force_login(user)
    url = reverse('confirm_delate_comment', args=(comment.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_confirm_delate_comment_post_with_permission(author_comment, comment):
    url = reverse('confirm_delate_comment', args=(comment.id,))
    client.force_login(author_comment)
    response = client.post(url)
    assert response.status_code == 302
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_confirm_delate_comment_post_without_permission(user, comment):
    client.force_login(user)
    url = reverse('confirm_delate_comment', args=(comment.id,))
    response = client.post(url)
    assert response.status_code == 302
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_edit_product_get_with_permission(product_item):
    url = reverse('edit_product', args=(product_item.id,))
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_edit_product_get_with_permission(admin_client, product_item):
    url = reverse('edit_product', args=(product_item.id,))
    response = admin_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_edit_product_post_without_permission(product_item):
    url = reverse('edit_product', args=(product_item.id,))
    data = {
        'name': 'someText',
        'price': 99,
        "description": 'someText',
        'tags': tags,
        'color': color,
        'available_size': size
    }
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_edit_product_post_with_permission(admin_client, product_item):
    url = reverse('edit_product', args=(product_item.id,))
    data = {
        'name': 'someText',
        'price': 99,
        "description": 'someText',
        'tags': tags,
        'color': color,
        'available_size': size
    }
    response = admin_client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_shopping_cart_get():
    url = reverse('shopping_cart')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_show_shopping_cart():
    url = reverse('shopping_cart')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_about_me():
    url = reverse('about_me')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_admin_panel_without_permission(user):
    client.force_login(user)
    url = reverse('admin_panel')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_panel_with_permission(admin_client):
    url = reverse('admin_panel')
    response = admin_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_category_get_without_permission():
    url = reverse('add_category')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_category_get_with_permission(admin_client):
    url = reverse('add_category')
    response = admin_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_category_post_without_permission():
    url = reverse('add_category')
    response = client.post(url, {'name': 'someText'})
    assert response.status_code == 302
    assert Category.objects.count() == 0

@pytest.mark.django_db
def test_add_category_post_with_permission_correct(admin_client):
    url = reverse('add_category')
    response = admin_client.post(url, {'name': 'someText'})
    assert response.status_code == 302
    assert Category.objects.count() == 1
    assert Category.objects.get(name='someText')

@pytest.mark.django_db
def test_add_category_post_with_permission_incorrect(admin_client):
    url = reverse('add_category')
    response = admin_client.post(url, {'name': False})
    assert response.status_code == 200
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_add_size_get_without_permission():
    url = reverse('add_size')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_size_get_with_permission(admin_client):
    url = reverse('add_size')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_size_post_without_permission():
    url = reverse('add_size')
    response = client.post(url, {'size': 99})
    assert response.status_code == 302
    assert Size.objects.count() == 0


@pytest.mark.django_db
def test_add_category_post_with_permission_correct(admin_client):
    url = reverse('add_size')
    response = admin_client.post(url, {'size': 99})
    assert response.status_code == 302
    assert Size.objects.count() == 1
    assert Size.objects.get(size=99)

@pytest.mark.django_db
def test_add_category_post_with_permission_incorrect(admin_client):
    url = reverse('add_size')
    response = admin_client.post(url, {'size': False})
    assert response.status_code == 200
    assert Size.objects.count() == 0

@pytest.mark.django_db
def test_add_color_get_without_permission():
    url = reverse('add_color')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_color_get_with_permission(admin_client):
    url = reverse('add_color')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_color_post_without_permission():
    url = reverse('add_color')
    response = client.post(url, {'name': 'someText'})
    assert response.status_code == 302
    assert Color.objects.count() == 0


@pytest.mark.django_db
def test_add_color_post_with_permission_correct(admin_client):
    url = reverse('add_color')
    response = admin_client.post(url, {'name': 'someText'})
    assert response.status_code == 302
    assert Color.objects.count() == 1
    assert Color.objects.get(name='someText')

@pytest.mark.django_db
def test_add_category_post_with_permission_incorrect(admin_client):
    url = reverse('add_color')
    response = admin_client.post(url, {'size': False})
    assert response.status_code == 200
    assert Color.objects.count() == 0
