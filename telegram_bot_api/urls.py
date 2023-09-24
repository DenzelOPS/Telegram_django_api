from django.urls import path, include

urlpatterns = [
    # ... другие URL-пути ...
    path('api/', include('telegram_bot.urls')),
]
