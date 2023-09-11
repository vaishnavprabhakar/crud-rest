
from account.models import CustomUser

from rest_framework import serializers

# from rest_framework import mixins

# from rest_framework.generics import GenericAPIView

from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError


class CustomSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ("__all__")



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   help_text='Required.'
                                   )
    
    username = serializers.CharField(help_text='Required',
                                     required=True,
                                      min_length=5,                                  
                                      )
    
    password = serializers.CharField(help_text='Required. Must have 6 charector.',
                                     required=True,
                                     min_length=6, write_only=True,
                                      
                                       style={'input_type' : 'password'})
    
    confirm_password = serializers.CharField(help_text='Required. Must have 6 charector.',
                                             required=True,

                                              min_length=6, write_only=True, 
                                              
                                              style={'input_type' : 'password'})
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password','confirm_password')
        extra_kwargs = {
            'password' : {'write_only' : True},
            'confirm_password' : {'read_only' : True},
        }

    
    def validate(self, validated_data):
        """
        Validate that the passwords match.
        """
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        username = validated_data.get('username')
        print(username)
        print(type(username))
        if username[0:-2].isalpha() and username[-2:].isdigit():
    
            raise serializers.ValidationError({"username": ValidationError.messages})
       
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
    
        return validated_data

   
    

     

    def create(self, validated_data):
        
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password ==confirm_password:
            user = CustomUser.objects.create_user(
                            username = validated_data['username'], 
                                                
                            password=validated_data['password'],
                                                
                            email = validated_data['email'],
                            
                            )
            
            try:
                validate_password(password=validated_data['password'], user=user)

            except ValidationError as err:
                user.delete()
                raise serializers.ValidationError({"password": err.messages})
            
            
        return user
    
    

    
class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True,help_text='Required.')
    
    password = serializers.CharField(help_text='Required. Must have 6 charector.',
                                     required=True,
                                       write_only=True,
                                         style={'input_type' : 'password'}  
                                         )

    class Meta:
        model = CustomUser
        fields = ('email','password')
    


class UpdateSerializer(serializers.ModelSerializer):
    
    

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile',)

    