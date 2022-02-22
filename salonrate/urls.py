from django.urls import path
from salonrate import views

app_name = 'salonrate'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('salon_detail/', views.salon_detail, name="salon_detail"),
    path('service_detail/', views.service_detail, name="service_detail"),
    path('search_result/', views.search, name='search'),
    # path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    # path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]