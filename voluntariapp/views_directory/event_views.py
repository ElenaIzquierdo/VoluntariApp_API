# voluntariapp/views_directory/event_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser

from voluntariapp.models import Event
from voluntariapp.serializers import EventSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone


# Create your views here.

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventSerializer

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = EventSerializer(data=data)
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


class EventBeforeCurrentDateListView(generics.ListAPIView):
    queryset = Event.objects.filter(start_date__lte=timezone.now())
    serializer_class = EventSerializer



class EventAfterCurrentDateListView(generics.ListAPIView):
    queryset = Event.objects.filter(start_date__gte=timezone.now())
    serializer_class = EventSerializer


class EventFromWeekView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EventSerializer

    def get(self, request, id_week):
        events = self.queryset.filter(week=id_week)
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
