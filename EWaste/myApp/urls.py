from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# Define router for ViewSets
router = DefaultRouter()
urlpatterns = [
    # JWT tokens url
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/delete-tokens/', views.delete_all_tokens),
    path('api/list-tokens/', views.list_tokens),
    # Authentication url's
    path('auth/', include('social_django.urls')), 
    path('api/auth/user/', views.get_current_user, name='current-user'), #✅
    path('api/check-authentication/', views.checkAuthentication, name='check-authentication'), #✅
    # Google Authentication url's 
    path('auth/google/<str:backend>/', views.google_login, name='google-login'),
    path('auth/social/', include('allauth.socialaccount.urls')), 

    # user api's
    path('api/register-user/', views.register_user, name='register-user'), #✅
    path('api/user/<int:user_id>/', views.userDetails, name='get-user-details'), #✅
    path('api/enduser/<int:enduser_id>/', views.endUserDetails, name='get-endusers-user-details'), #✅
    path('api/get-enduser/<int:user_id>/', views.getEndUserDetails, name='get-enduser-details'), #✅
    path('api/update-user/<int:user_id>/',views.update_user, name='update-user'), #✅
    path('api/users/', views.getUserDetails, name='get-all-users'), #✅
    path('api/scrap-request/', views.submit_scrap_request, name='scrap-request'), #✅
    path('api/contact-us/', views.submit_contact_details, name='contact-submit'), #✅
    path('api/notifications/', views.showNotifications, name='notifications'), #✅

    # owner api's
    path('api/owners/', views.getOwnerDetails, name='get-all-owners'), #✅
    path('api/owner/<int:user_id>/', views.ownerDetails, name='get-owner-details'), #✅
    path('api/order-details/<int:user_id>/', views.getAllOrders, name='order-details'), #✅
    path('api/user-order-detail/<str:order_id>/', views.getOrderDetail, name='order-detail'), #✅
    path('api/user-pending-order-detail/<int:user_id>/', views.getAllPendingOrders, name='user-pending-order-details'), #✅
    path('api/order-accept/<str:order_id>/', views.orderAccepted, name='order-accepted'), #✅
    path('api/order-reject/<str:order_id>/', views.orderRejected, name='order-reject'), #✅
    path('api/transaction-details/<int:user_id>/', views.successfulPayments, name='order-reject'), #✅
    path('api/payment/', views.makePayment, name='make-payment'), #✅
    path('api/payment-status/<str:order_id>/<str:username>/<int:owner_id>/<int:amount>/<str:transaction_id>/', views.addPaymentStatus, name='add-payment-status'), #✅
    # Image classification url
    # path('api/classify-image/', views.classify_image_view, name='classify-image'), #✅
    path('api/send-mail/', views.sendMail, name='send-mail'),
    # core django path
    path('', views.index, name='index'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

