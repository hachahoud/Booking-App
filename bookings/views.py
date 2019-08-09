from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required
def delete_book(request, book_date):
	"""Delete a booking."""
	# the object (one object)
	booking = Day.objects.filter(date=book_date, owner=request.user)
	if request.method == 'POST':
		#confirming delete.
		booking.delete()
		return HttpResponseRedirect(reverse('bookings:home'))

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
				#day = match_objects_day(book_date, request.user)
				messages.add_message(request, messages.ERROR,'You already have a booking for this day!')
				return HttpResponseRedirect(reverse("bookings:date"))

			else:
				day = form.save(commit=False)
				day.owner = request.user
				day.reserved = 0
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
		# check if there's room 
		day_set = Day.objects.filter(date=book_date)
		# max 25 bookings for each hour
		room = [2 for _ in range(9)]
		full = 9
		for d in day_set:
			#just one hours object but it's a query so iterate is necessary
			for h in d.hours_set.all():
				if h.h1:
					room[0] -= 1
					if not room[0]:
						full -= 1
						form.fields['h1'].widget.attrs['disabled'] = True
						form.fields['h1'].initial = True
				if h.h2:
					room[1] -= 1
					if not room[1]:
						full -= 1
						form.fields['h2'].widget.attrs['disabled'] = True
						form.fields['h2'].initial = True
				if h.h3:
					room[2] -= 1
					if not room[2]:
						full -= 1
						form.fields['h3'].widget.attrs['disabled'] = True
						form.fields['h3'].initial = True
				if h.h4:
					room[3] -= 1
					if not room[3]:
						full -= 1
						form.fields['h4'].widget.attrs['disabled'] = True
						form.fields['h4'].initial = True
				if h.h5:
					room[4] -= 1
					if not room[4]:
						full -= 1
						form.fields['h5'].widget.attrs['disabled'] = True
						form.fields['h5'].initial = True
				if h.h6:
					room[5] -= 1
					if not room[5]:
						full -= 1
						form.fields['h6'].widget.attrs['disabled'] = True
						form.fields['h6'].initial = True
				if h.h7:
					room[6] -= 1
					if not room[6]:
						full -= 1
						#no room left for this hour: disable
						form.fields['h7'].widget.attrs['disabled'] = True
						form.fields['h7'].initial = True
				if h.h8:
					room[7] -= 1
					if not room[7]:
						full -= 1
						form.fields['h8'].widget.attrs['disabled'] = True
						form.fields['h8'].initial = True
				if h.h9:
					room[8] -= 1
					if not room[8]:
						full -= 1
						form.fields['h9'].widget.attrs['disabled'] = True
						form.fields['h9'].initial = True
				# all hours are reserved fully, display error
				if full == 0:
					messages.add_message(request, messages.INFO,'No left room for this date - Please choose another date.')
					# delete the Day object that was created
					booking = Day.objects.get(date=book_date,owner=request.user)
					booking.delete()
					return HttpResponseRedirect(reverse("bookings:date"))

	else:
		form = HoursForm(request.POST)
		day = Day.objects.get(date=book_date,owner=request.user)
		if form.is_valid():
			# First time to book for this day.
			# build the relationship Hours-Day models.
			hours = form.save(commit=False)
			# the number of hours reserved for a day.
			hs = ['h1','h2','h3','h4','h5','h6','h7','h8','h9']
			for h in hs:
				if request.POST.get(h,False)=="True":
					day.reserved += 1
			day.save()

			hours.related_day = day
			hours.save()


			return HttpResponseRedirect(reverse('bookings:home'))

	context = {'form':form, 'date':book_date}
	return render(request,"bookings/hours.html", context)
