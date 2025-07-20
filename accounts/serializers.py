from rest_framework import serializers
from .models import CustomUser, Booking
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=CustomUser
        fields=["email","username","password"]
        
        
    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token= super().get_token(user)
        
        #add custom claims
        token['email']=user.email
        token['username']=user.username
        return token
    
    def validate(self, attrs):
        
        #replacing username with email
        attrs['username']=attrs.get('email')
        return super().validate(attrs)
    
    

#The booking serializer 

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields= ['id', 'destination', 'date' , 'phone_number' , 'created_at']
        read_only_fields =['created_at']
    
            