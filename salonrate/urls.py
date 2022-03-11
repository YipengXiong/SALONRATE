from django.urls import path
from salonrate import views

app_name = 'salonrate'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('salon/', views.salon_detail, name="salon"),
    path('service/', views.service_detail, name="service"),
    path('search_result/', views.search_result, name='search_result'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
