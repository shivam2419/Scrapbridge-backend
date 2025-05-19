from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.http import JsonResponse
# from .predict import classify_image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from social_django.utils import psa
import razorpay
from EWaste.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from rest_framework.permissions import IsAdminUser

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

@api_view(['GET'])
@permission_classes([])
def delete_all_tokens(request):
    count, _ = OutstandingToken.objects.all().delete()
    print("Deleted all tokens")
    return JsonResponse({'message': f'Deleted {count} tokens'})

@api_view(['GET'])
@permission_classes([])  # or use [] to remove auth for testing
def list_tokens(request):
    tokens = OutstandingToken.objects.all()
    return Response({
        'total_tokens': tokens.count(),
        'tokens': [
            {
                'user_id': token.user_id,
                'jti': token.jti,
                'created_at': token.created_at,
                'expires_at': token.expires_at,
            } for token in tokens
        ]
    })
# conn = http.client.HTTPSConnection("mail-sender-api1.p.rapidapi.com")
# headers = {
#     'x-rapidapi-key': "41f8c5c26emsh33af3107ae7eb1fp165595jsnd6e414bce373",
#     'x-rapidapi-host': "mail-sender-api1.p.rapidapi.com",
#     'Content-Type': "application/json"
# }
@api_view(['GET'])
def checkAuthentication(request):
    user = request.user
    IsAuthenticated = True if user.is_authenticated else False
    return Response({'isAuthenticated': IsAuthenticated}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    API to get logged-in user details.
    """
    user = request.user
    role = 'user' if hasattr(user, 'enduser') else 'recycler'
    try:
        if role == 'user':
            userProfile = user.enduser.image.url if user.enduser.image else None
        else:
            userProfile = user.owner.image.url if user.owner.image else None
    except Exception as e:
        userProfile = None  # fallback if image is missing or error occurs

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role,
        "user_profile": userProfile,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API to register a new user with email & password.
    OAuth users should register via Google.
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role")

    if not username or not email or not password or not role:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if role not in ['user', 'recycler']:
        return Response({"error": "Invalid role specified"}, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)

    if role == 'user':
        enduser = endUser.objects.create(user=user, phone="123456")
    elif role == 'recycler':
        owner = Owner.objects.create(user=user, organisation_name=username)

    return Response({
        "message": "User registered successfully. Please log in to get tokens.",
    }, status=status.HTTP_201_CREATED)

# Google login : Takes access token : user information
@api_view(['POST'])
@permission_classes([AllowAny])
@psa('social:complete')
def google_login(request, backend):
    """
    Accepts Google OAuth token, logs in user, and assigns role (Simple User or Recycler).
    """
    token = request.data.get("access_token")
    user_type = request.data.get("user_type")  # Expect 'user' or 'recycler'

    if not token:
        return Response({'error': 'Access token is required'}, status=400)

    user = request.backend.do_auth(token)

    if user and user.is_active:
        login(request, user)  # Create session

        # Check if the user already has a role
        if endUser.objects.filter(user=user).exists():
            role = "user"
        elif Owner.objects.filter(user=user).exists():
            role = "recycler"
        else:
            # New user, assign role based on user input
            if user_type == "user":
                endUser.objects.create(user=user, phone="1234567890")
                role = "user"
            elif user_type == "recycler":
                Owner.objects.create(user=user, organisation_name=user.username, phone="1234567890")
                role = "recycler"
            else:
                return Response({'error': 'Invalid user type'}, status=400)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": role
            }
        }, status=200)
    
    return Response({'error': 'Invalid token'}, status=400)

# Scrap classifier : Takes image of scrap : predicted class and accuracy
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def classify_image_view(request):
#     serializer = ImageUploadSerializer(data=request.data)
    
#     if serializer.is_valid():
#         image = serializer.validated_data['image']
        
#         try:
#             # Save the image and get the path
#             image_path = default_storage.save(image.name, image)
            
#             # Get the full path to the image
#             full_image_path = os.path.join(default_storage.location, image_path)
            
#             # Call your classification function
#             result = classify_image(full_image_path)  # Adjust based on your function
            
#             # Delete the image after processing
#             if os.path.exists(full_image_path):
#                 os.remove(full_image_path)
            
#             return Response({'classification': result}, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User role : Take user_id : Return whether user is Recycler or Simple user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request, user_id):
    """
    API to return the role of the logged-in user.
    """
    user = User.objects.get(id = user_id)
    role = "unknown"

    if endUser.objects.filter(user=user).exists():
        role = "user"
    elif Owner.objects.filter(user=user).exists():
        role = "recycler"

    return Response({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": role
    })

# Owner details : Takes recycler id : return data about specific recycler
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ownerDetails(request, user_id):
    try:
        user = User.objects.get(pk = user_id)
        owner = Owner.objects.get(user = user)
        serializer = OwnerSerializer(owner)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except Owner.DoesNotExist:
        return Response({"Error":"Owner does not exist"}, status=status.HTTP_404_NOT_FOUND)

# User detail : Takes user id : return data about specific user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDetails(request, user_id):
    try:
        user = User.objects.get(id = user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"Error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def endUserDetails(request, enduser_id):
    try:
        enduser = endUser.objects.get(enduser_id = enduser_id)
        user = enduser.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"Error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEndUserDetails(request, user_id):
    try:
        user = User.objects.get(pk = user_id)
        enduser = endUser.objects.get(user = user)
        serializer = EndUserSerializer(enduser)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"Error":"User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        print(user)
        enduser = None
        owner = None

        # Update related profile models
        if hasattr(user, 'enduser'):
            enduser = endUser.objects.get(user=user)
        elif hasattr(user, 'owner'):
            owner = Owner.objects.get(user=user)
            owner.phone = request.data.get("phone", owner.phone)
            owner.street = request.data.get("street", owner.street)
            owner.city = request.data.get("city", owner.city)
            owner.state = request.data.get("state", owner.state)
            owner.zipcode = request.data.get("zipcode", owner.zipcode)
            owner.save()

        # Update email in User model
        email = request.data.get("email")
        if email:
            user.email = email
            user.save()

        # Serialize and update profile
        if enduser:
            serializer = EndUserSerializer(enduser, data=request.data, partial=True)
        elif owner:
            serializer = OwnerSerializer(owner, data=request.data, partial=True)
        else:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User info updated successfully!",
                "data": serializer.data,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# All owners detail : Takes nothing : returns all the owner available
@api_view(['GET'])
@permission_classes([AllowAny])
def getOwnerDetails(request):
    try:
        owner = Owner.objects.all()
        serializer = OwnerSerializer(owner, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'Error':'Some error occured'}, status=status.HTTP_404_NOT_FOUND)

# All users detail : Takes nothing : returns all the user available (not needed API, gonna kill)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    try:
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'Error':'Some error occured'}, status=status.HTTP_404_NOT_FOUND)
        
# Submit pickup request : Takes pickup specific data : return true/false response and send pickup request to recycler
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_scrap_request(request):
    mutable_data = request.data.copy()  # QueryDict ko mutable bana le

    # User ko endUser model se uthakar daal
    try:
        enduser = endUser.objects.get(user=request.user)
        mutable_data['user'] = enduser.enduser_id  # ID pass karni hai
    except endUser.DoesNotExist:
        return Response({"error": "EndUser not found"}, status=400)

    # Organisation ka ID uthakar object ka ID daal
    try:
        organisation_id = request.data.get('organisation')
        organisation = Owner.objects.get(organisation_id=organisation_id)
        mutable_data['organisation'] = organisation.pk
    except (KeyError, Owner.DoesNotExist):
        return Response({"error": "Valid organisation ID required"}, status=400)

    # Ab serialize karle
    serializer = RecycleFormSerializer(data=mutable_data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Scrap request submitted successfully!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Registration for any query : Takes email id : sends query of user to admin
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_details(request):
    serializer = ContactFormSerializer(data=request.data)  # Corrected serializer
    if serializer.is_valid():
        serializer.save()
        return Response({'message' : 'Contact details submitted successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response({'Error' : 'Contact details not submitted'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])  # Also fix POST casing
@permission_classes([IsAuthenticated])
def showNotifications(request):
    try:
        pk = request.data.get("user_id")
        user = User.objects.get(pk = pk)
        enduser = endUser.objects.get(user=user)
        data = Notification.objects.filter(user=enduser)

        # Yeh tha error: data= wrong tha yahan
        serializer = NotificationSerializer(instance=data, many=True)

        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# All orders of specific recycler : Takes recycler id : return all the orders of that recycler
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllOrders(request, user_id):
    try:
        user = User.objects.get(pk = user_id)
        owner = Owner.objects.get(user = user)
        data = RecycleForm.objects.filter(organisation = owner, status = False)
        serializer = RecycleFormSerializer(data, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:  # Catch all errors instead
        return Response({'Error': f'Some error occurred: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

# All pending orders of specific recycler : Takes recycler id : return all the orders of that recycler
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllPendingOrders(request, user_id):
    try:
        user = User.objects.get(pk = user_id)
        owner = Owner.objects.get(user = user)
        print(owner)
        data = RecycleForm.objects.filter(organisation = owner, status = True)
        serializer = RecycleFormSerializer(data, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:  # Catch all errors instead
        return Response({'Error': f'Some error occurred: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

# Detail of specific order : Takes order_id : return all the details regarding that order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderDetail(request, order_id):
    try:
        recycle_data = RecycleForm.objects.get(order_id=order_id)

        # Fetch the user using the user_id from the recycle_data
        user = User.objects.get(enduser=recycle_data.user)  # Assuming user_id is a field in RecycleForm
        
        # Add the username to the serializer data
        recycle_data_serialized = RecycleFormSerializer(recycle_data)
        response_data = recycle_data_serialized.data
        response_data['user'] = user.username  # Add the username to the response
        
        return Response({'data': response_data}, status=status.HTTP_200_OK)

    except RecycleForm.DoesNotExist:
        return Response({'Error': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'Error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Order acceptance : Takes order id : return true/false
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderAccepted(request, order_id):
    try:
        recycle_data = get_object_or_404(RecycleForm, order_id=order_id)  # Ensure object exists
        owner = recycle_data.organisation  # Corrected organisation reference
        enduser = recycle_data.user if recycle_data.user else None
        if(enduser == None): 
            return Response({'data':'Some error occured'}, status=status.HTTP_400_BAD_REQUEST)
        data = f"Your request has been accepted by {owner.organisation_name}. " \
            f"Delivery will arrive soon.\nScrap collector: {owner.user.username}\nEmail: {owner.user.email}"
        Notification.objects.create(status=True, user=enduser, message=data)
        recycle_data.status = True  # Remove order after acceptance
        print(recycle_data)
        recycle_data.save()
        return Response({'data': 'Order accepted'}, status=status.HTTP_200_OK)
    except:
        return Response({'data':'Some error occured'}, status=status.HTTP_400_BAD_REQUEST)
    
# Order rejected : Takes order id : return description of rejection
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def orderRejected(request, order_id):
    try:
        try:
            recycle_obj = RecycleForm.objects.get(order_id=order_id)
        except RecycleForm.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        print(order_id)
        reason = f"Your request has been rejected by {recycle_obj.organisation.user.username}. Scrap collector said '{request.data.get('reason')}'"
        print(reason)
        enduser = recycle_obj.user
        obj = Notification.objects.create(status = status, user = enduser, message = reason)
        recycle_obj.delete()

        return Response({'message': 'Order rejected successfully.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makePayment(request):
    # Assume you're passing amount in query params, e.g., ?amount=50000
    order_amount = int(request.data.get('amount'))  # amount in paise
    order_currency = 'INR'
    print(order_amount)
    # Create order with Razorpay
    payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))

    return JsonResponse({
        'payment_id': payment_order['id'],
        'amount': order_amount,
        'api_key': RAZORPAY_API_KEY
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def addPaymentStatus(request, order_id, username, owner_id, amount, transaction_id):
    try:
        enduser = User.objects.get(username = username).enduser
        print(enduser)
        owner = User.objects.get(pk = owner_id).owner
        data = f"Payment of {amount} received by {owner.user.username}"
        print("owner id", owner)
        print("data", data)
        Notification.objects.create(status = True, user = enduser, message = data)
        Payments.objects.create(user = enduser, owner = owner, transaction_id = transaction_id, amount = amount)
        recycle_obj = RecycleForm.objects.get(order_id = order_id)
        recycle_obj.delete()
        return Response({"Success" : "Payment done"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Successful payments : Takes user id and return all the payments done by a specific scrap collector
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def successfulPayments(request, user_id):
    try:
        user = User.objects.get(pk = user_id)
        owner = Owner.objects.get(user=user)
        allTransactions = Payments.objects.filter(owner = owner)
        serializer = PaymentsSerializer(allTransactions, many = True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Non api work


def index(request):
    return render(request, 'index.html')

