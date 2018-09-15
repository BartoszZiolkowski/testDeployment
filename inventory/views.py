from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from inventory.models import Supplier, Sample
from .forms import LoginForm, AddUserForm, ChangeUserDataForm, AddSampleForm, UpdateSampleForm, SearchForm
from django.views.generic import DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
import re
import os
from barcode import generate
import datetime
# Create your views here.


class HomeView(View):
    def get(self, request):

        return render(request, 'home.html')

    def post(self, request):

        return HttpResponse('post request')



class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            userAuth = authenticate(**form.cleaned_data)

            if userAuth:
                login(request, userAuth)
                logged_in = request.user.is_authenticated

                return redirect('/home')
                    #render(request, 'home.html', {'data':userAuth})
            else: return render(request, 'login.html', {'form':form,
                                                        'message':'wrong data'})

class Logout(View):


    def get(self, request):
        logout(request)
        form = LoginForm()
        return render(request, 'login.html', {'form':form})


    def post(self, request):
        logout(request)
        form = LoginForm()
        return render(request, 'login.html', {'form':form})


class AddUser(View):

    def get(self, request):

        form = AddUserForm()
        return render(request, 'add_user.html', {'form':form})

    def post(self, request):

        form = AddUserForm(request.POST)
        if form.is_valid():

            try:
                User.objects.get(username=form.cleaned_data['username'])

                return render(request, 'add_user.html', {'form': form,
                                                         'message': 'user already exists'})

            except Exception as e:
                if form.cleaned_data['password'] == form.cleaned_data['repeat_password']:

                    User.objects.create_user(username=form.cleaned_data['username'],
                                             password=form.cleaned_data['password'],
                                             first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             email=form.cleaned_data['email'])


                    return redirect('/home')

                else:
                    return render(request, 'add_user.html', {'form': form,
                                                             'message': 'passowords are not the same'})
        return render(request, 'add_user.html', {'form': form,
                                                 'message': 'coś nie tak w formularzu'})



class ChangeUserDataView(View):

    def get(self, request, user_id):


        try:
            user = User.objects.get(pk=user_id)
        except:
            return HttpResponse('there is no user with id {}'.format(user_id))

        form = ChangeUserDataForm(initial=model_to_dict(user))
        print(request.user.username)

        return render(request, 'change_user_data.html', {'form': form,
                                                        'user_id': user_id})

    def post(self, request, user_id):
        form = ChangeUserDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = User.objects.get(pk=user_id)
            if data['password'] == data['repeat_password']:
                user.set_password(data['password'])
                user.username = (data['username'])
                user.save()


                return redirect('/home')
            else:
                return render(request, 'change_user_data.html', {'form': form,
                                                                'error': 'password not the same',
                                                                'user_id': user_id
                                                                 })
        return render(request, 'change_user_data.html', {'form': form,
                                                        'error': 'form not valid',
                                                        'user_id': user_id
                                                         })




class AddSupplier(CreateView):
    model = Supplier
    fields = '__all__'
    success_url = '/home'


class UpdateSupplier(UpdateView):
    model = Supplier
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/home'


class ViewSuppliers(View):
    def get(self, request):
        suppliers = Supplier.objects.all()

        return render(request, 'supplier_list.html', {'suppliers':suppliers})


class DeleteSupplier(DeleteView):
    model = Supplier
    success_url = '/home'




class AddSample(View):
    def get(self, request):
        form = AddSampleForm()

        return render(request, 'add_sample.html', {'form': form} )

    def post(self, request):

        form = AddSampleForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)

            number_of_samples_that_day = Sample.objects.filter(date_received=form.cleaned_data['date_received']).count()

            sample_code = '{}-{}'.format(form.cleaned_data['date_received'],number_of_samples_that_day+1)
            
            data = form.cleaned_data
            data['sample_code'] = sample_code
            data['user'] = request.user
            data['user_id'] = request.user.pk
            """
            filename = f'static/img/{sample_code}'
            barcode = generate('code128', sample_code, output=filename)
            PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
            barcode_opened = open('static/img/', f'{filename}.svg')
            data['barcode'] = barcode_opened
            """

            try:
                new_sample = Sample.objects.create(**data)

                return redirect('/samples_list')
            except Exception as e:
                return render(request, 'add_sample.html', {'form': form,
                                                 'message': e})



        return render(request, 'add_sample.html', {'form': form,
                                                 'message': 'coś nie tak w formularzu'})
