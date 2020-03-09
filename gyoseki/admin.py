from django.contrib import admin
from .models import Author, Recode, Tag, Division, Language

# Register your models here.
admin.site.register(Author)
admin.site.register(Recode)
admin.site.register(Tag)
admin.site.register(Division)
admin.site.register(Language)