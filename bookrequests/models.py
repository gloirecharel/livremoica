from django.db import models

from django.contrib.auth.models import User

from books.models import Book


from django.utils import timezone

class BookRequest(models.Model):
	REQUEST_MADE = 0
	REQUEST_ACCEPTED = 1
	REQUEST_REJECTED = 2
	WITH_COURIER_TO_BORROWER = 3
	WITH_BORROWER = 4
	DONE_READING = 5
	WITH_COURIER_TO_OWNER = 6
	RETURNED = 7

	STATUS_CHOICES = (
		(REQUEST_MADE, 'request pending'),
		(REQUEST_ACCEPTED, 'request accepted'),
		(REQUEST_REJECTED, 'request rejected'),
		(WITH_COURIER_TO_BORROWER, 'being delivered to borrower'),
		(WITH_BORROWER, 'with borrower'),
		(DONE_READING, 'done reading'),
		(WITH_COURIER_TO_OWNER, 'being delivered to owner'),
		(RETURNED, 'returned'),
	)

	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	borrower = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	# Date de retour prévue pour ce prêt
	due_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return str(self.borrower) + " requested " + str(self.book) + " from " + str(self.book.owner)

	def save(self, *args, **kwargs):
		# Synchronise la date de retour prévue avec le livre si renseignée
		if self.due_date:
			self.book.unavailable_until = self.due_date
			self.book.is_available = False
			self.book.save()
		super().save(*args, **kwargs)

	def next_status(self):
		next_statuses = {
			# set manually, dont use this function
			# to advance a pending request
			self.REQUEST_MADE: self.REQUEST_MADE,

			self.REQUEST_ACCEPTED: self.WITH_COURIER_TO_BORROWER,

			self.REQUEST_REJECTED: self.REQUEST_REJECTED,

			self.WITH_COURIER_TO_BORROWER: self.WITH_BORROWER,

			self.WITH_BORROWER: self.DONE_READING,

			self.DONE_READING: self.WITH_COURIER_TO_OWNER,

			self.WITH_COURIER_TO_OWNER: self.RETURNED,

			self.RETURNED: self.RETURNED,
		}

		return next_statuses[self.status]

