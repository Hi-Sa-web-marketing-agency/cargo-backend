from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from cargo.models import Notification,Enquiry,CustomUser
from .serializers import EnquirySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from datetime import datetime
import json
from django.contrib.auth import get_user_model

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')


        print(username,'---------------this is username')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


def get_notifications(request):
    user = request.user  # Assuming user is authenticated
    print(user,'----------this user----------')
    notifications = Notification.objects.all()
    data = [{'id': n.id, 'message': n.message, 'created_at': n.created_at} for n in notifications]
    # Mark notifications as read
    notifications.update(read=True)
    return JsonResponse({'notifications': data})

@csrf_exempt 
def Enquiry_post(request):
    if request.method == 'POST':
        # Extract data from the query parameters (GET request)
        data = json.loads(request.body) # This extracts data from the query parameters

        print(data,'---------------------this is data---------------------------')
        print(data,'---------------------this is data---------------------------')

        # Check if required fields are present
        required_fields = ['name', 'place']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Required field "{field}" is missing'}, status=400)

        # Parse data and create Enquiry instance
        name = data.get('name')
        place = data.get('place')
        pickup_date_str = data.get('pickup_date')
        pickup_time = data.get('pickup_time')
        phone = data.get('phone')
        mode = data.get('mode')
        driver = data.get('driver')
        salesman = data.get('salesman', None)
        if salesman is not None:
            check = salesman.split('-')
        else:
            pass
        salesman_id = check[0]
        salesman_name = check[1]
        print(salesman_id,'--------------------this is salesman id---------------')
        status = data.get('status', 'pending')  # Default to 'pending' if not provided

        try:
            pickup_date = pickup_date_str.split('T')[0]
        except ValueError:
            return JsonResponse({'error': 'Invalid pickup_date format'}, status=400)

        if salesman_id:
            try:
                salesman = CustomUser.objects.get(id=salesman_id)
            except:
                return JsonResponse({'error': 'Salesman not found'}, status=400)
        else:
                salesman = None


        # Create Enquiry instance
        enquiry = Enquiry(
            name=name,
            place=place,
            pickup_date=pickup_date,  # Ensure pickup_date is provided
            pickup_time=pickup_time,
            phone=phone,
            mode=mode,
            driver=driver,
            salesman=salesman,
            salesman_name=salesman_name,
            status=status,
            created_at=timezone.now()
        )

        # Save the Enquiry instance
        enquiry.save()

        # Return a JSON response with the created enquiry details
        return JsonResponse({'message': 'Enquiry created successfully', 'enquiry_id': enquiry.id}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# def Enquiry_get(request,pk):
#     try:
#         enquiry = Enquiry.objects.get(pk=pk)
#     except Enquiry.DoesNotExist:
#         return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = EnquirySerializer(enquiry)
#     return Response(serializer.data)

@csrf_exempt
def Enquiry_put(request, pk):
    if request.method == 'PUT':
        try:
            enquiry = Enquiry.objects.get(pk=pk)
        except Enquiry.DoesNotExist:
            return JsonResponse({'error': 'Enquiry not found'}, status=404)

        # Extract data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Check if required fields are present
        required_fields = ['name', 'place']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Required field "{field}" is missing'}, status=400)

        # Parse data
        name = data.get('name')
        place = data.get('place')
        pickup_date_str = data.get('pickup_date')
        pickup_time = data.get('pickup_time')
        phone = data.get('phone')
        mode = data.get('mode')
        driver = data.get('driver')
        salesman_id = data.get('salesman_id')
        status = data.get('status', 'pending')  # Default to 'pending' if not provided

        # Validate pickup_date format
        try:
            pickup_date = pickup_date_str.split('T')[0]
        except (ValueError, AttributeError):
            return JsonResponse({'error': 'Invalid pickup_date format'}, status=400)

        # Get salesman instance if salesman_id is provided
        if salesman_id:
            try:
                salesman = CustomUser.objects.get(id=salesman_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Salesman not found'}, status=404)
        else:
            salesman = None

        # Update Enquiry instance fields
        enquiry.name = name
        enquiry.place = place
        enquiry.pickup_date = pickup_date
        enquiry.pickup_time = pickup_time
        enquiry.phone = phone
        enquiry.mode = mode
        enquiry.driver = driver
        enquiry.salesman = salesman
        enquiry.status = status
        enquiry.updated_at = timezone.now()

        # Save the updated Enquiry instance
        enquiry.save()

        # Return a JSON response with the updated enquiry details
        return JsonResponse({'message': 'Enquiry updated successfully', 'enquiry_id': enquiry.id}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def enquiryList(request):
    enquiries = Enquiry.objects.all()

    data = []
    for enquiry in enquiries:
        # Serialize salesman data if available
        salesman_data = None
        if enquiry.salesman:
            salesman_data = {
                'id': enquiry.salesman.id,
                'username': enquiry.salesman.username,
                'email': enquiry.salesman.email,
                # Add more fields as needed
            }

        # Construct enquiry data dictionary
        enquiry_data = {
            'id': enquiry.id,
            'name': enquiry.name,
            'place': enquiry.place,
            'pickup_date': enquiry.pickup_date,
            'pickup_time': enquiry.pickup_time,
            'phone': enquiry.phone,
            'mode': enquiry.mode,
            'driver': enquiry.driver,
            'salesman': salesman_data,
            'status': enquiry.status,
            'created_at': enquiry.created_at,
        }

        data.append(enquiry_data)

    return JsonResponse({'data': data})


@csrf_exempt
def Enquiry_delete(request, pk):
    if request.method == 'DELETE':
        try:
            enquiry = Enquiry.objects.get(pk=pk)
        except Enquiry.DoesNotExist:
            return JsonResponse({'error': 'Enquiry not found'}, status=404)

        # Delete the Enquiry instance
        enquiry.delete()

        # Return a JSON response confirming deletion
        return JsonResponse({'message': 'Enquiry deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)