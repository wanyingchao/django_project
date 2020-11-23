from django.urls import path, include
from all_app import views

urlpatterns = [
    path('hello_word/', views.hello_word),
    path('select/', views.select),
    path('index/', views.get_index_page),
    path('pop_all/', views.pop_all),
    path('device_detail/', views.device_detail),
    path('device_statics/', views.device_statics),
    path('select_signal/', views.select_signal),
    path('device_index/', views.get_device_index_page),
    path('pop_index/', views.get_pop_index_page),
    path('signal_index/', views.get_signal_index_page),
]