from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False

# Типичный класс, определякхций модель, производный от класса Model
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Введите жанр книги', verbose_name='Жанр книги')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20, help_text='Введите язык книги', verbose_name='Язык книги')

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Введите имя автора', verbose_name='Имя автора')
    last_name = models.CharField(max_length=100, help_text='Введите фамилию автора', verbose_name='Фамилия автора')
    date_of_birth = models.DateField(verbose_name="Дaтa рождения",
                                     null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Дaтa смерти", null=True, blank=True)

    def __str__(self):
        return self.last_name

class Book(models.Model):
    title = models.CharField(max_length=200, help_text='Введите название книги', verbose_name='Название книги')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, help_text='Выберите жанр для книги',
                              verbose_name='Жанр книги', null=True)
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE,
                                 help_text='Выберите язык книги',
                                 verbose_name='Язык книги', null=True)
    author = models.ManyToManyField('Author', help_text='Выберите автора книги',
                                    verbose_name='Автор книги')
    summary = models.TextField(max_length=1000, help_text='Введите краткое описание книги',
                               verbose_name='Аннотация книги')
    isbn = models.CharField(max_length=13, help_text='Должно содержать 13 символов', verbose_name='ISBN книги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    # Функция возвращает авторов книги для отображения в админке
    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Авторы'


class Status(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name="Cтaтyc экземпляра книги")
    def __str__ (self):
        return self.name

class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                                verbose_name="Инвентарный номер")
    imprint = models.CharField(max_length=200,
                               verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               null=True,
                               verbose_name="Cтaтyc экземпляра книги")
    due_back = models.DateField(blank=True, verbose_name="Дaтa окончания статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Заказчик', help_text='Выберите заказчика книги')
    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)