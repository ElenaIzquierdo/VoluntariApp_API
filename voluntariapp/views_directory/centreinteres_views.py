# voluntariapp/views_directory/centreinteres_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import CentreInteres
from voluntariapp.serializers import CentreInteresSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse

class ListCentreInteresView(generics.ListAPIView):
    queryset = CentreInteres.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CentreInteresSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = CentreInteres.objects.all()
        serializer = CentreInteresSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CentreInteresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CentreInteresDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET centreinteres/:id/
    PUT centreinteres/:id/
    DELETE centreinteres/:id/
    """
    queryset = CentreInteres.objects.all()
    serializer_class = CentreInteresSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
