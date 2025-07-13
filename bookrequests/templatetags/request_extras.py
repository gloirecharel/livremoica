# template tags used for book requests

from bookrequests.models import BookRequest

from django.db.models import Q

from django import template

register = template.Library()

# request tracking by the owner of a book
# 1. accept/reject request
# 2. pending pickup
# 3. with courier, going to borrower
# 4. with borrower
# 5. borrower finished reading
# 6. with courier, coming back
# 7. completed

@register.inclusion_tag('bookrequests/request_owner.html')
def show_request_owner(req):
	borrower = str(req.borrower)
	title = str(req.book.title)
	author = str(req.book.author)

	messages = {
		BookRequest.REQUEST_MADE:
			 "{0} vous a envoyé une demande pour {1}",
		BookRequest.REQUEST_ACCEPTED:
			 "Demande acceptée de {0} pour {1}",
		BookRequest.REQUEST_REJECTED:
			 "Demande refusée de {0} pour {1}",
		BookRequest.WITH_COURIER_TO_BORROWER:
			"Votre livre {1} est en cours d'envoi à {0}", 
		BookRequest.WITH_BORROWER:
			"Votre livre {1} est avec {0}", 
		BookRequest.DONE_READING:
			"{0} a terminé de lire votre livre {1}", 
		BookRequest.WITH_COURIER_TO_OWNER:
			"Votre livre {1} vous est renvoyé par {0}", 
		BookRequest.RETURNED:
			"{1} a été retourné par {0}", 
	}

	accept_buttons = (req.status == BookRequest.REQUEST_MADE)

	return {
		'request_id': req.id,
		# add the borrower and title into the message
		'message': messages[req.status].format(borrower, title),
		'accept_buttons': accept_buttons
	}

# request tracking by the borrower of a book
@register.inclusion_tag('bookrequests/request_borrower.html')
def show_request_borrower(req):
	owner = str(req.book.owner)
	title = str(req.book.title)
	author = str(req.book.author)

	messages = {
		BookRequest.REQUEST_MADE:
			 "{0} doit encore approuver votre demande pour {1}",
		BookRequest.REQUEST_ACCEPTED:
			 "{0} a accepté votre demande pour {1}",
		BookRequest.REQUEST_REJECTED:
			 "{0} a refusé votre demande pour {1}",
		BookRequest.WITH_COURIER_TO_BORROWER:
			"{0} a remis {1} au coursier", 
		BookRequest.WITH_BORROWER:
			"Le livre {1} de {0} est avec vous", 
		BookRequest.DONE_READING:
			"Notre coursier viendra récupérer {1} chez vous sous peu", 
		BookRequest.WITH_COURIER_TO_OWNER:
			"{1} est en cours de retour vers {0}", 
		BookRequest.RETURNED:
			"Vous avez retourné {1} à {0}", 
	}

	return_button = (req.status == BookRequest.WITH_BORROWER)

	return {
		'request_id': req.id,
		# add the borrower and title into the message
		'message': messages[req.status].format(owner, title),
		'return_button': return_button
	}

# request tracking by the courier
@register.inclusion_tag('bookrequests/request_courier.html')
def show_request_courier(req):
	messages = {
		BookRequest.REQUEST_ACCEPTED:
			"Récupérer {title} chez {name}, {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),
		BookRequest.DONE_READING:
			"Récupérer {title} chez {name}, {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),

		BookRequest.WITH_COURIER_TO_BORROWER:
			"Déposer {title} chez {name}, {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),
   
		BookRequest.WITH_COURIER_TO_OWNER:
			"Déposer {title} chez {name}, {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),

		BookRequest.WITH_BORROWER:
			"{title} déposé chez {name}, à {addr}".format(
				title=req.book.title,
				name=req.borrower.username,
				addr=req.borrower.userinfo.address),
		BookRequest.RETURNED:
			"{title} déposé chez {name}, à {addr}".format(
				title=req.book.title,
				name=req.book.owner.username,
				addr=req.book.owner.userinfo.address),
	}

	# show the confirm button when there is something to be 
	# done (pick/drop)
	confirm_button = (req.status not in (
			BookRequest.WITH_BORROWER,
			BookRequest.RETURNED,
		))

	return {
		'message': messages[req.status],
		'req_id': req.id,
		'confirm_button' : confirm_button
	}	


# template filters

# returns the pending requests from a queryset 
# of requests
@register.filter
def pending(queryset):
	return queryset.filter(Q(status=BookRequest.REQUEST_MADE)
						|  Q(status=BookRequest.WITH_BORROWER)
						|  Q(status=BookRequest.REQUEST_ACCEPTED)
						|  Q(status=BookRequest.DONE_READING))


# returns the completed requests from a queryset 
# of requests
@register.filter
def completed(queryset):
	return queryset.filter(Q(status=BookRequest.RETURNED)
						|  Q(status=BookRequest.REQUEST_REJECTED))

# returns the requests with courier from a queryset 
# of requests
@register.filter
def intransit(queryset):
	return queryset.filter(Q(status=BookRequest.WITH_COURIER_TO_BORROWER)
						|  Q(status=BookRequest.WITH_COURIER_TO_OWNER))	


@register.filter
def courier_pending(queryset):
	return queryset.filter(Q(status=BookRequest.REQUEST_ACCEPTED)
						|  Q(status=BookRequest.DONE_READING)
						|  Q(status=BookRequest.WITH_COURIER_TO_BORROWER)
						|  Q(status=BookRequest.WITH_COURIER_TO_OWNER))


@register.filter
def courier_completed(queryset):
	return queryset.filter(Q(status=BookRequest.RETURNED)
						|  Q(status=BookRequest.WITH_BORROWER))
