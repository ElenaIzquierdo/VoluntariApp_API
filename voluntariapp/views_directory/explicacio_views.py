# voluntariapp/views_directory/cours_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Explicacio
from voluntariapp.paginations import OneByOneItems
from voluntariapp.serializers import ExplicacioSerializer, ExplicacioGetFromCentreInteresSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse


class ListExplicacioView(generics.ListAPIView):
    queryset = Explicacio.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = ExplicacioSerializer

    def get(self, request, *args, **kwargs):
        queryset = Explicacio.objects.all()
        serializer = ExplicacioSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExplicacioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def post(self, request):
    serializer = ExplicacioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExplicacioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET explicacio/:id/
    PUT explicacio/:id/
    DELETE explicacio/:id/
    """
    queryset = Explicacio.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ExplicacioSerializer

    def get(self, request, id_explicacio):
        a_explicacio = get_object_or_404(Explicacio, pk=id_explicacio)
        serializer = ExplicacioSerializer(a_explicacio, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id_explicacio):
        a_explicacio = get_object_or_404(Explicacio, pk=id_explicacio)
        serializer = ExplicacioSerializer(a_explicacio, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_explicacio):
        a_explicacio = get_object_or_404(Explicacio, pk=id_explicacio)
        a_explicacio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExplicacioFromCentreInteresView(generics.ListAPIView):
    queryset = Explicacio.objects.all().order_by('date')
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = ExplicacioGetFromCentreInteresSerializer

    def get(self, request, id_centreinteres):
        self.pagination_class = OneByOneItems
        queryset = self.filter_queryset(self.queryset.filter(centreinteres=id_centreinteres))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
