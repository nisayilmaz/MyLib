from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'isbn', 'info', 'image')

    def clean(self):
        super(BookForm, self).clean()
        form_isbn = self.cleaned_data.get('isbn')

        if len(str(form_isbn).strip()) != 13 or not (str(form_isbn).strip()).isdigit():
            self._errors['isbn'] = self.error_class(['Invalid ISBN'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
