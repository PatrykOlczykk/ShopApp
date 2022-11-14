from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    sale = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('detail_product', args=(self.id,))


class Comment(models.Model):
    choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(choices=choices)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}"