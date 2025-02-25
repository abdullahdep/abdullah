from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_list, name='data_list'),
    path('('', views.data_list, name='data_list'),
    path('add/', views.add_data, name='add_data'),
    path('edit/<int:pk>/', views.edit_data, name='edit_data'),
    path('delete/<int:pk>/', views.delete_data, name='delete_data'),
    path('download/<int:pk>/', views.download_data, name='download_data'),
    path('share/<int:pk>/', views.share_data, name='share_data'),
]

