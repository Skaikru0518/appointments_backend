from django.contrib import admin
from .models import Client, Appointments, Workers

# Register your models here.
# admin.site.register(Client)
# admin.site.register(Appointments)
@admin.register(Workers)
class Workers(admin.ModelAdmin):
    list_display = ('nev', 'added_at')
    search_fields = ('nev',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nev', 'email', 'phone', 'created_at')
    search_fields = ('nev', 'email', 'phone')
    list_filter = ('created_at','masseur',)
    ordering = ('nev',)


@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_client_phone', 'get_client_masseur', 'get_client_appointment', 'status')
    list_filter = ('status',)
    ordering = ('-date_time',)  # Csökkenő sorrend dátum szerint
    search_fields = ('nev__nev', 'nev__phone')

    def get_client_name(self, obj):
        return obj.nev.nev
    get_client_name.short_description = 'Név'

    def get_client_phone(self, obj):
        return obj.nev.phone
    get_client_phone.short_description = 'Telefonszám'

    def get_client_masseur(self, obj):
        return obj.nev.masseur
    get_client_masseur.short_description = 'Masszőr'

    def get_client_appointment(self, obj):
        return obj.date_time
    get_client_appointment.short_description = 'Foglalt időpont'


    

    

