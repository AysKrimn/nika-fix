from django import forms
from .models import *

class CreateUrun(forms.ModelForm):
    class Meta:
        model=Urun
        fields=["ad", "urundetayi", "fiyat", "stokAdet", "urunResmi" ]

        help_texts = {
            "fiyat": None
        }


# forum olustur
class EditComment(forms.ModelForm):
    class Meta:
        model=Yorum
        fields=['mesaj']

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = UserCreditCard
        fields = ['cardNo', 'cardOwner', 'expiredMonthAndYear', 'cvc']

# randevu
class GetReservation(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['tel', 'email', 'date']
