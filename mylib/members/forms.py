from django import forms
from django.forms import ModelForm
from .models import User


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class CreateLibraryForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'library_address', 'email', 'phone', 'password')

    def __init__(self, *args, **kwargs):
        super(CreateLibraryForm, self).__init__(*args, **kwargs)

        placeholders = {
            'username': 'Library Name',
            'library_address': 'Address',
            'email': 'Email',
            'phone': 'Phone Number',
            'password': 'Password'
        }
        for k in placeholders.keys():
            self.fields[k].widget.attrs.update({'class': 'form-control'})
            self.fields[k].widget.attrs.update({'placeholder': placeholders[k]})
