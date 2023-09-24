<h1 align="center">Telegram Django API</h1>

## Запуск

Сделано на Python версии 3.9.16.
1. Установите зависимости с помощью pip:

    ```
    pip install -r requirements.txt
    ```

2. В папке `configs` откройте файл `configs.py` и замените `<YOUR_TOKEN>` на токен вашего бота.

3. Запустите сервер с помощью команды:

    ```
    python manage.py runserver
    ```

## API Endpoints

- `api/register/` - Регистрация
- `api/login/` - Авторизация
- `api/generate_token/` - Генерация токена (необходимо предварительно отправить любое сообщение боту)
- `api/get_all_messages/` - Получение списка сообщений
- `api/send_message/` - Отправка сообщений
