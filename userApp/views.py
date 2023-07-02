from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from urunApp.models import *

# Create your views here.

# user kayit olursa
def user_register(request):

    if request.method == 'POST':
        k_ad = request.POST.get('k_ad')
        k_email = request.POST.get('k_email')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_email and k_sifre:
            # veritabanini sorgula
            try:
                User.objects.get(email=k_email)
                # boyle bir kullanici varsa hata mesaji dondur
                messages.error(request, message="Bu email adresine sahip bir hesap mevcut")
                return redirect('user-register')

            except:
                # boyle bir kullanici yoktur o zaman kayit et
                User.objects.create_user(username=k_ad, email=k_email, password=k_sifre)
                # basarili mesaji ver
                messages.success(request, message='Basarili bir sekilde kayit oldunuz. Lutfen Giris Yapiniz.')
                return redirect('user-login')
        

    else:
        return render(request, 'user-register.html')

# user giris yaparsa
def user_login(request):
    if request.method == "POST":
        k_ad = request.POST.get('k_ad')
        k_sifre = request.POST.get('k_sifre')

        if k_ad and k_sifre:
            user = authenticate(request, username=k_ad, password=k_sifre)

            if user is not None:
                login(request, user)
                # anasayfaya yonlendir
                return redirect('anasayfa')
            else:
                # hata mesaji yazdir ve logine yonlendir
                messages.error(request, "kullanici veya parola hatali")
                return redirect('user-login')
    else:
        # get istegi geldiginde sayfayi gonder
        return render(request, 'user-login.html')
    
# cikis yapma
def user_logout(request):
    logout(request)
    # anasayfaya yonlendir
    return redirect('anasayfa')

# hesap ayarlari
from urunApp.form import CreditCardForm

@login_required(login_url='user-login')
def user_setting(request):
    context = {}
    cardForm = CreditCardForm()
    # kullanicinin karti var mi yok mu
    hesapBilgisi = UserCreditCard.objects.filter(user_id=request.user.id).first()

    if hesapBilgisi is None:
        context['cardDetail'] = False
    else:
        context['cardDetail'] = hesapBilgisi
        context['form'] = CreditCardForm(instance=hesapBilgisi)

    # post istegi gelirse
    if request.method == "POST":
        duzenlemeIstegi = request.POST.get('_cardDuzenle')
        silmeIstegi = request.POST.get('_cardSil')
        sifreDegistirmeIstegi = request.POST.get('_sifreDuzenle')

        # sifre degistirme istegi
        if sifreDegistirmeIstegi:
            # sifre degistirme istegi gelmis inputlari al
            sifre_1 = request.POST.get('password_check_1')
            sifre_2 = request.POST.get('password_check_2')

            if sifre_1 and sifre_2 and sifre_1 == sifre_2:
                # user objesini bul
                user = User.objects.filter(id=request.user.id).first()
                # sifre degis
                user.set_password(sifre_1)
                user.save()
                # cikis yap ve tekrar girmesini iste
                logout(request)
                return redirect('user-login')
    

        # silme istegi varsa
        if silmeIstegi:
            cardForm = CreditCardForm(request.POST)
            if cardForm.is_valid():
                hesapBilgisi.delete()
                messages.success(request, message='Basarili bir sekilde kartiniz silindi.')
                return redirect('user-setting')
            else:
                # potansiyel hata durumlarinda
                messages.error(request, message='Uzgunuz kartinizi silerken bir takim sorunlar meydana geldi. Daha sonra tekrardan deneyiniz.')
                return redirect('404')

        # duzenleme istegi varsa kart bilgilerini guncelle
        if duzenlemeIstegi:
            cardForm =CreditCardForm(request.POST, instance=hesapBilgisi)
            if cardForm.is_valid():
                cardForm.save()
                messages.success(request, message='Basarili bir sekilde kart bilgileriniz guncellendi.')
                return redirect('user-setting')
            else:
                # potansiyel hata durumlarinda
                messages.error(request, message='Uzgunuz kartinizi guncellerken bir takim sorunlar meydana geldi. Daha sonra tekrardan deneyiniz.')
                return redirect('404')
        # duzenleme istegi yoksa alt kosulu calistir:

        # post uzerinden verileri cek (karti yoksa kart olustur)
        cardForm = CreditCardForm(request.POST)
        if cardForm.is_valid():
            cardForm = cardForm.save(commit=False)
            cardForm.user = request.user
            cardForm.save()
            return redirect('user-setting')
        else:
            print('hatalar:', cardForm.errors.as_data())
            messages.error(request, 'Uzgunuz kartinizi olustururken bir takim sorunlar meydana geldi. Daha sonra tekrardan deneyiniz')
            return redirect('404')

    else:
        # get istekleri 
        # istegi yapan kisinin satin alma gecmisini yazdir
        purchaseHistory = PurchaseLog.objects.filter(user_id=request.user.id)

        # if purchaseHistory is not None:
        #     context['purchaseLog'] = purchaseHistory

        paginator = Paginator(purchaseHistory, 3) 
        page_number = request.GET.get("page")

        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        

        return render(request, 'user-setting.html', context)