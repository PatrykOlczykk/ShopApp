from django import forms
from django.core.exceptions import ValidationError
from Shop_app.models import Product, Comment, Color, Size, Category
from django.contrib.auth.models import User


class AddNewProductForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    available_size = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = '__all__'


class RegisterNewUserForm(forms.ModelForm):

    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Hasla nie sa takie same')


class LoginForm(forms.Form):

    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'vote']


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


class AddSizeForm(forms.ModelForm):

    class Meta:
        model = Size
        fields = ['size']


class AddColorForm(forms.ModelForm):

    class Meta:
        model = Color
        fields = ['name']
