from django import forms
from django.contrib.auth import password_validation
from .models import User
from library.models import Library


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    library = forms.ModelChoiceField(queryset=Library.objects.all().order_by('name'), empty_label='Chose your library',
                                     required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'library')
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        super(CreateUserForm, self).clean()

        form_first_name = self.cleaned_data.get('first_name')
        form_last_name = self.cleaned_data.get('last_name')
        form_password = self.cleaned_data.get('password')
        form_confirm_password = self.cleaned_data.get('confirm_password')
        form_email = self.cleaned_data.get('email')

        try:
            password_validation.validate_password(form_password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)

        if form_password != form_confirm_password:
            self.add_error('password', 'Passwords do not match!')
        if len(str(form_first_name).strip()) < 1:
            self.add_error('first_name', 'Please enter your first name')
        if len(str(form_last_name).strip()) < 1:
            self.add_error('last_name','Please enter your last name')
        if len(str(form_email).strip()) < 1:
            self.add_error('email', 'Please enter your email')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateLibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ('name', 'address', 'phone', 'image', 'email')

    def clean(self):
        super(CreateLibraryForm, self).clean()
        form_phone = self.cleaned_data.get('phone')
        form_name = self.cleaned_data.get('name')
        form_address = self.cleaned_data.get('address')
        form_email = self.cleaned_data.get('email')

        if len(str(form_phone).strip()) != 11 or not (str(form_phone).strip()).isdigit():
            self._errors['phone'] = self.error_class(['Please enter a valid phone number'])
        if len(str(form_name).strip()) < 1:
            self._errors['name'] = self.error_class(['Please enter name of the library'])
        if len(str(form_address).strip()) < 1:
            self._errors['address'] = self.error_class(['Please enter address of the library'])
        if len(str(form_address).strip()) < 1:
            self._errors['email'] = self.error_class(['Please enter email of the library'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CreateLibraryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ResetPasswordForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
