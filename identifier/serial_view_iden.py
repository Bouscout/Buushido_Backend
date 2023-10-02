from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from identifier.serializer_iden import serial_user
from django.contrib.auth.models import User

class create_user(APIView):
    def post(self, request, format='json'):
        serializer = serial_user(data=request.data)
        print('les donnes sont : ', request.data)
        # return Response('good job', status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            user = True
            print('went through')
            print(serializer)
            user = serializer.save()
            if user : 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            print('the errors are : ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class log_user(APIView):
    def post(self, request, format='json'):
        serializer = serial_user(data=request.data)
        print('les donnes sont : ', request.data)


class view_test(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        print('c\'est bon il est dans le system')
        print('the user is : ', request.user, 'the id is : ',request.user.id)
        message = "connexion reussi bruh"
        return Response(message, status=status.HTTP_202_ACCEPTED)