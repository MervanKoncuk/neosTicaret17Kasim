from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def userRegister(request):
    form = KayitForm()
    if request.method == 'POST':
        form = KayitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt Başarılı. Giriş yapabilirsiniz.')
            return redirect('login')
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def userLogin(request):
    if request.method == "POST":
        # post methoduyla gelen inputların çekilmesi
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']
        
        # kullanici adı ve şifreyi veritabanındaki bilgilerle kontrol etmek için
        user = authenticate(request, username = kullanici, password = sifre)

        # bilgilerin doğruluğunu kontrol edip login edilmesi
        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş Yapıldı')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'login.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı')
    return redirect('index')