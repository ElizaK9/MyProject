from django.urls import path
from . import views

app_name = 'LearnCard'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/',views.start_session, name='start_session'),
    path('card/<int:word_id>/', views.card_view, name='card_view'),
    path('done/', views.training_done, name='training_done'),
    path('alphabet/', views.alphabet, name='alphabet'),
    path('about/', views.about, name='about')
]