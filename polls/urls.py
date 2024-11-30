from django.urls import path

# for the veiws with vynerabilities use the following import

from . import views
# for the views without vynerabilities use the following import
#from . import betterViews as views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
]