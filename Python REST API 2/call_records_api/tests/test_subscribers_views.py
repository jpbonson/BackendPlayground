import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Subscriber
from rest_framework import status
from rest_framework.test import APITestCase


class SubscriberTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        Subscriber.objects.create(name="Ana", phone=48991123456)
        Subscriber.objects.create(name="Ricardo", phone=48981234545)
        Subscriber.objects.create(name="Maria", phone=4899123178)

    def test_create_subscriber(self):
        """
        Ensure we can create a new subscriber.
        """
        url = reverse('v1:subscriber-list')
        data = {'name': 'Paulo', 'phone': 4838129918}
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))

        result.pop('id')
        self.assertEqual(result, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_subscriber_with_short_phone_number(self):
        """
        Ensure the creation fails for too long phone numbers.
        """
        self.validate_phone_size(483812)

    def test_fail_create_subscriber_with_long_phone_number(self):
        """
        Ensure the creation fails for too long phone numbers.
        """
        self.validate_phone_size(483812991888)

    def validate_phone_size(self, phone):
        url = reverse('v1:subscriber-list')
        data = {'name': 'Paulo', 'phone': phone}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = ['Phone number {} must have 10 or 11 digits'.format(phone)]
        self.assertEqual(response.data['phone'], error_msg)

    def test_list_subscribers(self):
        """
        Ensure we can list subscribers.
        """
        url = reverse('v1:subscriber-list')
        response = self.client.get(url)
        result = map(
            lambda x: x['name'], json.loads(response.content.decode('utf-8')))
        expected = map(lambda x: x.name, list(Subscriber.objects.all()))
        self.assertEqual(list(result), list(expected))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_subscriber(self):
        """
        Ensure we can get an subscriber.
        """
        sample_id = 1
        url = reverse(
            'v1:subscriber-detail', kwargs={'subscriber_id': sample_id})
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        expected = Subscriber.objects.get(id=sample_id)
        self.assertEqual(result['name'], expected.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_subscriber(self):
        """
        Ensure we can update an subscriber.
        """
        sample_id = 1
        url = reverse(
            'v1:subscriber-detail', kwargs={'subscriber_id': sample_id})
        data = {'name': 'Ana', 'phone': 4881822635}
        response = self.client.put(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        expected = Subscriber.objects.get(id=sample_id)
        self.assertEqual(result['name'], expected.name)
        self.assertEqual(result['phone'], expected.phone)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_subscriber(self):
        """
        Ensure we can partially update an subscriber.
        """
        sample_id = 1
        url = reverse(
            'v1:subscriber-detail', kwargs={'subscriber_id': sample_id})
        data = {'phone': '48857319822'}
        response = self.client.patch(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        expected = Subscriber.objects.get(id=sample_id)
        self.assertEqual(result['name'], expected.name)
        self.assertEqual(result['phone'], expected.phone)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscriber(self):
        """
        Ensure we can delete an subscriber.
        """
        sample_id = 1
        url = reverse(
            'v1:subscriber-detail', kwargs={'subscriber_id': sample_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode('utf-8'), '')
        with self.assertRaises(Exception) as context:
            Subscriber.objects.get(id=sample_id)
        self.assertEqual(
            'Subscriber matching query does not exist.',
            str(context.exception))
