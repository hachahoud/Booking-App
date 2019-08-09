from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import CustomUser
from .models import Day, Hours
from django.urls import path
from django.template.response import TemplateResponse
# Register your models here.

admin.site.site_header = "Bookings Administration"
admin.site.site_title = "Bookings"
admin.site.index_title = "The bookings"

admin.site.register(Hours)
admin.site.unregister(Group)
admin.site.unregister(CustomUser)

@admin.register(Day)	# = admin.site.register(Day, DayAdmin)
class DayAdmin(admin.ModelAdmin):
	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('admin/bookings/day/', self.admin_site.admin_view(self.myview)),	
		]

		return urls + custom_urls

	def myview(self, request):
		context = dict(
			# Include common variables for rendering the admin template.
        	self.admin_site.each_context(request),
        	# Anything else you want in the context...}

          )

		return TemplateResponse(request, 'admin/bookings/mychange.html', context)


#admin.site.index_template = "admin/bookings/mychange.html"