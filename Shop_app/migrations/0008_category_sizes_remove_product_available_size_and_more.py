# Generated by Django 4.1.3 on 2022-11-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_app', '0007_remove_product_gender_alter_product_available_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='available_size',
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.IntegerField(choices=[(1, 'white'), (2, 'black'), (3, 'grey'), (4, 'brown'), (5, 'red'), (6, 'blue'), (7, 'green'), (8, 'multicolor'), (9, 'other colors')]),
        ),
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='available_size',
            field=models.ManyToManyField(to='Shop_app.sizes'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='Shop_app.category'),
        ),
    ]