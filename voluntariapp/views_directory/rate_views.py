# voluntariapp/views_directory/rate_views.py
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from voluntariapp.models import Rate
from voluntariapp.serializers import RateSerializer
from rest_framework import status
from rest_framework.response import Response

class ListRateView(generics.ListAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser,)
    serializer_class = RateSerializer

    def get(self, request):
        queryset = Rate.objects.all()
        serializer = RateSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def post(self, request):
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class RateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rate/:id/
    PUT rate/:id/
    DELETE rate/:id/
    """
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request,id_rate):
        a_rate = get_object_or_404(Rate, pk=id_rate)
        serializer = RateSerializer(a_rate)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


    def patch(self, request, id_rate):
        a_rate = get_object_or_404(Rate, pk=id_rate)
        serializer = RateSerializer(a_rate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id_rate):
        a_rate = get_object_or_404(pk=id_rate)
        a_rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class RateFromEventView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RateSerializer

    def get(self, request, id_event):
        rates = self.queryset.filter(event=id_event)
        serializer = RateSerializer(rates, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)