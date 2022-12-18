from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):

    """This model is a category for the product"""

    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):

    """This model is an available size for the product"""

    size = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.size}'


class Color(models.Model):

    """This model is a color for the product"""

    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    """This is a base product-model."""

    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    sale = models.BooleanField(default=False)
    description = models.TextField()
    tags = models.ManyToManyField(Category)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    available_size = models.ManyToManyField(Size)
    product_image = models.ImageField(null=True, blank=True, upload_to='images/')
#django orm Count, Sum
    @property
    def score(self):
        #self.commet_set.all()
        comments = Comment.objects.filter(product=self)
        product_score = 0
        for comment in comments:
            product_score += comment.vote
        if product_score != 0:
            product_score = product_score/comments.count()
        return round(product_score, 2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_product', args=(self.id,))


class Comment(models.Model):

    """This model is a comment for the product"""

    choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(choices=choices)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.author


class Customer(models.Model):

    """This is a customer model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=64, null=True)


class ShoppingCart(models.Model):

    """This is a cart-model"""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class ShoppingCartItems(models.Model):

    """This is a shopping cart model"""

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class ShippingAddress(models.Model):

    """This is the shipping address model"""

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(ShoppingCart, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=64, null=False)
    city = models.CharField(max_length=64, null=False)
    zipcode = models.CharField(max_length=64, null=False)

