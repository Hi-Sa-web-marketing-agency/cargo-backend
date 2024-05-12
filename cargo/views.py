from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from cargo.models import Notification,Enquiry
from .serializers import EnquirySerializer
from django.views.decorators.csrf import csrf_exempt


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
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will set the default status as 'pending'
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
