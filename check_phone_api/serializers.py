from rest_framework import serializers

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, help_text='Номер телефона')

    operator = serializers.CharField(help_text='Оператор связи')

    region = serializers.CharField(help_text='Регион')

    class Meta:
        fields = ['phone', 'operator', 'region']

class PhoneRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=11,
        min_length=11,
        help_text='Номер телефона в формате MSISDN(70000000000)',
        trim_whitespace=True
    )

    def validate_phone(self, phone):
        phone = ''.join(filter(str.isdigit, phone))

        if len(phone) != 11:
            raise serializers.ValidationError('Номер должен содержать 11 цифр')

        if not phone.startswith('7'):
            raise serializers.ValidationError('Номер должен начинаться с 7')

        return phone