# voluntariapp/views_directory/rate_views.py
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Rate
from voluntariapp.serializers import RateSerializer
from rest_framework import status
from rest_framework.response import Response

class ListRateView(generics.ListAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Rate.objects.all()
        serializer = RateSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rate/:id/
    PUT rate/:id/
    DELETE rate/:id/
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]




class RateFromEventView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_event):
        rates = self.queryset.filter(event=id_event)
        serializer = RateSerializer(rates, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)