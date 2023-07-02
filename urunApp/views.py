from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# Sayfalarimizi ayarladigimiz yer
def anaSayfa(request):
    # sayfayi render et
    return render(request, 'index.html')

# Urunlerimiz Sayfasi
def urunlerimiz(request):
    context = {}
    aramaIstegi = request.GET.get('filtrele')

    if aramaIstegi:
        # kullanici urun aramak istiyosa
        filtrelenenUrunler = Urun.objects.filter(ad__icontains = aramaIstegi)
        context['data'] = filtrelenenUrunler
    else:
        butunVeriler = Urun.objects.all()
        context["data"] = butunVeriler
    return render(request, 'urunlerimiz.html', context)

# Hakkimizda Sayfasi
def hakkimizda(request):
    # sayfayi render et
    return render(request, 'hakkimizda.html')


# hata sayfasi
def sayfa_bulunamadi(request):
    return render(request, "404.html")


# detay sayfasi 
def detail_page(request, urunId):
    # veritabani sorgulamasi
    context = {}

    try:
        urun = Urun.objects.filter(id=urunId).first() #bulursa object aksi takdirde guzel bi hata

        if urun is None:
            return redirect("anasayfa")
        # contexte at
        context["data"]=urun

        # kredi karti var mi yok mu?
        hasCard = UserCreditCard.objects.filter(user_id=request.user.id).first()

        if hasCard:
            context['hasCard'] = True
        else:
            context['hasCard'] = False

        # user adminse
        if request.user.is_superuser:
                context['admin'] = True
            
        # user urunu olusturan kisi ise
        # if request.user.id == urun.satici.id:
        #     context['urunSahibi'] = True

            
    except:
        return redirect("404")
   
    return render(request, "detail_product.html", context)

# urun ekleme
from .form import CreateUrun
def createProduct(request):
        # metotlari ayir
        context = {}
        urunForm = CreateUrun()
        if request.method == "POST":
            # post istegi icin
            if request.user.is_authenticated is False:
                messages.error(request, 'Yetkilendirme Basarisiz.')
                return redirect('404')
            
            urunForm = CreateUrun(request.POST, request.FILES)
            # request files calismiyor
            if urunForm.is_valid():
                urunForm.save()
            # anasayfaya yonlendir
            return redirect("urunlerimiz")
        else:
            # get put delete istekleri icin:
            context['form'] = urunForm
            return render(request, 'createProduct.html', context)

# urun guncelle
def editProduct(request, urunId):
    context = {}

    urun = Urun.objects.filter(id=urunId).first()

    if urun is None:
        return redirect('404')
    
    if urun.satici.id != request.user.id and request.user.is_superuser is not True:
        raise PermissionDenied()

    
    productForm = CreateUrun(instance=urun)

    if request.method == 'POST':
        urunForm = CreateUrun(request.POST, request.FILES, instance=urun)
        if urunForm.is_valid():
            urunForm.save()
        # sayfaya yonlendir
        return redirect('/urun/' + str(urunId))
    else:
        # get istekleri
        context['form'] = productForm
        context['data'] = urun
        return render(request, 'editProduct.html', context) 

# urun sil
def deleteProduct(request, urunId):
    # get istegi geldiginde mesaji sil
    product = Urun.objects.filter(id=urunId).first()

    if product is None:
        return redirect('404')
    
    # istegi yapan kisi?
    if product.satici.id != request.user.id and request.user.is_superuser is not True:
        # permission denied
        raise PermissionDenied()
    
    # hicbir problem yoksa veriyi sil
    product.delete()
    return redirect('urunlerimiz')

# urun satin al
def makePurchase(request, urunId):
    if request.method == "POST":

        satinAlinanUrun = Urun.objects.filter(id=urunId).first()
        kartBilgisi = UserCreditCard.objects.filter(user_id = request.user.id).first()

        if satinAlinanUrun is None:
            messages.error(request, "Uzgunuz bu urun stokta bulunamadi.")
            return redirect('404')
        
        if satinAlinanUrun.stokAdet <=0 :
            messages.error(request, "Uzgunuz satin almank istediginiz urun tukenmistir.")
            return redirect('404')
        
        # istegi yapan kisinin karti
        if kartBilgisi is None:
            messages.error(request, message="Uzgunuz gecerli olmayan kart bilgileri tespit edildi. Lutfen ayarlar sekmesinden bilgilerinizi kontrol ediniz.")
            return redirect('404')
        
        # eger hersey yolundaysa
        PurchaseLog.objects.create(user=request.user, product=satinAlinanUrun, card=kartBilgisi).save()
        # satin alinan urunun stokundan alinan adet kadar dusur
        adetSayisi = request.POST.get('urun_adet')
        satinAlinanUrun.stokAdet -= int(adetSayisi)
        # kaydet
        satinAlinanUrun.save()
        # session mesaj at
        messages.success(request, message="Basarili bir sekilde {urunAdi} satin alindi".format(urunAdi=satinAlinanUrun.ad))
        # urun sayfasina yonlendir
        return redirect('/urun/'+ str(urunId))

        
    else:
        # get istegi
        return redirect('urunlerimiz')
       
# yorum yapma (API)
def makeComment(request, urunId):
    # urunu bul
    if request.method == "POST":
        urun = Urun.objects.get(id=urunId)
        if urun:
            # datalari cek
            message = request.POST.get('message')
            # author ve message urunun yorum kismina kayit at
            urun.yorumlar.create(yazar=request.user, mesaj=message).save()
            # urunun sayfasina yonlendir
            return redirect('/urun/' + str(urunId))
        else:
            # hata sayfasina yonlendir
            return redirect('404')
    else:
        # get istekleri icin
        return redirect('/urun/' + str(urunId))
    

# yorum duzenleme
from .form import EditComment
def editComment(request, urunId, yorumId):
    context = {}
    yorum_data = Yorum.objects.filter(id=yorumId).first()

    if yorum_data is None:
        # bulunamadi sayfasina yonlendir
        return redirect('404')

    # 3. kisi manipule etmeye calisiyorsa ve bu kisi admin degilse
    if request.user.id != yorum_data.yazar.id and request.user.is_superuser is not True:
        raise PermissionDenied()


    # kontroller, guvenlik ve get, filter farki
    if request.method == "POST":
        editForm = EditComment(request.POST, instance=yorum_data)
        if editForm.is_valid():
            # veritabanini guncelle
            editForm.save()

        # yorumun oldugu yere yonlendir
        return redirect('/urun/' + str(urunId))
    
    else:
        # get istegi gelirse
        context['productId'] = urunId
        context['commentId'] = yorumId
        context['form'] = EditComment(instance=yorum_data)
        return render(request, 'comment/edit_comment.html', context)
    
    
# yorum silme (API)
def deleteComment(request, urunId, yorumId):
    
    yorum_data = Yorum.objects.filter(id=yorumId).first()

    if yorum_data is None:
        return redirect('404')
    
    # 3. kisi manipule etmeye calisiyorsa ve bu kisi admin degilse
    if request.user.id != yorum_data.yazar.id and request.user.is_superuser is not True:
        raise PermissionDenied()
    
    # yorumu sil
    yorum_data.delete()
    # sayfaya yonlendir
    # session messages
    messages.success(request, 'Basarili bir sekilde mesaj silindi')

    return redirect('/urun/' + str(urunId))

