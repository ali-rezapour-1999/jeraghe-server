from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='ایمیل', max_length=254)


