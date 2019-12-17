# voluntariapp/views_directory/cours_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Week
from voluntariapp.serializers import WeekSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse

class ListWeekView(generics.ListAPIView):
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = WeekSerializer

    def get(self, request, *args, **kwargs):
        queryset = Week.objects.all()
        serializer = WeekSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WeekSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeekDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET week/:id/
    PUT week/:id/
    DELETE week/:id/
    """
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = WeekSerializer

    def get(self, request, id_week):
        a_quarter = get_object_or_404(Week,pk=id_week)
        serializer = WeekSerializer(a_quarter, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_week):
        a_quarter = get_object_or_404(Week, pk=id_week)
        serializer = WeekSerializer(a_quarter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_week):
        a_quarter = get_object_or_404(Week, pk=id_week)
        a_quarter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeekFromQuarterView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = WeekSerializer

    def get(self, request, id_quarter):
        quarters = self.queryset.filter(quarter=id_quarter)
        serializer = WeekSerializer(quarters, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)