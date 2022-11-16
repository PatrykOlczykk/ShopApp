from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField


class Product(models.Model):

    tag_choices = (
        (1, 'women’s shoes'),
        (2, 'men’s shoes'),
        (3, 'unisex shoes'),
        (4, 'kids’ shoes'),
        (5, 'lifestyle'),
        (6, 'sneakers'),
        (7, 'winter shoes'),
        (8, 'dress shoes'),
        (9, 'flip-flops'),
        (10, 'sandals'),
        (11, 'running'),
        (12, 'shoes for other sports'),
        (13, 'other shoes'),
    )

    color_choices = [
        (1, 'white'),
        (2, 'black'),
        (3, 'grey'),
        (4, 'brown'),
        (5, 'red'),
        (6, 'blue'),
        (7, 'green'),
        (8, 'multicolor'),
        (9, 'other colors'),
    ]

    size_choices = (
        (1, '38'),
        (2, '39'),
        (3, '40'),
        (4, '41'),
        (5, '42'),
        (6, '43'),
        (7, '44'),
        (8, '45'),
    )

    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    sale = models.BooleanField(default=False)
    description = models.TextField()
    tags = MultiSelectField(max_length=49, max_choices=13, choices=tag_choices)
    color = models.IntegerField(choices=color_choices)
    available_size = MultiSelectField(max_length=49, max_choices=8, choices=size_choices)

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
        (5, '5'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    vote = models.IntegerField(choices=choices)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}"

class Cart(models.Model):

    name = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)