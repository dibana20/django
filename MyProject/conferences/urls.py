from django.urls import path
from .views import *


urlpatterns= [
    path('list/',conferenceList,name="listconf"),
    path('ConferenceListView/',ConferenceListView.as_view(),name='listViewconf'),
    path('Details/<int:pk>/', DetailsViewConference.as_view(), name='confDetail')

]