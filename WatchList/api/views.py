from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from WatchList.api import serializers, permissions, pagination
from WatchList import models

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

class StreamPlatformListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        queryset = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        queryset = models.StreamPlatform.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = serializers.StreamPlatformSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = models.StreamPlatform.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = serializers.StreamPlatformSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        obj = models.StreamPlatform.objects.get(pk=pk)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# =======================================================================

class ReviewCreateAV(generics.CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = models.WatchList.objects.get(pk=pk)

        if models.Review.objects.filter(user=self.request.user, watchlist=watchlist).exists():
            raise ValidationError('You already did a review for this movie. ')

        ratingSum = 0
        
        watchlist.rating_number += 1
        watchlist.save()

        if (watchlist.rating_number == 1):
            watchlist.average_rating = serializer.validated_data['rating']
            watchlist.save()
        else:
            for review in watchlist.reviews.all():
                ratingSum += review.rating

            ratingSum += serializer.validated_data['rating']
            watchlist.average_rating = ratingSum / watchlist.rating_number
            watchlist.save()

        serializer.save(watchlist=watchlist, user=self.request.user)

class ReviewListAV(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)

class ReviewDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.ReviewUserOrReadOnly]

class ReviewUserList(APIView):

    def get(self, request):
        queryset = models.Review.objects.filter(user=self.request.user)
        serializer = serializers.ReviewSerializer(queryset, many=True)
        return Response(serializer.data)


# =======================================================================

class WatchListGenericList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    pagination_class = pagination.WatchListPagination

class WatchListGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
