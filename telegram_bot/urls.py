from django.urls import path
from .views import (
    register_user, 
    login_user, 
    generate_telegram_token, 
    send_message_to_bot, 
    get_all_messages
)

urlpatterns = [
    path('generate_token/', generate_telegram_token, name='generate_token'),
    path('get_all_messages/', get_all_messages, name='get_all_messages'),
    path('send_message/', send_message_to_bot, name='send_message'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
]
