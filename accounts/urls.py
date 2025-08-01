from django.urls import path
from .views import SignupView, MyLoginView, ProfileView , BookNowView,PasswordResetRequestView,PasswordResetConfirmView, EditProfileView, BookingHistoryView, UpcomingBookingsView



urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('book-now/' , BookNowView.as_view(), name='book-now'),
    path('profile/me/update/' , EditProfileView.as_view(), name='edit-profile'),
    path('bookings/history/', BookingHistoryView.as_view(), name='booking-history'),
    path('bookings/upcoming/', UpcomingBookingsView.as_view(), name='booking-upcoming'),
    
    
    #The password reset paths
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
]


