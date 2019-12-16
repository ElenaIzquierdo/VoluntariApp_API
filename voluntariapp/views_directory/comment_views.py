# voluntariapp/views_directory/comment_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Comment
from voluntariapp.serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        data = {"author": request.user.id, "created_date": timezone.now()}
        data.update(request.data)
        serializer = CommentSerializer(data=data)
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
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, id_comment):
        a_comment = get_object_or_404(Comment,pk=id_comment)
        serializer = CommentSerializer(a_comment, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_comment):
        a_comment = get_object_or_404(Comment, pk=id_comment)
        serializer = CommentSerializer(a_comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_comment):
        a_comment = get_object_or_404(Comment,pk=id_comment)
        if a_comment.author == request.user:
            a_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={
                    "message": "You are not the original author of comment {}!".format(kwargs["pk"])
                },
                status=status.HTTP_403_FORBIDDEN
            )


class CommentFromThemeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = CommentSerializer

    def get(self, request, id_forumtheme):
        comments = self.queryset.filter(forumtheme=id_forumtheme)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

