from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class LoginAPI(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email, password=password)

                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid Credentials',
                        'data': serializer.errors
                    }, status=400)
                
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })


            return Response({
                'status': 400,
                'message': 'failed to login',
                'data': serializer.errors
            }, status=400)
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'failed to login',
            }, status=400)


class RegisterAPI(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 201,
                    'message': "registration successfull",
                    'data': serializer.data
                })
            
            return Response({
                'status': 400,
                'message': 'failed to register',
                'data': serializer.errors
            }, status=400)
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'failed to register',
            })


class RefreshTokenAPI(APIView):
    permission_classes = ()

    def post(self, request):
        data = request.data
        serializer = RefreshTokenSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'data': serializer.errors
            },status=401)
        try:
            refresh_token = serializer.data['refresh_token']
            RefreshToken(refresh_token)
            refresh = RefreshToken.for_user(request.user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({
                'status': 401,
                'data': "Invalid Token"
            }, status=401)
        

class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        user = {
            'email': user.__dict__.get("email"),
            'name': user.__dict__.get("first_name")
        }
        print(user)
        serializer = ProfileSerializer(data=user)
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'data':serializer.errors
            })
        
        return Response({
            'data': serializer.data
        })        