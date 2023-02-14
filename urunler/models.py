from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Bu sayfada yapılan her değişikliten sonra makemigrations ve migrate 
# komutlarının girilmesi gerekiyor
class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim

class AltKategori(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim

class SeriNo(models.Model):
    no = models.CharField(max_length=100)
    def __str__(self):
        return self.no

class Urun(models.Model):
    olusturan = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    kategori = models.ForeignKey(Kategori,on_delete=models.CASCADE, null=True, blank=True)
    alt = models.ManyToManyField(AltKategori)
    seri = models.OneToOneField(SeriNo, on_delete=models.SET_NULL, null=True, blank=True)
    isim = models.CharField(max_length=100) # text inputu
    aciklama = models.TextField(max_length = 500) # textarea
    fiyat = models.IntegerField() # number inputu
    resim = models.FileField(upload_to='urunler/', null=True)
    # __str__ : admin panelinde göstermek istediğimiz bilgi
    def __str__(self):
        return self.isim

# database releationships
# manytomany
# onetoone
# foreignkey = manytoone 