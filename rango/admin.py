from django.contrib import admin
from rango.models import Category, Page


# Customize admin page, break fields into sub-categories
class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        # Heading            'fields' : #model fields to include
        (None,              {'fields' : ['category']}),
        ('Page Details',    {'fields' : ['title', 'url']})
    ]

# Register your models here.
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
