from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,RegistrationSerializer
from rest_framework import viewsets,mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser] 


class RegistrationViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]  # Ensure anyone can access this view

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:8000/user/account/active/{uid}/{token}"

            email_subject = "confirm Your Email"
            email_body = render_to_string('confirm_account_email.html',{'confirm_link':confirm_link})

            email = EmailMultiAlternatives(email_subject,"",from_email=settings.EMAIL_HOST_USER,to=[user.email])
            email.attach_alternative(email_body,"text/html")
            try:
                email.send()
                print(f"Email sent successfully to {user.email}")  # Check console
                return Response({"message": "Check Your Mail for Confirmation"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Email Error: {str(e)}")  # Check console
                return Response({"message": "User created but email failed to send", "error": str(e)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()

        return HttpResponse("Account activated successfully! You can now log in.")
    else:
        return HttpResponse("Activation link is invalid or expired.")
    #     return redirect("http://127.0.0.1:8000/login")
    # return redirect("http://127.0.0.1:8000/register")

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 
    
    def get_queryset(self):
        # Return only the logged-in user's profile
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        # Optional: ensure users can only update themselves
        serializer.save(id=self.request.user.id)