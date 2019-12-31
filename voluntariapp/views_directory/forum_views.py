# voluntariapp/views_directory/forum_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import ForumTopic
from voluntariapp.serializers import ForumTopicGetSerializer, ForumTopicSerializer, ForumCreateTopicSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView


class ForumThemeListView(generics.ListAPIView):
    queryset = ForumTopic.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ForumTopicSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ForumTopic.objects.filter(group=request.user.profile.group)
        sort_param = self.request.query_params.get('sort', None)
        possible_param = ["title", "created_date", "-title", "-created_date"]
        if sort_param is not None:
            if sort_param in possible_param:
                queryset = queryset.order_by(sort_param)
            else:
                status_code = 400
                message = "The request is not valid."
                explanation = "The parameter to sort is not correct, possible values: title,created_date"
                return Response({'message': message, 'explanation': explanation}, status=status_code)

        filter_status = self.request.query_params.get('status', None)
        if filter_status is not None:
            possible_status = ["open", "closed"]
            if filter_status in possible_status:
                if filter_status == "open":
                    queryset = queryset.filter(finished=False)
                elif filter_status == "closed":
                    queryset = queryset.filter(finished=True)
            else:
                status_code = 400
                message = "The request is not valid."
                explanation = "The parameter to filter status is not correct, possible values: open, closed"
                return Response({'message': message, 'explanation': explanation}, status=status_code)
        serializer = ForumTopicGetSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = ForumCreateTopicSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)



class ForumTopicNewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {"creator": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = ForumCreateTopicSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class ForumThemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET forumtheme/:id/
        PUT forumtheme/:id/
        DELETE forumtheme/:id/
        """
    queryset = ForumTopic.objects.all()
    serializer_class = ForumTopicSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
