from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addMessages', views.addMessages, name='addMessages'),
    path('clearMessages', views.clearMessages, name='clearMessages'),
    path('login/', views.user_login, name='login'),
]