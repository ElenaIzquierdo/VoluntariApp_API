# voluntariapp/views_directory/event_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from voluntariapp.models import Event
from voluntariapp.serializers import EventSerializer, EventPostSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone


# Create your views here.

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EventCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("request ", request.user.id)
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        print("data ", data)
        serializer = EventPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET event/:id/
        PUT event/:id/
        PATCH event/:id/
        DELETE event/:id/
        """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class EventBeforeCurrentDateListView(generics.ListAPIView):
    queryset = Event.objects.filter(start_date__lte=timezone.now())
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class EventAfterCurrentDateListView(generics.ListAPIView):
    queryset = Event.objects.filter(start_date__gte=timezone.now())
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class EventFromWeekView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_week):
        events = self.queryset.filter(week=id_week)
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
