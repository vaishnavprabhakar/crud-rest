from account.models import CustomUser

from rest_framework import serializers

from rest_framework import mixins

from rest_framework.generics import GenericAPIView

from django.contrib.auth import password_validation



class CustomSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser
        fields = ("__all__")



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   help_text='Required.'
                                   )
    
    username = serializers.CharField(help_text='Required',
                                     
                                      min_length=5,                                  
                                      )
    
    password = serializers.CharField(help_text='Required. Must have 6 charector.',
                                     
                                     min_length=6, write_only=True,
                                      
                                       style={'input_type' : 'password'})
    
    confirm_password = serializers.CharField(help_text='Required. Must have 6 charector.',
                                             
                                              min_length=6, write_only=True, 
                                              
                                              style={'input_type' : 'password'})
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password','confirm_password')
        extra_kwargs = {
            'password' : {'write_only' : True},
            'confirm_password' : {'write_only' : True},
        }

    
    def validate(self, data):
        """
        Validate that the passwords match.
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.DjangoModelField('password', "Passwords do not match.")
        
         
        return data

   
    

     

    def create(self, validated_data):
        
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password ==confirm_password:
            user = CustomUser.objects.create_user(
                            validated_data['username'], 
                                                
                            password=validated_data['password'],
                                                
                            email = validated_data['email'],
                            
                            )

        return user
    
    

    
class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True,help_text='Required.')
    # username = serializers.CharField(help_text='Required.', min_length=5,)
    password = serializers.CharField(help_text='Required. Must have 6 charector.'
                                     ,#min_length=6,
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

    