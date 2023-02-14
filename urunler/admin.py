from django.contrib import admin
from .models import *
# Register your models here.

# Modeli admin panelinde görüntüleyebilmek için
admin.site.register(Urun)
admin.site.register(Kategori)
admin.site.register(AltKategori)
admin.site.register(SeriNo)