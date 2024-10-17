from django.contrib import admin
from .models import participant,reservation

# Register your models here.

class ReservationInline(admin.StackedInline):
    model=reservation
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True

class ConfUser(admin.ModelAdmin):
    list_display = ('cin', 'email', 'first_name', 'last_name', 'username','participant_category','created_at','update_at') 
    search_fields = ('username',)
    list_per_page=5
    ordering=('created_at',)
    fieldsets = (
        ('login', {
            'fields': ('cin', 'email'),
        }),
        ('other infos', {
            'fields': ('first_name', 'last_name', 'username','participant_category'),
        }),
        
    )
    readonly_fields=('created_at','update_at')
    list_filter=('participant_category',)
    list_editable = ('first_name', 'last_name')
    inlines=[ReservationInline]
    list_display_links = ('cin',)
    date_hierarchy = 'created_at'
    prepopulated_fields = {'username': ('first_name', 'last_name',)}




admin.site.register(participant,ConfUser)
admin.site.register(reservation)


