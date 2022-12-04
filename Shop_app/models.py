from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.size}'


class Color(models.Model):
    name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

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
        return product_score

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_product', args=(self.id,))


class Comment(models.Model):
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


class ShoppingCart(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

