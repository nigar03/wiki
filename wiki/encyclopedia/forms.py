from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(label='Content', widget=forms.Textarea)


class EditPageForm(forms.Form):
    content = forms.CharField(label='Content', widget=forms.Textarea)