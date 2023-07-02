from django.contrib import admin
from .models import *
# Modellerini admin sayfasina kayit et
admin.site.register(Urun)
admin.site.register(Yorum)
admin.site.register(UserCreditCard)
admin.site.register(PurchaseLog)
admin.site.register(Reservation)
admin.site.register(MakeAppointment)
