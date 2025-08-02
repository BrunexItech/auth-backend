from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, BookingSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from  django.utils import timezone

#The password reset imports 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
class SignupView(APIView):
    parser_classes = [MultiPartParser , FormParser]
    
    def post(self, request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({'message':'User created successfully'}, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MyLoginView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
    
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request':request})
        return Response(serializer.data)
    
    
    #This is commented out
    '''def get(self, request):
        user=request.user
        return Response({
            'message':'You are authenticated',
            'email':user.email,
            'first_name':user.first_name,
            'username':user.username,
            'profile_image':request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
        })'''
    
    

class BookNowView(APIView):
    permission_classes = [IsAuthenticated]
        
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message':'Booking successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
#The password reset logic flow
class PasswordResetRequestView(APIView):
    def post(self,request):
        email =request.data.get('email')#checking whether the email exists first
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'No user with that email'}, status=status.HTTP_404_NOT_FOUND)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        frontend_url = settings.FRONTEND_URL
        
        reset_link = f"{frontend_url}/#/reset-password/{uid64}/{token}"
        
        send_mail(
            subject="Password Reset Request",
            message = f"Hi {user.username}, click the link below to reset your password:\n {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            
        )
        
        return Response({'message':'Check your email for the password reset link.'}, status = status.HTTP_200_OK)
    
    
#Setting the new password 

class PasswordResetConfirmView(APIView):
    def post(self ,request , uidb64, token):
        new_password = request.data.get('password')
        User = get_user_model()
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(User.DoesNotExist, ValueError, TypeError,OverflowError):
            return Response({"error":"Invalid link"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user,token):
            return Response({"error":"Invalid or expired token"}, status = status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({"message":"Password has been reset successfully"}, status=status.HTTP_200_OK) 
    
    
    
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    
    def patch(self, request):
        user=request.user
        serializer =UserProfileSerializer(
            user, data=request.data, partial=True, context={'request':request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
        
    
    '''def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial = True)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response ({'message':"Profile updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
    
    #Booking History
    
class BookingHistoryView(APIView):
        permission_classes = [IsAuthenticated]
        
        
        def get(self, request):
            user=request.user
            past_bookings = Booking.objects.filter(user=user, date__lt=timezone.now()).order_by('-date')
            serializer=BookingSerializer(past_bookings, many=True)
            return Response(serializer.data)
        
        
class UpcomingBookingsView(APIView):
        permission_classes = [IsAuthenticated]
        
        def get(self, request):
            user=request.user
            upcoming_bookings = Booking.objects.filter(user=user, date__gte=timezone.now()).order_by('date')
            serializer=BookingSerializer(upcoming_bookings, many=True)
            return Response(serializer.data)
    


