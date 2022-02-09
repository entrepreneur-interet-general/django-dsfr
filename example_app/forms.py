from django.forms import ModelForm, inlineformset_factory
from django import forms

from .models import Author, Book

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field

class AuthorCreateForm(ModelForm):
    class Meta:
        model = Author
        exclude = []
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'birth_date': forms.DateInput(attrs={'type':'date',}),
        }

#Prévenir pour le help text ici
BOOK_FORMAT=(
    ('PAPER', 'Papier'),
    ('NUM', {'label':'Numérique', 'help_text':'Livre électronique'}),
)

class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        exclude=[]
        widgets = {
            'title': forms.TextInput(),
            'number_of_pages': forms.NumberInput(),
            # 'book_format': forms.RadioSelect(attrs={'class':'fr-fieldset--inline'})
        }
    book_format = forms.ChoiceField(
        label="Format",
        choices=BOOK_FORMAT,
        widget=forms.RadioSelect(attrs={'class':'fr-fieldset--inline'}),
        )
    def clean(self):
        cleaned_data = super().clean()
        print(self.data)
        return cleaned_data



class BookCreateFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(BookCreateFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Fieldset("Ajouter un livre", 
                     Field('title'),
                     Field('number_of_pages'),
                     Field('book_format')),
        )
        
BookCreateFormSet = inlineformset_factory(
    Author,
    Book,
    form=BookCreateForm,
    extra=1,
    exclude=[],
)