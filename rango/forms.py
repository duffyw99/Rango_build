from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter a name here.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # slug will be populated during save()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #inline class to provide additional info on the form
    class Meta:
        # associate the ModelForm with the model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter a title here.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), intitial=0)

    class Meta:
        model = Page

        # What fields do we want to include/exclude from our form?
        # We don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # For example, exclude the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        # or specify the fields to include (i.e. not include the category field)
        # fields = ('title', 'url', 'views')
        # include/exclude are DIFFERENT from visable/hidden to the user
        # This is all part of the NESTED Meta class