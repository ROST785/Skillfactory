import datetime

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import PerevalAdded, Coord, Users, Level
from .serializers import PerevalAddedSerializer


class MountApiTestCase(APITestCase):

    def setUp(self):
        user_1 = Users.objects.create(email='Test_1', phone=1111, fam='Test_1', name='Test_1', otc='Test_1')
        user_2 = Users.objects.create(email='Test_2', phone=2222, fam='Test_2', name='Test_2', otc='Test_2')
        coords_1 = Coord.objects.create(latitude=5.0002, longitude=5.0002, height=200)
        coords_2 = Coord.objects.create(latitude=5.0022, longitude=5.0002, height=200)
        level_1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level_2 = Level.objects.create(winter='2a', spring='2a', summer='2a', autumn='2a')
        self.mount_1 = PerevalAdded.objects.create(user_id=user_1, beauty_title='beauty_title_1', title="title_1",
                                                   other_titles='other_titles_1', coord_id=coords_1, level_id=level_1)
        self.mount_2 = PerevalAdded.objects.create(user_id=user_2, beauty_title='beauty_title_2', title="title_2",
                                                   other_titles='other_titles_2', coord_id=coords_2, level_id=level_2)

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalAddedSerializer([self.mount_1, self.mount_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.mount_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalAddedSerializer(self.mount_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class MountSerializerTestCase(TestCase):
    def setUp(self):
        user_1 = Users.objects.create(email="Test_1", phone=1111, fam="Test_1", name="Test_1", otc="Test_1")
        user_2 = Users.objects.create(email="Test_2", phone=2222, fam="Test_2", name="Test_2", otc="Test_2")
        coords_1 = Coord.objects.create(latitude=5.0002, longitude=5.0002, height=200)
        coords_2 = Coord.objects.create(latitude=5.0002, longitude=5.0002, height=200)
        level_1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level_2 = Level.objects.create(winter='2a', spring='2a', summer='2a', autumn='2a')
        self.mount_1 = PerevalAdded.objects.create(user_id=user_1, beauty_title="beauty_title_1", title="title_1",
                                                   other_titles="other_titles_1",
                                                   coord_id=coords_1, level_id=level_1)
        self.mount_2 = PerevalAdded.objects.create(user_id=user_2, beauty_title="beauty_title_2", title="title_2",
                                                   other_titles="other_titles_2",
                                                   coord_id=coords_2, level_id=level_2)

    def test_check(self):
        serializer_data = PerevalAddedSerializer([self.mount_1, self.mount_2], many=True).data

        expected_data = [
            {
                "id": 1,
                "beauty_title": "beauty_title_1",
                "title": "title_1",
                "other_titles": "other_titles_1",
                "connect": None,
                "add_time": self.mount_1.add_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "level_id": {
                    "id": 1,
                    "winter": "1a",
                    "summer": "1a",
                    "autumn": "1a",
                    "spring": "1a"
                },
                "user_id": {
                    "email": "Test_1",
                    "phone": "1111",
                    "fam": "Test_1",
                    "name": "Test_1",
                    "otc": "Test_1"
                },
                "coord_id": {
                    "latitude": 5.0002,
                    "longitude": 5.0002,
                    "height": 200
                },
                "images": [],
                "status": "NEW"
            },
            {
                "id": 2,
                "beauty_title": "beauty_title_2",
                "title": "title_2",
                "other_titles": "other_titles_2",
                "connect": None,
                "add_time": self.mount_2.add_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "level_id": {
                    "id": 2,
                    "winter": "2a",
                    "summer": "2a",
                    "autumn": "2a",
                    "spring": "2a"
                },
                "user_id": {
                    "email": "Test_2",
                    "phone": "2222",
                    "fam": "Test_2",
                    "name": "Test_2",
                    "otc": "Test_2"
                },
                "coord_id": {
                    "latitude": 5.0002,
                    "longitude": 5.0002,
                    "height": 200
                },
                "images": [],
                "status": "NEW"
            },
        ]

        self.assertEqual(serializer_data, expected_data)
