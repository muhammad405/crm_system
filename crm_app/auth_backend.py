from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username != 'admin' or password != '1':
            return None
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            # Agar foydalanuvchi topilmasa, yangi foydalanuvchi yaratish
            user = User(username=username)
            user.set_password(password)
            user.save()
            return user