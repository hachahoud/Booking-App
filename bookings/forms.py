from django import forms
from django.core.exceptions import ValidationError
import datetime

from .models import Day, Hours

class DayForm(forms.ModelForm):
	class Meta:
		model = Day
		fields = ['date']
		#labels = {'firstname':'','lastname':'','datetime':''}
		widgets = {'date':forms.SelectDateWidget()}

	def clean_date(self):
		data = self.cleaned_data['date']

		# check if data is not in the past.
		if data < datetime.date.today():
			raise ValidationError('Invalid date - date is in past')
		elif data > datetime.date.today() + datetime.timedelta(weeks=2):
			raise ValidationError('Invalid date - can\'t book more than 2 weeks beforehand')

		return data

class HoursForm(forms.ModelForm):
	class Meta:
		model = Hours
		fields = ['h1','h2','h3','h4','h5','h6','h7','h8','h9']
		labels = {'h1':'09:00 to 10:00',
				'h2':'10:00 to 11:00',
				'h3':'11:00 to 12:00',
				'h4':'12:00 to 13:00',
				'h5':'13:00 to 14:00',
				'h6':'14:00 to 15:00',
				'h7':'15:00 to 16:00',
				'h8':'16:00 to 17:00',
				'h9':'17:00 to 18:00'}
