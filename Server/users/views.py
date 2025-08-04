from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer,SetNewPasswordSerializer,LogoutUserSerializer
from .utlis import send_code_to_user
from .models import OneTimePassword,User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Token helper function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # instance of user
            user_data = serializer.data
            send_code_to_user(user.email)  # Sending OTP or passcode
            tokens = get_tokens_for_user(user)
            
            return Response({
                'user': user_data,
                'tokens': tokens,
                'message': f"Hi {user.email}, thanks for signing up! A passcode has been sent. Have a nice day."
            }, status=status.HTTP_201_CREATED)
       

        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyUserEmail(GenericAPIView):
    permission_classes = [AllowAny]
    def post(self,request):
        otpcode=request.data.get('otp')
        try:
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user=user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'account email verified successfully'
                },status=status.HTTP_200_OK)
            return Response({
                'message':'code is invalid user already verified'

            },status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message':'passcode not provided'},status=status.HTTP_404_NOT_FOUND)
        

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    
class TestAuthenticationView(GenericAPIView):
    permission_classes=[IsAuthenticated]


    def get(self,request):
        data={
            'msg':'its working'
        }
        return Response(data,status=status.HTTP_200_OK)

class  PasswordResetRequestView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=PasswordResetRequestSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':"a link has been sent to your mail to reset your password"},status=status.HTTP_200_OK)

    
class PasswordRestConfirm(GenericAPIView):
    permission_classes = [AllowAny]
    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid','uidb64':uidb64, 'token':token},status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)

class SetNewPassword(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':"Password reset successfully "},status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Logout successful."}, status=status.HTTP_204_NO_CONTENT)