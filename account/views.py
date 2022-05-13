from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from account.models import OTP
from account.serializers import ListUserSerializer, SendOtpSerializer, VerifyOtpSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = OTP.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return SendOtpSerializer
        return VerifyOtpSerializer

    @action(detail=False, methods=['POST'], url_path='verify')
    def verify_otp(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
