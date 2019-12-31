# voluntariapp/views_directory/course_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Course
from voluntariapp.serializers import CourseSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListCourseView(generics.ListAPIView):
    queryset = Course.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET cours/:id/
    PUT cours/:id/
    DELETE cours/:id/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
