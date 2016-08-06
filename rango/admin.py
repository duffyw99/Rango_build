from django.contrib import admin
from rango.models import Category, Page, UserProfile


# Customize admin page, break fields into sub-categories
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    fieldsets = [
        # Heading            'fields' : #model fields to include
        (None,              {'fields' : ['category']}),
        ('Page Details',    {'fields' : ['title', 'url']})
    ]

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)