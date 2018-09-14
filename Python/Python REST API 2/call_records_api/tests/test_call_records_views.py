import json
import datetime
import pytz
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import CallStartRecord, CallEndRecord
from rest_framework import status
from rest_framework.test import APITestCase


class CallRecordTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.client.force_authenticate(user=self.user)

        CallStartRecord.objects.create(
            timestamp=datetime.datetime(
                2015, 1, 1, 12, 30, 59, 0, tzinfo=pytz.UTC),
            call_id=1,
            origin_phone=48981234545,
            destination_phone=4899123178)
        CallEndRecord.objects.create(
            timestamp=datetime.datetime(
                2015, 1, 1, 14, 35, 32, 0, tzinfo=pytz.UTC),
            call_id=1,
            reference_month=1,
            reference_year=2015)
        CallStartRecord.objects.create(
            timestamp=datetime.datetime(
                2017, 12, 12, 18, 35, 59, 0, tzinfo=pytz.UTC),
            call_id=2,
            origin_phone=48981457523,
            destination_phone=4893468278)

    def test_create_call_start_records(self):
        """
        Ensure we can create call start records.
        """
        url = reverse('v1:call-records-list')
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T18:35:59Z',
            'call_id': 71,
            'source': 48988526423,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))

        result.pop('id')
        expected = {
            'type': 'start',
            'timestamp': data['timestamp'],
            'call_id': data['call_id'],
            'origin_phone': data['source'],
            'destination_phone': data['destination']
        }
        self.assertEqual(result, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_call_end_records(self):
        """
        Ensure we can create call end records.
        """
        url = reverse('v1:call-records-list')
        data = {
            'type': 'end',
            'timestamp': '2017-12-12T22:12:19Z',
            'call_id': 71
        }
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))

        result.pop('id')
        expected = {
            'type': 'end',
            'timestamp': data['timestamp'],
            'call_id': data['call_id'],
            'reference_month': 12,
            'reference_year': 2017
        }
        self.assertEqual(result, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_call_records(self):
        """
        Ensure we can list call records.
        """
        url = reverse('v1:call-records-list')
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
