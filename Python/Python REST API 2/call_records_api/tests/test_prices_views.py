import json
import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import PriceRate
from rest_framework import status
from rest_framework.test import APITestCase


class PriceRateTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        PriceRate.objects.create(
            rate_type="std",
            start_time=datetime.time(6),
            end_time=datetime.time(22),
            standing_charge=0.36,
            charge_per_min=0.09)
        PriceRate.objects.create(
            rate_type="rdc",
            start_time=datetime.time(22),
            end_time=datetime.time(6),
            standing_charge=0.36,
            charge_per_min=0.0)

    def test_create_price_rate(self):
        """
        Ensure we can create a new price rate.
        """
        url = reverse('v1:price-rate-list')
        data = {'rate_type': 'std', 'start_time': datetime.time(12),
                'end_time': datetime.time(2), 'standing_charge': 0.36,
                'charge_per_min': 0.09}
        response = self.client.post(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))

        result.pop('id')
        expected = {'rate_type': data['rate_type'],
                    'start_time': str(data['start_time']),
                    'end_time': str(data['end_time']),
                    'standing_charge': str(data['standing_charge']),
                    'charge_per_min': str(data['charge_per_min'])}
        self.assertEqual(result, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_price_rate_with_invalid_type(self):
        """
        Ensure the creation fails for too long phone numbers.
        """
        url = reverse('v1:price-rate-list')
        rate_type = 'why'
        data = {'rate_type': rate_type, 'start_time': datetime.time(12),
                'end_time': datetime.time(2), 'standing_charge': 0.36,
                'charge_per_min': 0.09}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = ['"{}" is not a valid choice.'.format(rate_type)]
        self.assertEqual(response.data['rate_type'], error_msg)

    def test_list_price_rates(self):
        """
        Ensure we can list priceRates.
        """
        url = reverse('v1:price-rate-list')
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(result), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_price_rate(self):
        """
        Ensure we can get an price rate.
        """
        sample_id = 1
        url = reverse(
            'v1:price-rate-detail', kwargs={'priceRate_id': sample_id})
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        expected = PriceRate.objects.get(id=sample_id)
        self.assertEqual(result['rate_type'], expected.rate_type)
        self.assertEqual(
            result['start_time'], str(expected.start_time))
        self.assertEqual(
            result['end_time'], str(expected.end_time))
        self.assertEqual(
            result['standing_charge'], str(expected.standing_charge))
        self.assertEqual(
            result['charge_per_min'], str(expected.charge_per_min))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_price_rate(self):
        """
        Ensure we can update an price rate.
        """
        sample_id = 1
        url = reverse(
            'v1:price-rate-detail', kwargs={'priceRate_id': sample_id})
        data = {'rate_type': 'std', 'start_time': datetime.time(12),
                'end_time': datetime.time(2), 'standing_charge': 1.5,
                'charge_per_min': 0.05}
        response = self.client.put(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        expected = PriceRate.objects.get(id=sample_id)
        self.assertEqual(
            result['standing_charge'], str(expected.standing_charge))
        self.assertEqual(
            result['charge_per_min'], str(expected.charge_per_min))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_price_rate(self):
        """
        Ensure we can partially update an price rate.
        """
        sample_id = 1
        url = reverse(
            'v1:price-rate-detail', kwargs={'priceRate_id': sample_id})
        data = {'standing_charge': 0.4, 'charge_per_min': 0.01}
        response = self.client.patch(url, data, format='json')
        result = json.loads(response.content.decode('utf-8'))
        expected = PriceRate.objects.get(id=sample_id)
        self.assertEqual(
            result['standing_charge'], str(expected.standing_charge))
        self.assertEqual(
            result['charge_per_min'], str(expected.charge_per_min))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_price_rate(self):
        """
        Ensure we can delete an price rate.
        """
        sample_id = 1
        url = reverse(
            'v1:price-rate-detail', kwargs={'priceRate_id': sample_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode('utf-8'), '')
        with self.assertRaises(Exception) as context:
            PriceRate.objects.get(id=sample_id)
        self.assertEqual(
            'PriceRate matching query does not exist.',
            str(context.exception))
