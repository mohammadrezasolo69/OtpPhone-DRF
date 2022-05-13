from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import OTP

from account.generate_otp import generate_code_opt

# ---------------------------------------------------------------------------------------------------

User = get_user_model()


class CustomTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = user.phone
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class ListUserSerializer(serializers.ModelField):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone']
        read_only_fields = ['id', ]


class SendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('phone',)

    def create(self, validated_data):
        """ create OTP """
        phone = validated_data['phone']
        otp = generate_code_opt()  # Generate otp code
        validated_data['otp'] = otp
        return super().create(validated_data)


class VerifyOtpSerializer(serializers.Serializer):
    # Request
    phone = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    # Response
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    new_user = serializers.BooleanField(read_only=True)

    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')

        if not OTP.objects.filter(
                phone=phone,
                otp=otp,
                created_at__gte=datetime.now() - timedelta(minutes=settings.OTP_EXPIRE_TIME)).exists():
            raise serializers.ValidationError('OTP invalid')
        return data

    def create(self, validated_data):
        phone = validated_data.get('phone')

        user, created = User.objects.get_or_create(phone=phone, defaults={'phone': phone, 'is_phone_verified': True})
        if not created:
            if not user.first_name:
                created = True
            if not user.is_phone_verified:
                user.is_phone_verified = True
                user.save()

        validated_data['new_user'] = created

        # generate JWT Token
        refresh = CustomTokenObtain.get_token(user)
        access = refresh.access_token

        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(access)

        return validated_data
