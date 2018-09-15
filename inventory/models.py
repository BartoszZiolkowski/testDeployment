from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

DOCUMENTS = ((False, 'Nie'),
             (True, 'Tak')
            )

ROOMS = (('1', 'pokój nr 1'),
         ('2', 'pokój nr 2'),
         ('3', 'pokój nr 3'),
         ('4', 'pokój nr 4'),
         ('5', 'pokój nr 5'),
         ('6', 'pokój nr 6'),
         ('7', 'pokój nr 7'),
         ('8', 'pokój nr 8'),
)





class Supplier(models.Model):
    name = models.CharField(max_length=500, unique=True)
    address = models.CharField(max_length=500)
    email = models.EmailField(max_length=254)
    telephone = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Sample(models.Model):

    sample_code = models.CharField(max_length=128, unique=True, verbose_name='kod próbki')
    name = models.CharField(max_length=500, verbose_name='nazwa')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='dostawca')
    amount = models.IntegerField(verbose_name='ilość opakowań')
    mass = models.DecimalField(decimal_places=1, max_digits=4, verbose_name='masa próbki w kg')
    MSDS = models.BooleanField(choices=DOCUMENTS, verbose_name='dołączony MSDS?')
    TDS = models.BooleanField(choices=DOCUMENTS, verbose_name='dołączony TDS?')
    location = models.CharField(choices=ROOMS, max_length=50, verbose_name='miejsce składowania')
    date_received = models.DateField(default=date.today, verbose_name='data przyjęcia')
    user = models.ForeignKey(User, on_delete=models.SET('deleted user'), verbose_name='podpis')
    photo = models.ImageField(upload_to='img/')
    barcode = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.name
