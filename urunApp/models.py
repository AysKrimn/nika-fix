from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# veritabani modelleri

class Urun(models.Model):
    # database fields
    # django her class icin otomatik  id fieldi atar
    
    ad = models.CharField(("Urunun adi"), max_length=50)
    urundetayi = models.TextField(verbose_name="Urun Hakkinda aciklama", max_length=200)
    fiyat = models.CharField(("Urunun Fiyati"), default="Ucret belirtilmedi", max_length=6)
    urunResmi = models.FileField(("Urunun Resmi"), upload_to="uploads", max_length=100, null=True, blank=True)
    stokAdet = models.PositiveBigIntegerField(("Stoktaki adet sayisi"), default=1)
   
    # meta verisi
    def __str__(self):
        return "{ad} | {urunFiyat}".format(ad=self.ad, urunFiyat=self.fiyat)
    
        
    def adAyarla(self):
        if self.stokAdet >= 1:
            return self.ad
        else:
            return "{urunAdi} ({durum})".format(urunAdi=self.ad, durum="TUKENDI")

        
    def stokKontrol(self):
        if self.stokAdet > 0:
            return "{miktar} adet".format(miktar=self.stokAdet)
        elif self.stokAdet == 0:
            return "Tukendi"
        
    def resimKontrol(self):
        if self.urunResmi:
            return self.urunResmi
        else:
            return "static/public/no-image.jpg"
        
    # yorum modeli

class Yorum(models.Model):
    product = models.ForeignKey(Urun, verbose_name=("Urun"), on_delete=models.CASCADE, related_name="yorumlar", default="")
    yazar = models.ForeignKey(User, verbose_name=("Yazar"), on_delete=models.CASCADE)
    mesaj = models.TextField(("Mesaj"), max_length=350)
    olusturuldu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.yazar.username
    
# kullanici karti
class UserCreditCard(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanici"), on_delete=models.CASCADE)
    cardNo = models.CharField(("Hesap Numarasi"), max_length=19)
    cardOwner = models.CharField(("Hesap Sahibi"), max_length=50)
    expiredMonthAndYear = models.CharField(("Gecerlilik Suresi"), max_length=5)
    cvc = models.CharField(("Guvenlik Kodu"), max_length=3)

# satin alma
class PurchaseLog(models.Model):
    user = models.ForeignKey(User, verbose_name=("Satin Alan Kisi"), on_delete=models.CASCADE)
    product = models.ForeignKey(Urun, verbose_name=("Satin Alinan Urun"), on_delete=models.CASCADE)
    card = models.ForeignKey(UserCreditCard, verbose_name=("Islem Yapilan Kart"), on_delete=models.CASCADE)
    createdAt = models.DateTimeField(("Tarih"), auto_now=True)

# randevu olusturma
class Reservation(models.Model):
    user = models.ForeignKey(User, verbose_name=("Randevu Olusturan Kisi"), on_delete=models.CASCADE)
    title = models.CharField(("Adı"), max_length=50, null=True)
    tel = models.CharField(("Telefon Numarası"), max_length=50, null=True, blank=True)
    email = models.CharField(("Mail Adresi"), max_length=50, null=True, blank=True)
    date = models.DateField(("Tarih"), auto_now=False, auto_now_add=False)


class MakeAppointment(models.Model):
    user = models.ForeignKey(User, verbose_name=("Rezervasyonu Yapan Kişi"), on_delete=models.CASCADE)     
    rezervasyon = models.ForeignKey("urunApp.Reservation", verbose_name=("Rezervasyon Yapıldı"), on_delete=models.CASCADE)

