from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('function/', views.hello_world),
    path('class/', views.Helloethopia.as_view()),
     path('reservation/', views.home), 
]
