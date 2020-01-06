# voluntariapp/views_directory/eventattendee_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Event, EventAttendee
from voluntariapp.serializers import EventAttendeeSerializer, AttendeesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ListEventAttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer


class AttendeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        EventAttendee.objects.create(user=request.user, event=a_event)
        return Response(status=status.HTTP_201_CREATED)


class UnattendView(generics.DestroyAPIView):
    serializer_class = EventAttendeeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        a_event = get_object_or_404(Event, pk=self.kwargs['pk'])
        queryset = EventAttendee.objects.filter(event = a_event, user = self.request.user)
        return queryset

class EventAttendeeUpdateDestroyAttendance(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class ListAttendeesView(APIView):
    queryset = EventAttendee.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, id_event):
        attendees = self.queryset.filter(event=id_event)
        serializer = AttendeesSerializer(attendees, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)