from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('match/add/', views.add_match, name='add_match'),
    path('match/edit/<int:match_id>/', views.edit_match, name='edit_match'),
    path('match/delete/<int:match_id>/', views.delete_match, name='delete_match'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
]