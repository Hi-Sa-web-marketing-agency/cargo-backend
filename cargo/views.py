from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from cargo.models import Notification

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
    # user = request.user  # Assuming user is authenticated
    notifications = Notification.objects.all()
    data = [{'id': n.id, 'message': n.message, 'created_at': n.created_at} for n in notifications]
    # Mark notifications as read
    notifications.update(read=True)
    return JsonResponse({'notifications': data})

