from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('room/<slug>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<slug>/', views.updateRoom, name="update-room"),
    path('delete-room/<slug>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),



    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]
