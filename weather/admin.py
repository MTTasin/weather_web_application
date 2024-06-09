from django.contrib import admin
from .models import City, Worldcities

# Register your models here.


admin.site.register(City)

@admin.register(Worldcities)
class WorldcitiesAdmin(admin.ModelAdmin):
    list_display = ('field1',)