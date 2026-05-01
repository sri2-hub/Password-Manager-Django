from django.urls import path
from . import views

app_name = 'vault'      # ← important

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),  # your login
    path('logout/', views.user_logout, name='logout'),
    path('passwords/', views.password_list, name='password_list'),
    path('add/', views.add_password, name='add_password'),
    path('reveal/<int:entry_id>/', views.reveal_password, name='reveal_password'),
]