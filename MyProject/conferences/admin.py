from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import conferences  # Importation du modèle
from users.models import *
from django.db.models import Count

class ReservationInline(admin.StackedInline):
    model=reservation
    extra=1
    readonly_fields=('reservation_date',)
    #can_delete=True
#TabularInline affichage en tableau
#StackedInline affiche bi toul fouk b3adhhom
    
class ParticipantFilter(admin.SimpleListFilter):
    title = "Participant filter"
    parameter_name = "participants"

    def lookups(self, request, model_admin):
        return (
            ('0', 'No participants'),
            ('more', 'More participants'),
        )

    '''def queryset(self, request, queryset):
        if self.value() == '0':
            # Filter for conferences with no participants
            # pour faire le calcul on utilise annotate/participant_count est le retour de annotate
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        elif self.value() == 'more':
            # Filter for conferences with more than 0 participants
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        #__gt/__lt est un lookup
        return queryset
    '''
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(reservation__isnull=True)
        elif self.value() == 'more':
            # Define what 'more' should filter. This is a placeholder.
            return queryset.filter(reservation__isnull=False)
        return queryset




class DateFilter(admin.SimpleListFilter):
    title = "Date filter"
    parameter_name = "date"

    def lookups(self, request, model_admin):
        return (
            ('past', 'Past Conferences'),
            ('upcoming', 'Upcoming Conferences'),
            ('today', 'Today Conferences'),
        )

    def queryset(self, request, queryset):
        #.value() est le retour de lookups
        if self.value() == 'past':
            return queryset.filter(end_date__lt=timezone.now().date())
        elif self.value() == 'upcoming':
            return queryset.filter(start_date__gt=timezone.now().date())
        elif self.value() == 'today':
            return queryset.filter(start_date=timezone.now().date())
        return queryset

class ConfAdmin(admin.ModelAdmin):
    list_display = ('titre', 'location', 'start_date', 'end_date', 'price', 'category') 
    search_fields = ('titre',)
    list_per_page=2
    ordering=('start_date','titre')
    #ordre inverse ordering=('-start_date',)
    fieldsets = (
        ('Description', {
            'fields': ('titre', 'description', 'location', 'price', 'capacite', 'category'),
        }),
        ('Horraires', {
            'fields': ('start_date', 'end_date', 'created_at','update_at'),
        }),
        ('Documents', {
            'fields': ('program',),  
        }),
    )
    readonly_fields=('created_at','update_at')
    inlines=[ReservationInline]
    autocomplete_fields=('category',)
    list_filter=('titre',ParticipantFilter,DateFilter)
    list_display_links = ('titre', 'category',)
admin.site.register(conferences, ConfAdmin)
