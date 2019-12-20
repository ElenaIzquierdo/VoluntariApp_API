# voluntariapp/views_directory/cours_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Objectiu
from voluntariapp.paginations import SixItems
from voluntariapp.serializers import ObjectiuSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse

class ListObjectiuView(generics.ListAPIView):
    queryset = Objectiu.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ObjectiuSerializer

    def get(self, request, *args, **kwargs):
        queryset = Objectiu.objects.all()
        serializer = ObjectiuSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ObjectiuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObjectiuDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET objectiu/:id/
    PUT objectiu/:id/
    DELETE objectiu/:id/
    """
    queryset = Objectiu.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ObjectiuSerializer

    def get(self, request, id_objectiu):
        a_objectiu = get_object_or_404(Objectiu,pk=id_objectiu)
        serializer = ObjectiuSerializer(a_objectiu, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_objectiu):
        a_objectiu = get_object_or_404(Objectiu, pk=id_objectiu)
        serializer = ObjectiuSerializer(a_objectiu, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_objectiu):
        a_objectiu = get_object_or_404(Objectiu, pk=id_objectiu)
        a_objectiu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ObjectiuFromCentreInteresView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Objectiu.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ObjectiuSerializer

    def get(self, request, id_centreinteres):
        self.pagination_class = SixItems
        queryset = self.filter_queryset(self.queryset.filter(centreinteres=id_centreinteres))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ObjectiuFromCentreInteresWithoutPaginationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Objectiu.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ObjectiuSerializer

    def get(self, request, id_centreinteres):
        objectius = self.queryset.filter(centreinteres=id_centreinteres)
        serializer = ObjectiuSerializer(objectius, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


