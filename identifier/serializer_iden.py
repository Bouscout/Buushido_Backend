from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class serial_user(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(), message='Ce pseudo est deja pris')], max_length = 32)
    password = serializers.CharField(write_only =True, min_length=8)
    # password2 = serializers.CharField(write_only =True)
    #we check if the passwords in the data are the same
    # def validate(self, data):
    #     if data['password1'] != data['password2'] :
    #         raise serializers.ValidationError('les mots de passe doivent etre les memes')
    #     return data
    
    def create(self, ok_data):
        user = User.objects.create_user(username=ok_data['username'], password=ok_data['password'])
        return user
    class Meta :
        model = User
        fields = ('id', 'username', 'password')


   