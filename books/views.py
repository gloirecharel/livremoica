from django.contrib.auth.decorators import login_required
# Vue pour afficher tous les livres et leurs états
@login_required
def all_books(request):
    books = Book.objects.select_related('owner').all().order_by('title')
    return render(request, 'books/all_books.html', {'books': books})
from django.shortcuts import render, get_object_or_404
from django.urls import reverse  # 🔄 remplacé urlresolvers
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect

from books.models import Book
from bookrequests.models import BookRequest

from .forms import EditBookForm

from django.db.models import Q  # 🔍 pour la recherche


@login_required
def index(request):
    user = request.user
    book_list = user.books.all()

    return render(request, 'books/index.html', {
        'book_list': book_list
    })


@login_required
def add_book(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get("title")
        author = request.POST.get("author")
        summary = request.POST.get('summary')
        cover = request.FILES.get('cover')  # Ajout gestion image

        new_book = Book(owner=user, title=title, author=author, summary=summary, cover=cover)
        new_book.save()

        messages.success(request, 'Ajout du livre réussi !')
        return HttpResponseRedirect(reverse("users:books:index"))
    else:
        return render(request, 'books/add_book.html')


@login_required
def edit_book(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)

    if book not in user.books.all():
        return HttpResponseRedirect(reverse("users:home"))

    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES)

        if form.is_valid():
            book.title = form.cleaned_data['title']
            book.author = form.cleaned_data['author']
            book.summary = form.cleaned_data['summary']
            if form.cleaned_data.get('cover'):
                book.cover = form.cleaned_data['cover']
            book.save()
            messages.success(request, 'Updated your book successfully')
        return HttpResponseRedirect(reverse("users:books:index"))
    else:
        form = EditBookForm({
            'title': book.title,
            'author': book.author,
            'summary': book.summary
        })
        # Affichage de l'image actuelle (optionnel, à gérer dans le template si besoin)
        return render(request, 'books/edit_book.html', {
            'form': form,
            'book_id': book_id,
            'book_cover': book.cover if book.cover else None
        })


@login_required
def delete(request, id):
    book = get_object_or_404(Book, pk=id)

    requests = BookRequest.objects.filter(book=book).exclude(
        Q(status=BookRequest.REQUEST_REJECTED) |
        Q(status=BookRequest.RETURNED)
    )

    if requests.exists():
        messages.warning(request, 'There are pending requests for this book, you cannot delete it')
    elif book.owner == request.user:
        book.delete()
        messages.success(request, 'Deleted your book successfully')
    else:
        messages.warning(request, 'Could not delete this book')

    return HttpResponseRedirect(reverse("users:books:index"))


@login_required
def search(request):
    if request.method == 'POST':
        query_string = request.POST.get('query')
        results = Book.objects.filter(
            Q(title__icontains=query_string) |
            Q(author__icontains=query_string) |
            Q(summary__icontains=query_string)
        ).exclude(owner=request.user)

        return render(request, 'books/search.html', {
            'results': results
        })
    else:
        return HttpResponseRedirect(reverse("users:books:index"))



from datetime import timedelta
from django.utils import timezone

@login_required
def make_request(request, id):
    book_obj = get_object_or_404(Book, pk=id)
    # Vérifier la disponibilité
    book_obj.check_availability()
    if not book_obj.is_available:
        messages.warning(request, "Ce livre est actuellement indisponible jusqu'au {}.".format(book_obj.unavailable_until))
        return HttpResponseRedirect(reverse("users:books:index"))

    # Définir la date de retour prévue (exemple : 14 jours)
    duree_emprunt = 14
    date_retour = timezone.now().date() + timedelta(days=duree_emprunt)

    new_request = BookRequest(
        book=book_obj,
        borrower=request.user,
        status=BookRequest.REQUEST_MADE,
        due_date=date_retour
    )
    new_request.save()

    messages.success(request, f'Vous avez demandé ce livre avec succès. Il sera disponible à nouveau le {date_retour}.')

    return HttpResponseRedirect(reverse("users:books:index"))
