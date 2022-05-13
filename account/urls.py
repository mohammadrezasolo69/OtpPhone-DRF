from rest_framework.routers import DefaultRouter
from account  import views

app_name = 'account'
router = DefaultRouter()
router.register('', views.OTPViewSet, basename='otp')

urlpatterns = router.urls
