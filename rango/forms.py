from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

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
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

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

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url isn't empty and doesn't start with "http://", add http:// to it
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class UserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')