# Generated by Django 4.1.3 on 2022-11-12 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='toppings',
        ),
        migrations.RemoveField(
            model_name='product',
            name='votes',
        ),
        migrations.AlterField(
            model_name='comment',
            name='vote',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=5),
        ),
    ]
