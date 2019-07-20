from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from .forms import DayForm, HoursForm
from .models import Day, Hours
# Create your views here.

def home(request):
	"""Show the bookings a user has made if a user is authenticated."""
	if request.user.is_authenticated:
		days = Day.objects.filter(owner=request.user)
		context = {'days':days}
		return render(request,"bookings/home.html", context)
	else:
		return render(request,"bookings/home.html")

def match_objects_day(book_date, user):
	"""Select the corresponding object 'Day' for a user.
	return the object if it already existed, or False instead."""
	try:
		day = Day.objects.filter(date=book_date, owner=user)[0]
	except:
		return False
	else:
		return day

@login_required
def date(request):
	if request.method != 'POST':
		form = DayForm()
	else:
		# POST request, process..
		form = DayForm(request.POST)
		if form.is_valid():
			# check if the user had created an object for this date.
			book_date = datetime.date(int(request.POST['date_year']),int(request.POST['date_month']),
				int(request.POST['date_day']))
			if match_objects_day(book_date, request.user):
				day = match_objects_day(book_date, request.user)
			else:
				day = form.save(commit=False)
				day.owner = request.user
				day.save()

			return HttpResponseRedirect(reverse('bookings:hours', args=[day.date]))

	context = {'form':form}
	return render(request, 'bookings/date.html', context)


@login_required
def hours(request,book_date):

	if request.method != 'POST':
		# 1-get the bookings for the day the user choose.		
		# 2-get the hours set objects, True value of a Hours model field means reserved.
		# 3-disable the already reserved hours.
		form = HoursForm()
		day_set = Day.objects.filter(date=book_date)
		for d in day_set:
			for h in d.hours_set.all():	# should be just one
				if h.h1:
					form.fields['h1'].widget.attrs['disabled'] = True
					form.fields['h1'].initial = True
				if h.h2:
					form.fields['h2'].widget.attrs['disabled'] = True
					form.fields['h2'].initial = True
				if h.h3:
					form.fields['h3'].widget.attrs['disabled'] = True
					form.fields['h3'].initial = True
				if h.h4:
					form.fields['h4'].widget.attrs['disabled'] = True
					form.fields['h4'].initial = True
				if h.h5:
					form.fields['h5'].widget.attrs['disabled'] = True
					form.fields['h5'].initial = True
				if h.h6:
					form.fields['h6'].widget.attrs['disabled'] = True
					form.fields['h6'].initial = True
				if h.h7:
					form.fields['h7'].widget.attrs['disabled'] = True
					form.fields['h7'].initial = True
				if h.h8:
					form.fields['h8'].widget.attrs['disabled'] = True
					form.fields['h8'].initial = True
				if h.h9:
					form.fields['h9'].widget.attrs['disabled'] = True
					form.fields['h9'].initial = True
	else:
		form = HoursForm(request.POST)
		day = Day.objects.get(date=book_date,owner=request.user)
		if form.is_valid():
			# First time to book for this day.
			# build the relationship Hours-Day models.
			hours = form.save(commit=False)
			hours.related_day = day
			hours.save()

			return HttpResponseRedirect(reverse('bookings:home'))

	context = {'form':form, 'date':book_date}
	return render(request,"bookings/hours.html", context)
