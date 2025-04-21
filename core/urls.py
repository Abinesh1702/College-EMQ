from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('img/', views.candidate),
    path('person/', views.person, name='person'),
    path('candidates/', views.candidate_table, name='candidate_table'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('generate-qr/<int:pk>/', views.generate_qr_code, name='generate_qr_code'),
    path('register/', views.voter_register, name='voter_register'),
    path('generate-vote-qrcode/', views.generate_vote_qr_code, name='generate_vote_qr_code'), 
    path('vote/', views.vote, name='vote'), 
    path('voters-list/',views.total_voters,name='voters-list'),
    path('regiter-voters/',views.register_voters,name='voters-reg')
]
