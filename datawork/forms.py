from django import forms

class userform(forms.Form):
    name = forms.CharField(label="users",required=True)
    password = forms.CharField(label="password", required=True)
