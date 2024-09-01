from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Q

def book_list(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    return render(request, 'library_ap/book_list.html', {
        'books': books,
        'genres': genres,
        'publishers': publishers,
        'authors': authors
    })
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AuthorForm()
    return render(request, 'library_ap/add_author.html', {'form': form})

def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = GenreForm()
    return render(request, 'library_ap/add_genre.html', {'form': form})

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = PublisherForm()
    return render(request, 'library_ap/add_publisher.html', {'form': form})

def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library_ap/create.html', {'form': form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library_ap/edit_book.html', {'form': form, 'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library_ap/delete_book.html', {'book': book})

def search_books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).distinct()
    else:
        books = Book.objects.all()
    return render(request, 'library_ap/book_list.html', {'books': books})

def filter_books(request):
    genre = request.GET.get('genre')
    publisher = request.GET.get('publisher')
    author = request.GET.get('author')
    
    books = Book.objects.all()
    
    if genre and genre != 'All':
        books = books.filter(genre__name=genre)
    if publisher and publisher != 'All':
        books = books.filter(publisher__name=publisher)
    if author and author != 'All':
        books = books.filter(author__last_name=author)
    
    return render(request, 'library_ap/book_list.html', {'books': books})

def delete_by_filter(request):
    genre = request.GET.get('genre')
    publisher = request.GET.get('publisher')
    author = request.GET.get('author')
    
    books = Book.objects.all()
    
    if genre and genre != 'All':
        books = books.filter(genre__name=genre)
    if publisher and publisher != 'All':
        books = books.filter(publisher__name=publisher)
    if author and author != 'All':
        books = books.filter(author__last_name=author)
    
    if request.method == 'POST':
        books.delete()
        return redirect('book_list')
    
    return render(request, 'library_ap/delete_by_filter.html', {'books': books})