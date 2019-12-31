# voluntariapp/views_directory/course_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Week
from voluntariapp.paginations import SixItems
from voluntariapp.serializers import WeekSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse


class ListWeekView(generics.ListAPIView):
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Week.objects.all()
        serializer = WeekSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
    serializer_class = WeekSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class WeekFromQuarterView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_quarter):
        self.pagination_class = SixItems
        queryset = self.filter_queryset(self.queryset.filter(quarter=id_quarter))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WeekFromQuarterViewWithoutPagination(generics.RetrieveUpdateDestroyAPIView):
    queryset = Week.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_quarter):
        weeks = self.queryset.filter(quarter=id_quarter)
        serializer = WeekSerializer(weeks, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
