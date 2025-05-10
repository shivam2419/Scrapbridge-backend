from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# End User Model
class endUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enduser_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default=None)
    phone = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# QNA Model
class QNA(models.Model):
    questions = models.CharField(max_length=1000)
    answers = models.TextField()  # Use TextField for longer answers

# Index Gmails Model
class Index_gmails(models.Model):
    emails = models.EmailField(unique=True)  # Ensure unique emails

# Owner Model
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation_id = models.AutoField(primary_key=True)
    organisation_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)  # Change to CharField
    # Address section
    city = models.CharField(max_length=400, null=True, blank=True, default="")
    state = models.CharField(max_length=400, null=True, blank=True, default="")
    street = models.CharField(max_length=400, null=True, blank=True, default="")
    zipcode = models.CharField(max_length=20, null=True, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Contact Form Model
class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)  # Change to CharField
    message = models.TextField()

# Recycle Form Model
class RecycleForm(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(endUser, on_delete=models.CASCADE, null=True)  # ForeignKey
    organisation = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)  # ForeignKey
    item_type = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)  # Change to DateTimeField
    phone = models.CharField(max_length=16, null=True, blank=True)  # Change to CharField
    image = models.ImageField(upload_to='recycle_images/', null=True, blank=True)
    weight = models.IntegerField(null=True, default=0)
    location = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # Change to BooleanField

    class Meta:
        ordering = ['-created']

# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(endUser, on_delete=models.CASCADE, null=True)  # Use ForeignKey
    status = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        ordering = ['-created']

# Payments Model
class Payments(models.Model):
    user = models.ForeignKey(endUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=1)
    transaction_id = models.CharField(max_length=200, default=None, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Use DecimalField
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-created']