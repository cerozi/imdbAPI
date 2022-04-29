from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from WatchList.api.serializers import WatchListSerializer, ReviewSerializer
from .models import Review, StreamPlatform, WatchList

# Create your tests here.

class StreamPlatformTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser123')
        self.client.login(username='testuser', password='testuser123')

        self.stream = StreamPlatform.objects.create(name='Amazon', about='Amazon prime platform', url='https://primevideo.com')
    
    def test_update(self):
        data = {
            'name': 'Amazon Prime - UPDATED',
            'about': 'Amazon prime platform',
            'url': 'https://primevideo.com'
        }

        response = self.client.put(reverse('stream-detail', args=(self.stream.pk, )), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_getDetail(self):
        response = self.client.get(reverse('stream-detail', args=(self.stream.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(reverse('stream-detail', args=(self.stream.pk, )))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create(self):

        data = {
            'name': 'Netflix',
            'about': '1st streaming platform in the world',
            'url': 'https://netflix.com'
        }
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_getList(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser123', is_staff=True)
        self.client.login(username='testuser', password='testuser123', is_staff=True)

        self.stream = StreamPlatform.objects.create(name='Netflix', about='Streaming platform', url='https://netflix.com')
        self.watchlist = WatchList.objects.create(
            title='Social Network',
            description='Movie about the facebook. ',
            active = True,
            platform = self.stream
        )


    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_create(self):

        data = {
            'title': 'Test',
            'description': 'Test',
            'active': True,
            'platform': self.stream.pk
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_put(self):

        data = {
            'title': 'Social Network - UPDATED',
            'description':'Movie about the facebook. ',
            'active': False,
            'platform': self.stream.pk
        }

        response = self.client.put(reverse('watchlist-detail', args=(self.watchlist.pk, )), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_delete(self):

        response = self.client.delete(reverse('watchlist-detail', args=(self.watchlist.pk, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ReviewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='matheus', password='cerozi2002', is_staff=True)
        self.client.login(username='matheus', password='cerozi2002')

        self.stream = StreamPlatform.objects.create(name='Netflix', about='Streaming platform', url='https://netflix.com')

        # WATCHLIST FOR REVIEW CREATE

        self.watchlist = WatchList.objects.create(
            title = 'Social Network',
            description ='Movie about the facebook. ',
            active = True,
            platform = self.stream
        )

        # WATCHLIST AND REVIEW FOR REVIEW UPDATE

        self.watchlist2 = WatchList.objects.create(
            title = 'Django',
            description = 'Gangbang movie ',
            active = True,
            platform = self.stream
        )

        self.review = Review.objects.create(
            rating = 5,
            about = 'Great movie. ',
            watchlist = self.watchlist2,
            user = self.user
        )


    def test_review_create_authenticated(self):

        data = {
            'rating': 5,
            'about': 'Good movie'
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.pk, )), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # FAZENDO REVIEW PARA O MESMO FILME

        response = self.client.post(reverse('review-create', args=(self.watchlist.pk, )), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauthenticated(self):
        # DESLOGANDO
        self.client.logout()

        data = {
            'rating': 5,
            'about': 'Good movie. '
        }
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.pk, )), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):

        data = {
            'rating': 1,
            'about': "Didn't like it at all. "
        }

        response = self.client.put(reverse('review-detail', args=(self.review.pk, )), data)
        serializer = ReviewSerializer(data=response.data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_get_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist2.pk, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_get_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.pk, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_get_user(self):
        response = self.client.get(reverse('review-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.pk, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)