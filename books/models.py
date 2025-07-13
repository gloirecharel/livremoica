from django.db import models

from django.contrib.auth.models import User


# Create your models here.

from django.utils import timezone

class Book(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
	title = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	summary = models.CharField(max_length=100, default="")
	cover = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name="Image de couverture")
	# Nouveaux champs pour la disponibilité
	is_available = models.BooleanField(default=True)
	unavailable_until = models.DateField(null=True, blank=True)

	def __str__(self):
		return "%s by %s" % (self.title, self.author)

	def check_availability(self):
		"""Met à jour la disponibilité selon la date de retour prévue."""
		if self.unavailable_until and self.unavailable_until < timezone.now().date():
			self.is_available = True
			self.unavailable_until = None
			self.save()
		return self.is_available
