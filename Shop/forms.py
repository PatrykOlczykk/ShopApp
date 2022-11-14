from django import forms
from django.core.exceptions import ValidationError
from Shop.models import Product, Comment
from django.contrib.auth.models import User


class AddNewProductForm(forms.ModelForm):
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