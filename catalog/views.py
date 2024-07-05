from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Book, Author, BookInstance, Genre, Language
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  num_authors = Author.objects.count()
  num_genres = Genre.objects.count()
  num_languages = Language.objects.count()
  num_books_with_word = Book.objects.filter(title__icontains='war').count()

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genres': num_genres,
    'num_languages': num_languages,
    'num_books_with_word': num_books_with_word
  }

  return render(request, 'catalog/index.html', context=context)

class BookCreate(LoginRequiredMixin ,CreateView):
  model = Book
  fields = '__all__'
  
class BookDetail(DetailView):
  model = Book
  
@login_required
def my_view(request):
  return render(request, 'catalog/my_view.html')

class SignupView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'catalog/signup.html'
  
class CheckedOutBooksByUserView(LoginRequiredMixin, ListView):
  model = BookInstance
  template_name = 'catalog/profile.html'
  paginate_by = 5

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user)  