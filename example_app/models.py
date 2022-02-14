from django.db import models

# Create your models here.

#These are example models to show how forms can work
class Author(models.Model):
    first_name = models.CharField("Prénom", max_length=250, null=False, blank=False)
    last_name = models.CharField("Nom", max_length=250, null=False, blank=False)
    birth_date = models.DateField()


class Genre(models.Model):
    code = models.CharField("Code", max_length=15, null=False, blank=False)
    designation = models.CharField("Désignation", max_length=250, null=False, blank=False)
    help_text = models.CharField("Texte d'aide", max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.designation


BOOK_FORMAT=(
    ('PAPER', 'Papier'),
    ('NUM', 'Numérique'),
)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField("Titre", max_length=250, null=False, blank=False)
    number_of_pages = models.CharField("Nombre de pages", max_length=6, null=True, blank=True)
    book_format = models.CharField("Format", choices=BOOK_FORMAT, max_length=10, null=True, blank=True)
    genre = models.ManyToManyField(Genre)