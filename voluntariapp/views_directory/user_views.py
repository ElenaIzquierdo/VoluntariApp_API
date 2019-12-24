# voluntariapp/views_directory/user_views.py
from django.contrib.auth.models import User
from rest_framework import views, generics
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

# Create your views here.


class UserListView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
