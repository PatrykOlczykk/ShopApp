# Generated by Django 4.1.3 on 2022-11-17 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop_app', '0008_category_sizes_remove_product_available_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=24)),
            ],
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='Categories',
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop_app.colors'),
        ),
    ]