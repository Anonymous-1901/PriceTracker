from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('my-alerts/', views.my_alerts_view, name='my_alerts'),
    path('get_product_data/', views.get_product_data, name='get_product_data'),
    path('create-alert/',views.create_alert,name='create_alert')
]
