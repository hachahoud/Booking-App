"Defines URL patterns for bookings."

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
	path('', views.home, name='home'),
	path('<book_date>/delete', views.delete_book, name='delete-book'),
	path('date', views.date, name='date'),
	path('hours/<book_date>', views.hours, name='hours'),
	]