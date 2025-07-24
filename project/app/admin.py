from django.contrib import admin # type: ignore

from .models import Reservation

admin.site.register(Reservation)