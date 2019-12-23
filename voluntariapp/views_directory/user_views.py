# voluntariapp/views_directory/user_views.py
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = UserSerializer

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data['password'])
        password_encrypted = make_password(request.data['password'])
        print(password_encrypted)
        data ={"password":password_encrypted}
        data.update(request.data)
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)