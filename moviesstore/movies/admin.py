from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    odering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)