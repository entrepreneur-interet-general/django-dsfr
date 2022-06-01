#/!\ In order to use formsets
from django.forms import ModelForm, inlineformset_factory
from django import forms

from .models import Author, Book, Genre

#/!\ In order to use formsets
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


#If you need to define help_text for one radio button or checkbox in particular, you can do it in a dict {'label':...., 'help_text':....}
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
        }
    #/!\ You have to redefine each radio button or checkboxes field like so :
    book_format = forms.ChoiceField(
        label="Format",
        choices=BOOK_FORMAT, #If the choices are in a constant
        widget=forms.RadioSelect(attrs={'class':'fr-fieldset--inline'}),
    )
    genre = forms.ModelMultipleChoiceField(
        label="Genre",
        queryset=Genre.objects.all(), #If the choices are related to a model
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

#/!\ In order to use formsets, you have to define a crispy FormHelper for the form used for the formset
class BookCreateFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(BookCreateFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Fieldset("Ajouter un livre", 
                     Field('title'),
                     Field('number_of_pages'),
                     Field('book_format'),
                     Field('genre'),),
        )

#/!\ In order to use formsets, you have to define a formset factory
BookCreateFormSet = inlineformset_factory(
    Author,
    Book,
    form=BookCreateForm,
    extra=1,
    exclude=[],
)