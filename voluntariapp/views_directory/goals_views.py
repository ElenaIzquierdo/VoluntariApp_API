# voluntariapp/views_directory/course_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Goal
from voluntariapp.paginations import SixItems
from voluntariapp.serializers import GoalSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListGoalView(generics.ListAPIView):
    queryset = Goal.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Goal.objects.all()
        serializer = GoalSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET objectiu/:id/
    PUT objectiu/:id/
    DELETE objectiu/:id/
    """
    queryset = Goal.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_goal):
        a_objectiu = get_object_or_404(Goal, pk=id_goal)
        serializer = GoalSerializer(a_objectiu, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_goal):
        a_objectiu = get_object_or_404(Goal, pk=id_goal)
        serializer = GoalSerializer(a_objectiu, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id_goal):
        a_objectiu = get_object_or_404(Goal, pk=id_goal)
        a_objectiu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GoalFromCentreInteresView(generics.ListAPIView):
    queryset = Goal.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_centreinteres):
        self.pagination_class = SixItems
        queryset = self.filter_queryset(self.queryset.filter(centreinteres=id_centreinteres))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class GoalFromCentreInteresWithoutPaginationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_centreinteres):
        objectius = self.queryset.filter(centreinteres=id_centreinteres)
        serializer = GoalSerializer(objectius, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


