from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Messages

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Динамический сериализатор с возможностью указания полей для отображения
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class UserProfileSerializer(DynamicFieldsModelSerializer):
    """
    Сериализатор для регистрации
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name')
        
class TelegramDataSerializer(serializers.Serializer):
    class Meta:
        telegram_token = serializers.CharField(max_length=100, required=True)

class MessagesSerializer(DynamicFieldsModelSerializer):
    #message = serializers.CharField(max_length=1000, required=True)
    class Meta:
        model = Messages
        fields = '__all__' 


        