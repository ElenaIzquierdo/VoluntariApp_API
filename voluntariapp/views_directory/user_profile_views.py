# voluntariapp/views_directory/user_views.py
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.serializers import UserProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from voluntariapp.models import UserProfile
from rest_framework.generics import get_object_or_404

# Create your views here.


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = UserProfileSerializer

    def get(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET userprofile/:id/
    PUT userprofile/:id/
    DELETE userprofile/:id/
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
