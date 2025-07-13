# template tags used for books

from django import template

register = template.Library()

# a partial view of a single book as
# seen by the owner

# returns the book id, title and author of 'book'

# TODO: check the status of the book
# and add classes to color the book block
# and other logic?

@register.inclusion_tag('books/book_private.html', takes_context=True)
def show_book_private(context, book):
	user = context['user']
	can_request = (book.is_available and book.owner != user)
	return {
		'book_id': book.id,
		'book_title': book.title,
		'book_author': book.author,
		'summary': book.summary,
		'can_request': can_request,
		'book_is_available': book.is_available,
		'book_cover': book.cover if hasattr(book, 'cover') else None,
	}

# this tag allows the viewer to request the book/
# etc - as seen by a non-owner
@register.inclusion_tag('books/book_public.html')
def show_book_public(book):
	return {
		'book_id': book.id,
		'book_title': book.title,
		'book_author': book.author,
		'book_owner': book.owner,
		'summary' : book.summary,
	}
