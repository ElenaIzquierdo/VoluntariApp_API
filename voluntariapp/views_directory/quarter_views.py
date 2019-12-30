# voluntariapp/views_directory/cours_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Quarter
from voluntariapp.serializers import QuarterSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListQuarterView(generics.ListAPIView):
    queryset = Quarter.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = QuarterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Quarter.objects.all()
        serializer = QuarterSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuarterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuarterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET quarter/:id/
    PUT quarter/:id/
    DELETE quarter/:id/
    """
    queryset = Quarter.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = QuarterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_quarter):
        a_quarter = get_object_or_404(Quarter,pk=id_quarter)
        serializer = QuarterSerializer(a_quarter, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_quarter):
        a_quarter = get_object_or_404(Quarter, pk=id_quarter)
        serializer = QuarterSerializer(a_quarter, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_quarter):
        a_quarter = get_object_or_404(Quarter, pk=id_quarter)
        a_quarter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuarterFromCoursView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quarter.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = QuarterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_course):
        quarters = self.queryset.filter(cours=id_course)
        serializer = QuarterSerializer(quarters, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
