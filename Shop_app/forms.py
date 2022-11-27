from django import forms
from django.core.exceptions import ValidationError
from Shop_app.models import Product, Comment, Colors, Sizes, Categories
from django.contrib.auth.models import User


class AddNewProductForm(forms.ModelForm):
    # name = forms.CharField(max_length=64)
    # price = forms.DecimalField(max_digits=999, decimal_places=2)
    # sale = forms.BooleanField()
    # description = forms.Textarea()
    # tags = forms.ChoiceField(Categories)
    # color = forms.ChoiceField(Colors)
    # available_size = forms.ChoiceField(Sizes)
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