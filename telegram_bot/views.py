from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer, TelegramDataSerializer, MessagesSerializer
from configs.configs import url_get_updates, url_send_message, message_text
from .models import TelegramData, Messages
import requests

@api_view(['POST'])
def register_user(request):
    """
    Регистрация пользователя
    """
    
    serializer = UserProfileSerializer(data=request.data, fields=["username", "password", "first_name"])
    if serializer.is_valid():
        User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name']
        )
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Авторизация пользователя
    """
    
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_telegram_token(request):
    """
    Генерация токена телеграм и привязка к пользователю
    """
    
    serializer = TelegramDataSerializer(data=request.data)
    if serializer.is_valid():
        answer = requests.get(url_get_updates).json()
        telegram_token = request.data.get('telegram_token')
        
        for message in answer["result"]:
            if message["message"]["text"] == telegram_token:
                user = request.user  
    
                # Проверка если токен уже существует у пользователя
                try:
                    telegram_data = TelegramData.objects.get(user=user)
                    return Response({'token': telegram_data.telegram_token}, status=status.HTTP_200_OK)
                except TelegramData.DoesNotExist:
                    pass
    
                telegram_token = request.data.get('telegram_token')
    
                # Если токен не уникальный
                if TelegramData.objects.filter(telegram_token=telegram_token).exists():
                    return Response({'error': 'Telegram token already exists. Try another one'}, status=status.HTTP_400_BAD_REQUEST)
    
                # Привязка токена к пользователю
                telegram_data = TelegramData.objects.create(
                    user=user,
                    telegram_token=telegram_token,
                    telegram_chat_id=message["message"]["from"]["id"]  # You may want to set this as needed
                )
    
                return Response({'token': telegram_data.telegram_token}, status=status.HTTP_201_CREATED)
        return Response({'error': "Can't find your token. Send a message to the bot and try to generate again."}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_to_bot(request):
    """
    Отправка сообщений в телеграм
    """
    
    serializer = MessagesSerializer(data=request.data, fields=['message'])
    if serializer.is_valid():
        user = request.user
        telegram_data = TelegramData.objects.get(user=user)
        message = message_text.replace("1", user.first_name).replace("2", request.data.get('message'))
        chat_id = telegram_data.telegram_chat_id
        
        response=requests.get(url_send_message+f"?chat_id={chat_id}&text={message}").json()
        
        Messages.objects.create(
            user=user,
            message=request.data.get('message'),
            time=response["result"]["date"]
        )
        
        return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    """
    Получение всех сообщений пользователя
    """
    
    try:
        messages = Messages.objects.filter(user = request.user)
        serialized_messages = MessagesSerializer(messages, many=True, fields=["message", "time"]).data
        return Response(serialized_messages, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Could not retrieve messages. Error: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)