"""
class UpdateSample(View):

    def get(self, request, pk):
        sample = Sample.objects.get(pk=pk)
        form = UpdateSampleForm(instance=sample)
        return render(request, 'sample_update_form.html', {'form':form})


"""
class UpdateSample(UpdateView):
    model = Sample
    fields = ['name', 'supplier', 'amount', 'mass', 'MSDS', 'TDS', 'location', 'date_received', 'photo' ]

    template_name_suffix = '_update_form'
    success_url = '/samples_list'


class DeleteSample(DeleteView):
    model = Sample
    success_url = '/samples_list'

"""
class AddSample(CreateView):
    model = Sample
    fields = '__all__'
    success_url = '/home'
"""




class ViewSamples(View):

    def get(self, request):
        form = SearchForm()
        samples = Sample.objects.all().order_by('-date_received')


        return render(request, 'samples_list.html', {'samples': samples,
                                                     "form": form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data['search_term']

                # żeby można było wpisać kilka słów i oddzielić dowolnym znakiem

                word_list = re.sub("[^\w]", " ", data).split()
                result = Sample.objects.filter(name__icontains=word_list[0])
                for data in word_list:
                    result_sample_code = Sample.objects.filter(sample_code__icontains=data)
                    result_name = Sample.objects.filter(name__icontains=data)
                    result_supplier = Sample.objects.filter(supplier__name__icontains=data)
                    result_amount = Sample.objects.filter(amount__icontains=data)
                    result_mass = Sample.objects.filter(mass__icontains=data)
                    result_location = Sample.objects.filter(location__icontains=data)
                    result_date_received = Sample.objects.filter(date_received__icontains=data)
                    result_user = Sample.objects.filter(user__username__icontains=data)

                    result_loop = result_sample_code | \
                                  result_name | \
                                  result_supplier | \
                                  result_amount | \
                                  result_mass | \
                                  result_location | \
                                  result_date_received | \
                                  result_user
                    result = result | result_loop

                message = f'wyniki wyszukiwania dla: {", ".join(word_list)}'
                return render(request, 'samples_list.html', {'samples': result,
                                                               'message': message,
                                                               'form': form})

            except Exception as e:
                return HttpResponse(e)
        return HttpResponse('form not valid')


class ViewSamplePhoto(View):
    def get(self, request,pk):
        file = Sample.objects.get(pk=pk)
        return render(request, 'sample_photo.html', {'file':file})

class ViewSampleBarcode(View):
    def get(self, request, pk):

        barcode = Sample.objects.get(pk=pk)

        return render(request, 'barcode.html', {'file':barcode})



"""
sample_code = models.CharField(max_length=128, unique=True, verbose_name='kod próbki')
    name = models.CharField(max_length=500, verbose_name='nazwa')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='dostawca')
    amount = models.IntegerField(verbose_name='ilość opakowań')
    mass = models.DecimalField(decimal_places=1, max_digits=4, verbose_name='masa próbki w kg')
    MSDS = models.BooleanField(choices=DOCUMENTS, verbose_name='dołączony MSDS?')
    TDS = models.BooleanField(choices=DOCUMENTS, verbose_name='dołączony TDS?')
    location = models.CharField(choices=ROOMS, max_length=50, verbose_name='miejsce składowania')
    date_received = models.DateField(default=date.today, verbose_name='data przyjęcia')
    user = models
"""




class ViewRecipes(View):
    def get(self, request):

        return HttpResponse('get')


"""
import barcode
barcode.PROVIDED_BARCODES[u'code39', u'code128', u'ean', u'ean13', u'ean8', u'gs1', u'gtin', u'isbn', u'isbn10', u'isbn13', u'issn', u'jan', u'pzn', u'upc', u'upca']
EAN = barcode.get_barcode_class('ean13')
print(EAN)



print(name)
u'barcode_svg.svg'
# with file like object
>>> fp = StringIO()
>>> generate('EAN13', u'5901234123457', writer=ImageWriter(), output=fp)

"""