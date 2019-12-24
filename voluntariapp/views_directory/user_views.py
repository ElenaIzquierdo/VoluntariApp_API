# voluntariapp/views_directory/user_views.py
from django.contrib.auth.models import User
from rest_framework import views, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from voluntariapp.serializers import UserSerializer
from rest_framework.views import APIView


# Create your views here.


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER", request.user.id)
        user = get_object_or_404(User, pk=request.user.id)
        data = UserSerializer(user).data
        return Response(data)
