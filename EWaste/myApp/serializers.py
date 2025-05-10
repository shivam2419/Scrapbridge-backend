from rest_framework import serializers
from django.contrib.auth.models import User
from .models import endUser, QNA, Index_gmails, Owner, ContactForm, RecycleForm, Notification, Payments

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# End User Serializer
class EndUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = endUser
        fields = '__all__'

# QNA Serializer
class QNASerializer(serializers.ModelSerializer):
    class Meta:
        model = QNA  
        fields = '__all__'

# Index Gmails Serializer
class IndexGmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index_gmails
        fields = '__all__'

# Owner Serializer
class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = '__all__'

# Contact Form Serializer
class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

# Recycle Form Serializer
class RecycleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecycleForm
        fields = ['item_type', 'date', 'phone', 'weight', 'image', 'user', 'organisation', 'order_id', 'location']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# Payments Serializer
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
