from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
    )
from rest_framework.response import Response
from user_profiles.serializers import (
    UserSerializer, TestSessionSerializer, UserRegisterSerializer, QuizSerializer
    )
from django.views.decorators.csrf import (
    ensure_csrf_cookie,
    csrf_protect
    )
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth import (
    authenticate, login, logout, get_user_model
    )
from user_profiles.models import User, TestSession
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_encode, urlsafe_base64_decode
    )
from django.utils.encoding import (
    force_bytes, force_str
    )
from rest_framework import status
from user_profiles.utils import send_activation_email
from RAGpipelines.questionGeneratorPipeline import GeneratorClient

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"success": "CSRF cookie set"}, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)

            print(request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                user.is_active = False
                user.save()

                # Generate activation link
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # activation_path = reverse('activate', kwargs={'uid': uid, 'token':token})
                activation_url = f"{settings.SITE_DOMAIN}/signup/activate?uid={uid}&token={token}"

                # Send activation email (replace with actual email sending logic)
                try:
                    send_activation_email(user.email, activation_url)
                except Exception as email_error:
                    print(f"Error sending email: {email_error}")
                    return Response({'message': 'Error sending activation email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(
                    {"message": "User created. Check your email to activate your account."},
                    status=status.HTTP_200_OK
                )
            
            errors = serializer.errors
            
            format_errors = {field: messages[0] for field, messages in errors.items()}
            return Response({"error": format_errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Internal server error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    


# @method_decorator(csrf_protect, name='dispatch')
# class activateConfirm(APIView):
#     permission_classes = [AllowAny]

@method_decorator(csrf_protect, name='dispatch')
class accountActivateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')

            print(uid)
            print(token)
            # Check if uid and token are provided
            if not uid or not token:
                return Response({'message': "Missing uid or token"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Decode the uid
                uid = urlsafe_base64_decode(force_str(uid))
                user = User.objects.get(pk=uid)

                # If the user is already active
                if user.is_active:
                    return Response({'message': 'Account already activated'}, status=status.HTTP_200_OK)

                # Check if the token is valid
                if default_token_generator.check_token(user, token):
                    user.is_active = True
                    user.save()
                    return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                # Return a message if user is not found
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # except Exception as e:
            #     # Log the exception (consider adding logging)
            #     return Response({'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Log any outer exceptions (not related to user processing)
            return Response({'message': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists before authentication
            try:
                User = get_user_model()
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request=request, user=user)
                return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email or password incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception:
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
    


class testSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        topicsName = request.data.get('topicName')
        difficultyLevel = request.data.get('difficultyLevel')
        noOfQuestions = request.data.get('noOfQuestions')

        if not topicsName or not difficultyLevel or not noOfQuestions:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        generateTestSessionClient = GeneratorClient()
        try:
            modelResponse = generateTestSessionClient.call_gemini(
                prompt=topicsName, 
                questions=noOfQuestions, 
                difficulty_level=difficultyLevel)

            if "error" in modelResponse:
                return Response({"error": modelResponse["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            test_session = TestSession.objects.create(
                user=user,
                topicsName=topicsName,
                noOfQuestions=noOfQuestions,
                difficultyLevel=difficultyLevel,
                questionsSet=modelResponse
            )
            serializer = TestSessionSerializer(test_session)

            return Response({"sessionId": serializer.data["sessionId"]}, status=status.HTTP_201_CREATED)
          
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class quizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sessionId):
        try:
            # Retrieve the TestSession object using the sessionId
            test_session = TestSession.objects.get(sessionId=sessionId)
        except TestSession.DoesNotExist:
            return Response({"error": "Test session not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSerializer(test_session)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
