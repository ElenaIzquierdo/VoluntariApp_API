# voluntariapp/views_directory/eventattendee_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Event, EventAttendee
from voluntariapp.serializers import EventAttendeeSerializer
from rest_framework import status
from rest_framework.response import Response

class ListEventAttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventAttendeeSerializer

    def get(self, request):
        queryset = EventAttendee.objects.all()
        serializer = EventAttendeeSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AttendeeView(generics.ListAPIView):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer

    def post(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        EventAttendee.objects.create(user=request.user, event=a_event)
        return Response(status=status.HTTP_201_CREATED)

    "UnAttend function"

    def delete(self, request, id_event):
        event = get_object_or_404(Event, pk=id_event)
        a_attendee = self.queryset.get(event=event, user=request.user)
        a_attendee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)