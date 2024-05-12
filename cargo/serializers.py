from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cargo.models import Enquiry
from django.utils import timezone

class EnquirySerializer(serializers.ModelSerializer):
    # salesman = serializers.CharField(source='salesman.username')  # Serialize salesman username

    class Meta:
        model = Enquiry
        fields = ['id', 'name', 'place', 'pickup_date', 'phone', 'mode', 'driver', 'salesman', 'status', 'created_at']

@api_view(['GET'])
def get_enquiries(request):
    enquiries = Enquiry.objects.all()
    serializer = EnquirySerializer(enquiries, many=True)
    return Response(serializer.data)