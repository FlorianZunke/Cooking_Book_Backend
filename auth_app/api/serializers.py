from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import job_send_activation_mail
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_confirmed_password(self, value):

        data = self.get_initial()
        password = data.get("password")
        confirmed_password = value

        if password != confirmed_password:
            raise serializers.ValidationError("Passwords do not match.")
        return value
    
    def validate_email(self, value):
        """
        Check that the email is unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bitte überprüfe deine Eingaben und versuche es erneut.")
        return value
    
    def save(self, **kwargs):
        """
        Create a new user with the provided email and password, set the user as inactive, generate an activation token, and send an activation email.
        """
        user = User.objects.create_user(
            username=self.validated_data['email'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            is_active=False
        )
        user.set_password(self.validated_data['password'])
        user.save() 

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        user.activation_token = token
        user.activation_uid = uid

        activation_link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"
        try:
            job_send_activation_mail(user.email, activation_link)
        except Exception as e:
            print(f"Mail-Fehler: {e}")
    
        return user