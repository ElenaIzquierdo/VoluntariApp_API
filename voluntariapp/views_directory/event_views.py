# voluntariapp/views_directory/event_views.py

import os
from django.http import HttpResponse, Http404
from django.conf import settings
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from voluntariapp.models import Event, EventAttendee
from voluntariapp.serializers import EventSerializer, EventPostSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User


# Create your views here.

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Event.objects.filter(group=request.user.profile.group)
        serializer = EventSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def createUserAttendsEventsWhenCreatingEvent(event):
    weekday = event.start_date.weekday()
    users = User.objects.all()
    for u in users:
        if u.profile.group == event.group and u.profile.days[weekday] == '1':
            EventAttendee.objects.create(user=u, event=event)


class EventCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = EventPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        createUserAttendsEventsWhenCreatingEvent(event)
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


class FileFromEventView(APIView):

    def get(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        file_path = os.path.join(settings.MEDIA_ROOT, a_event.activity_file.name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read())
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404

    def put(self, request, id_event):
        event = get_object_or_404(Event, id=id_event)
        serializer = EventSerializer(event, data={'activity_file': request.FILES.get('activity_file',None)}, partial=True)
        serializer.is_valid(raise_exception=True)
        event.activity_file.delete()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id_event):
        event = get_object_or_404(Event, pk=id_event)
        event.activity_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


