"""BZlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from inventory.views import HomeView, Login, Logout, AddUser, ChangeUserDataView, AddSupplier, UpdateSupplier, \
    DeleteSupplier, ViewSuppliers, ViewSamples, ViewRecipes, AddSample, DeleteSample, UpdateSample, ViewSamplePhoto, \
    ViewSampleBarcode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home_view'),
    url(r'^login', Login.as_view(), name='login-form'),
    url(r'^logout', Logout.as_view(), name='logout'),
    url(r'^add_user', AddUser.as_view(), name='add-user'),
    path('edit_user/<user_id>', ChangeUserDataView.as_view(), name='edit-user'),
    url(r'^add_supplier', AddSupplier.as_view(), name='add-supplier'),
    path('update_supplier/<pk>', UpdateSupplier.as_view(), name='update-supplier'),
    path('delete_supplier/<pk>', DeleteSupplier.as_view(), name='delete-supplier'),
    url(r'^view_suppliers/', ViewSuppliers.as_view(), name='view-suppliers'),

    path('samples_list/', ViewSamples.as_view(), name='samples-view'),
    path('recipes/', ViewRecipes.as_view(), name='recipes-view'),
    url(r'^add_sample/', AddSample.as_view(), name='add-sample'),
    path('delete_sample/<pk>', DeleteSample.as_view(), name='delete-sample'),
    path('update_sample/<pk>', UpdateSample.as_view(), name='update-sample'),
    path('sample_photo/<pk>', ViewSamplePhoto.as_view(), name='sample-photo'),
    path('barcode/<pk>', ViewSampleBarcode.as_view(), name='barcode-view'),
]

"""
url(r'^product/(?P<id>([0-9]+))/$', ProductView.as_view(), name='product'),
"""