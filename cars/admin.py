from django.contrib import admin
from .models import Dealer, Car, CarImage, ContactMessage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CarImageInline]
    list_display = ("title","price","year","mileage")

admin.site.register(Dealer)
admin.site.register(ContactMessage)
