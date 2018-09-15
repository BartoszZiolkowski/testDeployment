from django import forms
from django.contrib.auth.models import User

#from .validators import validate_name, validate_surname, validate_email_domain
from inventory.models import Supplier, Sample, DOCUMENTS, ROOMS


class UserForm(forms.Form):
    first_name = forms.CharField(label='Imię', max_length=128)
    last_name = forms.CharField(label='Nazwisko', max_length=128)
    email = forms.EmailField(label='Email')



class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class AddUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=128, widget=forms.PasswordInput)



class ChangeUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'



class UpdateSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        exclude = ['sample_code', 'user']


"""    
    sample_code = forms.CharField(max_length=128, verbose_name='kod próbki')
    name = forms.CharField(max_length=500, verbose_name='nazwa')
    supplier = forms.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='dostawca')
    amount = forms.IntegerField(verbose_name='ilość opakowań')
    mass = forms.DecimalField(decimal_places=1, max_digits=4, verbose_name='masa próbki w kg')
    MSDS = forms.BooleanField(choices=DOCUMENTS, verbose_name='dołączony MSDS?')
    TDS = forms.BooleanField(choices=DOCUMENTS, verbose_name='dołączony TDS?')
    location = forms.CharField(choices=ROOMS, max_length=50, verbose_name='miejsce składowania')
    date_received = forms.DateField(default=date.today, verbose_name='data przyjęcia')
"""

class AddSampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        exclude = ['sample_code', 'user', 'barcode']

class SearchForm(forms.Form):
    search_term = forms.CharField(label='', max_length=200)


"""
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    re_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

"""

