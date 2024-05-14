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
        salesman_id = data.get('salesman_id')
        print(salesman_id,'--------------------this is salesman id---------------')
        status = data.get('status', 'pending')  # Default to 'pending' if not provided

        try:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date() if pickup_date_str else None
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
            status=status,
            created_at=timezone.now()
        )

        # Save the Enquiry instance
        enquiry.save()

        # Return a JSON response with the created enquiry details
        return JsonResponse({'message': 'Enquiry created successfully', 'enquiry_id': enquiry.id}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def Enquiry_get(request,pk):
    try:
        enquiry = Enquiry.objects.get(pk=pk)
    except Enquiry.DoesNotExist:
        return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EnquirySerializer(enquiry)
    return Response(serializer.data)

def Enquiry_put(request, pk,):
    try:
        enquiry = Enquiry.objects.get(pk=pk)
    except Enquiry.DoesNotExist:
        return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EnquirySerializer(enquiry, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def enquiryList(request):
    enquiries = Enquiry.objects.all()
    data = []

    for enquiry in enquiries:
        # Serialize the salesman field using a nested serializer
        
        # Construct the enquiry data dictionary
        enquiry_data = {
            'id': enquiry.id,
            'name': enquiry.name,
            'place': enquiry.place,
            'pickup_date': enquiry.pickup_date,
            'phone': enquiry.phone,
            'mode': enquiry.mode,
            'driver': enquiry.driver,
            'salesman': enquiry.salesman.id,  # Include serialized salesman data
            'status': enquiry.status,
            'created_at': enquiry.created_at
        }

        data.append(enquiry_data)
    print(data)

    return JsonResponse({'enquiries': data})
