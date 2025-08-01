from rest_framework import serializers
from .models import CustomUser, Booking
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date


class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    profile_image=serializers.ImageField(required=False, allow_null = True) 
    
    class Meta:
        model=CustomUser
        fields=["email","username","password","first_name","last_name", "phone_number", "profile_image","address", "bio"]
        
   
        
    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number = validated_data['phone_number'],
            
            #Optional fields for the users 
            profile_image=validated_data.get('profile_image'),
            address=validated_data.get('address'),
            bio=validated_data.get('bio'),
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
        fields= ['id', 'destination', 'date' , 'phone_number' , 'number_of_travelers','group_type', 'duration', 'package','special_requests','created_at']
        read_only_fields =['user','created_at']
        
        
    def validate_date(self, value):
        if value < date.today(): 
            raise serializers.ValidationError('You cannot book for a past date.')
        return value
        
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'first_name', 'last_name', 'phone_number', 'profile_image', 'address', 'bio', 'date_joined'
        ]
        read_only_fields = ['email', 'date_joined', 'username', 'first_name','last_name',]
    
            
            
            