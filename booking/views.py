
# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from urunApp.models import *
from urunApp.form import GetReservation

# Randevu Sayfasi
def randevu(request):
    

    return render(request, 'randevu.html')



def makeRandevu(request, randevuId):
    print("ID:", randevuId)
    if request.method == 'POST':
        randevuId = int(randevuId)        
        # form = GetReservation(request.POST)
        # if form.is_valid():
            
        #     form = form.save(commit=False)
        #     form.user = request.user
        #     form.save()
        #     return redirect('randevu')
        # else:
        #     # session mesaj oluştur öyle gönder
        #     return redirect('404')

        rezervasyonItem = Reservation.objects.filter(id=randevuId).first()
        MakeAppointment.objects.create(user=request.user, rezervasyon=rezervasyonItem).save()
        return redirect('randevu')
    
    else:
          return redirect('anasayfa')

# Randevu Olusturma
# def reservation(request):
#     context = {}
#     reservationSystem = GetReservation()

#     # post istegi gelirse
#     if request.method == "POST":
#         randevuOlustur = request.POST.get('_randevuOlustur')
        
#         if randevuOlustur.is_valid():
#             reservationSystem = GetReservation(request.POST)
#             reservationSystem =reservationSystem.save(commit=False)
#             reservationSystem.user = request.user
#             reservationSystem.save()
#             return redirect('randevu')
#         else:
#             print('hatalar:', reservationSystem.errors.as_data())
#             messages.error(request, 'Uzgunuz randevunuz olusturulamadi. Daha sonra tekrardan deneyiniz')
#             return redirect('404')






# user kayit olursa
def reservation(request):
    context = {}
    randevuForm = GetReservation()
    if request.method == 'POST':
        pass

    else:
        context['form'] = randevuForm
        reservations = Reservation.objects.all()
        context["reservations"] = reservations


        return render(request, 'randevu.html', context)
