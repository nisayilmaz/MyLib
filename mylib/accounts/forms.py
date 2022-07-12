from django import forms
from .models import User
from library.models import Library


class CreateUserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)
    library = forms.ModelChoiceField(queryset=Library.objects.all().order_by('name'), empty_label='Chose your library')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'library')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        super(CreateUserForm, self).clean()

        value_name = self.cleaned_data.get('first_name')
        value_surname = self.cleaned_data.get('last_name')
        value_password = self.cleaned_data.get('password')
        value_confirm_password = self.cleaned_data.get('password2')

        if value_password != value_confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match!'])
        if len(str(value_password).strip()) < 8:
            self._errors['password'] = self.error_class(['Password cannot be shorter than 8 digits.'])
        if len(str(value_name).strip()) < 1:
            self._errors['first_name'] = self.error_class(['Please enter your first name'])
        if len(str(value_surname).strip()) < 1:
            self._errors['last_name'] = self.error_class(['Please enter your last name'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'username': 'Username*',
            'email': 'mylib@example.com*',
            'password': 'Password*',
            'password2': 'Confirm Password*',
            'library': ''

        }

        for k in placeholders.keys():
            self.fields[k].widget.attrs.update({'class': 'form-control'})
            self.fields[k].widget.attrs.update({'placeholder': placeholders[k]})


class CreateLibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ('name', 'address', 'phone', 'image', 'email')

    def __init__(self, *args, **kwargs):
        super(CreateLibraryForm, self).__init__(*args, **kwargs)

        placeholders = {
            'name': 'Library Name',
            'phone': '0312xxxxxxx',
            'email': 'mylib@example.com*',
            'address': 'Address',


        }

        for k in placeholders.keys():
            self.fields[k].widget.attrs.update({'class': 'form-control'})
            self.fields[k].widget.attrs.update({'placeholder': placeholders[k]})

