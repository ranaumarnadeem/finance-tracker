from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('toggle/<int:pk>/', views.toggle_checkbox_view, name='toggle-checkbox'),
    path('delete_all/', views.delete_all_view, name='delete-all'),
    path('send_emails/', views.send_email_view, name='send-emails'),
]
