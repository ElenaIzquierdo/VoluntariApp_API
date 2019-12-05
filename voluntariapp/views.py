# voluntariapp/views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Event, Comment, ForumTheme, Rate, EventAttendee
from .serializers import EventSerializer, EventGetSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = EventSerializer

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventGetSerializer(queryset, many=True, context={'request': request})
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
