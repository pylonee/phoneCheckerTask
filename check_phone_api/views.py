from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PhoneRange
from .serializers import PhoneSerializer, PhoneRequestSerializer

class PhoneInfoAPIView(APIView):

    def get(self, request):
        return render(request, 'check_phone_api/index.html')

    def post(self, request):
        serializer = PhoneRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Ошибка валидации',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        phone = serializer.validated_data['phone']

        try:
            phone_int = int(phone)
        except ValueError:
            return Response(
                {'error': 'Некорректный номер телефона'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            phone_range = PhoneRange.objects.get(
                startRange__lte=phone_int,
                endRange__gte=phone_int
            )

        except PhoneRange.DoesNotExist:
            return Response(
                {'error': f'Номер {phone} не найден в реестре'},
                status=status.HTTP_404_NOT_FOUND
            )

        except PhoneRange.MultipleObjectsReturned:
            phone_range = PhoneRange.objects.filter(
                startRange__lte=phone_int,
                endRange__gte=phone_int
            ).first()

        result = {
            'phone': phone,
            'operator': phone_range.operator,
            'region': phone_range.region
        }

        result_serializer = PhoneSerializer(result)

        return Response(
            result_serializer.data,
            status=status.HTTP_200_OK
        )
