from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
# Create your views here.
def index(request):
    # Veritabanımızdaki bilgileri çekmek için
    urunler = Urun.objects.all() # all fonksiyonu Urun classına ait tüm objeleri çeker
    kategoriler = Kategori.objects.all()
    # search
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        urunler = Urun.objects.filter(
            Q(isim__icontains = search) |
            Q(kategori__isim__icontains = search)
        )

    # urunler değişkeniyle çektiğimiz verileri index.html sayfasına göndermek için
    # ** context değişkenini render içerisine atmayı unutmayın **
    context = {
        'urunler':urunler,
        'search':search,
        'kategoriler':kategoriler
    }
    return render(request, 'index.html', context)



def urun(request, urunId):
    urunum = Urun.objects.get(id = urunId)
    context = {
        'urun':urunum
    }
    return render(request, 'urun.html', context)


def olustur(request):
    form = UrunForm()
    if request.method == 'POST':
        form = UrunForm(request.POST, request.FILES)
        if form.is_valid():
            urun = form.save(commit=False)
            urun.olusturan = request.user
            urun.save()
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'olustur.html', context)