from django.urls import path, include
from .views import StreamPlatformListAV, StreamPlatformDetailAV
from .views import ReviewCreateAV, ReviewListAV, ReviewDetailAV, ReviewUserList
from .views import WatchListGenericList, WatchListGenericDetail
from rest_framework import routers



urlpatterns = [

    # URLS PARA MANIPULAÇÃO DE STREAMPLATFORM

    path('stream/', StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-detail'),

    # URLS PARA MANIPULAÇÃO DE REVIEW

    path('watch/<int:pk>/reviews/create/', ReviewCreateAV.as_view(), name='review-create'),
    path('watch/<int:pk>/reviews/', ReviewListAV.as_view(), name='review-list'),
    path('review/detail/<int:pk>/', ReviewDetailAV.as_view(), name='review-detail'),
    path('review/user/', ReviewUserList.as_view(), name='review-user'),

    # URLS PARA MANIPULAÇÃO DE WATCHLISTS

    path('watchlist/', WatchListGenericList.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchListGenericDetail.as_view(), name='watchlist-detail'),

]