# voluntariapp/views_directory/comment_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated

from voluntariapp.models import Comment
from voluntariapp.serializers import CommentSerializer, CommentPostSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        data = {"author": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = CommentPostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET comment/:id/
    PUT comment/:id/
    DELETE comment/:id/
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class CommentFromThemeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id_forumtheme):
        comments = self.queryset.filter(forumtheme=id_forumtheme)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

