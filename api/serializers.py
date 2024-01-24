from rest_framework import serializers
from .models import CustomUser,Friendship

class UserSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email','name','tc','password','password2')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }}

    def validate(self, obj):
        password = obj.get('password')
        password2 = obj.get('password2')
        if password!= password2:
            raise serializers.ValidationError('Password and Confirm Password do not match')
        return obj


    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = CustomUser
    fields = ['email', 'password']


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name', 'email']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('from_user','to_user','status',)