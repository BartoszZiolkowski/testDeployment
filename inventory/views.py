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

                return redirect('/')
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


                    return redirect('/')

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


                return redirect('/')
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
    success_url = '/'


class UpdateSupplier(UpdateView):
    model = Supplier
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = '/'


class ViewSuppliers(View):
    def get(self, request):
        suppliers = Supplier.objects.all()

        return render(request, 'supplier_list.html', {'suppliers':suppliers})


class DeleteSupplier(DeleteView):
    model = Supplier
    success_url = '/'




class AddSample(View):
    def get(self, request):
        form = AddSampleForm()

        return render(request, 'add_sample.html', {'form': form} )

    def post(self, request):

        form = AddSampleForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            number_of_samples_that_day = Sample.objects.filter(date_received=form.cleaned_data['date_received']).count()

            sample_code = '{}-{}'.format(form.cleaned_data['date_received'],number_of_samples_that_day+1)
            
            data = form.cleaned_data
            data['sample_code'] = sample_code
            data['user'] = request.user
            data['user_id'] = request.user.pk


            try:
                new_sample = Sample.objects.create(**data)

                return redirect('/samples_list')
            except Exception as e:
                return render(request, 'add_sample.html', {'form': form,
                                                 'message': e})



        return render(request, 'add_sample.html', {'form': form,
                                                 'message': 'coś nie tak w formularzu'})

class UpdateSample(UpdateView):

    fields = ['name', 'supplier', 'amount', 'mass', 'MSDS', 'TDS', 'location', 'date_received' ]

    fields = ['name', 'supplier', 'amount', 'mass', 'MSDS', 'TDS', 'location', 'date_received']


    template_name_suffix = '_update_form'
    success_url = '/samples_list'


class DeleteSample(DeleteView):
    model = Sample
    success_url = '/samples_list'





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




class ViewRecipes(View):
    def get(self, request):

        return HttpResponse('get')

