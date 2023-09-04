from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins

from rest_framework.response import Response
from .serializer import RegisterSerializer,CustomSerializer, LoginSerializer, UpdateSerializer
from account.models import CustomUser
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
# Register Api


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh" : str(refresh),
        "access" : str(refresh.access_token)
    }



class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def get(self, request, *args, **kwargs):
        return Response({"message" : "Welcome ! Register Your details here..."})
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        return Response(
            {
                "message" : "User created successfully. Now perform Login to get your token..."
            }
        )
    

class ListUser(generics.ListAPIView):
    serializer_class = CustomSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]




class LoginApi(APIView):

    # queryset = CustomUser.objects.all()

    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                tk = get_token(user)

            return Response({"token": tk,
                "msg": "Login successfull" })
        return Response(
                {"msg": "something went wrong...!"}
                )
    

class ProfileCreateAPI(APIView):

    permission_classes=[IsAdminUser]


    def get(self, request):
        return Response({"msg" : "Hi there..!"})
    
    def put(self, request, pk=None, format=None):
        id = pk

        if id is not None:
            user = CustomUser.objects.get(pk=id)
            serializer = UpdateSerializer(user, request.data, partial=True)
         
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            return Response(
                {"msg" : serializer.errors}
            )
        data = {
            "msg" : "user does not exist",
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    

    def delete(self, request, pk=None, format=None):
        id = pk
        
        if id is not None:
            try:
                CustomUser.objects.get(pk=id).delete()
            except CustomUser.DoesNotExist as e:
                return Response({"User is deleted successfully. The user is not available"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"check the id given"}, status=status.HTTP_102_PROCESSING)
        
