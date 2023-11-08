from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4,
                                     error_messages={
                                         'required': 'Password is required.',
                                         'blank': 'Password is required.',
                                         'min_length': 'Password should contain minimum 4 characters.',
                                     })
    mobile_number = serializers.CharField(
        required=True, max_length=10, min_length=10,
        error_messages={
            'required': 'Mobile Number is required.',
            'blank': 'Mobile number is required.',
            'min_length': 'Enter valid 10 digit mobile number.',
            'max_length': 'Enter valid 10 digit mobile number.',
        })
    email = serializers.EmailField(required=False, allow_blank=True)
    # State + PAN-based 15-characters

    class Meta:
        model = User
        fields = ('id', 'mobile_number', 'email', 'password')

    def validate_fields(self, validated_data):
        mobile_number = validated_data.get('mobile_number')
        email = validated_data.get('email')

        if User.objects.filter(mobile_number=mobile_number).exists():
            raise serializers.ValidationError(
                {"mobile_number": ["Mobile number is already in use."]})

        if email and email != "":
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": ["Email is already in use."]})

    def create(self, validated_data):
        self.validate_fields(validated_data)

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
