from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib import messages
import iyzipay
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
import pprint


api_key = 'sandbox-QWJSy8tyY4uTQFwdBVrSyQO1p7Y3rUMP'
secret_key = 'sandbox-SR271XzbIn5nN7j21auHtmUyD7n3PnKX'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()


def payment(request):
    context = dict()
    odeme = Odeme.objects.get(user = request.user, odendiMi = False)
    buyer={
        'id': 'BY789',
        'name': odeme.user.username,
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': odeme.user.email,
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': odeme.toplamFiyat,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)


def success(request):
    context = dict()
    context['success'] = 'İşlem Başarılı'
    sepetim = Sepet.objects.filter(user = request.user, odendiMi = False)
    for i in sepetim:
        i.odendiMi = True
        i.save()
    odeme = Odeme.objects.get(user = request.user, odendiMi = False)    
    odeme.odendiMi = True
    odeme.save()
    messages.success(request, 'İşlem başarılı')
    return redirect('index')


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'
    messages.error(request, 'İşlem başarısız')
    return redirect('index')


# index function
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
    # sepete ekleme
    if request.method == 'POST':
        if request.user.is_authenticated:
            urunId = request.POST['urunId']
            adet = request.POST['adet']
            adet = int(adet)
            # eklenecek ürün
            urunum = Urun.objects.get(id = urunId)
            if Sepet.objects.filter(user = request.user, urun = urunum).exists():
                sepetim = Sepet.objects.get(user = request.user, urun = urunum)
                sepetim.adet += adet
                sepetim.toplam = urunum.fiyat * sepetim.adet
                sepetim.save()
                messages.success(request, "Ürün sepette güncellendi")
                return redirect('index')
            else:
                sepetim = Sepet.objects.create(
                    urun = urunum,
                    user = request.user, 
                    adet = adet,
                    toplam = urunum.fiyat * adet
                )
                sepetim.save()
                messages.success(request, "Ürün sepete eklendi")
                return redirect('index')
        else:
            messages.error(request, 'Giriş yapmanız gerekiyor')
            return redirect('login')
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

def sepet(request):
    user = request.user
    sepetim = Sepet.objects.filter(user = user, odendiMi = False)
    toplam = 0
    for i in sepetim:
        toplam += i.toplam
    if 'odeme' in request.POST:
        if Odeme.objects.filter(user = request.user, odendiMi = False).exists():
            return redirect('payment')
        else:
            odeme = Odeme.objects.create(
                user = user, 
                toplamFiyat = toplam
            )
            odeme.sepet.add(*sepetim)
            odeme.save()
            return redirect('payment')
    elif request.method == 'POST':
        urunId = request.POST['urunId']
        sepet = Sepet.objects.get(id = urunId)
        if 'guncelle' in request.POST:
            yeniAdet = request.POST['yeniAdet']
            sepet.adet = yeniAdet
            sepet.toplam = sepet.urun.fiyat * int(yeniAdet)
            sepet.save()
            messages.success(request, f'{sepet.urun.isim} Ürünün Adeti Güncellendi')
            return redirect('sepet')
        else:
            sepet.delete()
            messages.success(request, 'Ürün Sepetten Kaldırıldı.')
            return redirect('sepet')
    context = {
        'sepetim':sepetim,
        'toplam':toplam
    }
    return render(request, 'sepet.html', context)

