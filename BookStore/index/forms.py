from django import forms


class TitleSearch(forms.Form):
    title = forms.CharField(label='书名', label_suffix='', error_messages={'required':'请出入正确的‘title'})
