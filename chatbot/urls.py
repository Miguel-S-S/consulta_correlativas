from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_experto, name='chat_experto'),
    path('reiniciar/', views.reiniciar_chat, name='reiniciar_chat'),
]