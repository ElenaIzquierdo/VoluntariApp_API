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
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET event/:id/
        PUT event/:id/
        DELETE event/:id/
        """
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EventSerializer

    def get(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        serializer = EventSerializer(a_event)
        return Response(data=serializer.data, status= status.HTTP_200_OK)


    def patch(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        serializer = EventSerializer(a_event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status= status.HTTP_200_OK)

    def delete(self, request, id_event):
        a_event = get_object_or_404(Event, pk=id_event)
        if a_event.creator == request.user:
            a_event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "message": "You are not the original author of the event {}!"
                },
                status=status.HTTP_403_FORBIDDEN
            )