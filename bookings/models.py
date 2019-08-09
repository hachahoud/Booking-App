from django.db import models
from users.models import CustomUser

# Create your models here.
class Day(models.Model):
	"""This model contains the chosen date for the booking."""

	owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	# hours reserved for a day
	reserved = models.PositiveIntegerField(default=0)
	date = models.DateField()

	def __str__(self):
		return str(self.date)

class Hours(models.Model):
	"""The hours for a specific day."""
	
	related_day = models.ForeignKey(Day,on_delete=models.CASCADE)
	h1 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h2 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h3 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h4 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h5 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h6 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h7 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h8 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))
	h9 = models.BooleanField(default=False,blank=True,choices=((True,'Reserved'),(False,'Unreserved')))

	def __str__(self):
		return str(self.related_day)
