import datetime
import pytz
import json
from freezegun import freeze_time
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import (Subscriber, CallStartRecord,
                        CallEndRecord, PriceRate, BillRecord)
from rest_framework import status
from rest_framework.test import APITestCase


class BillRecordTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'test@test.com',
            'test',
        )
        self.client.force_authenticate(user=self.user)

        self.sample_subscriber = Subscriber.objects.create(
            name="Ana", phone=48988526423)
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

    def test_create_bill_records_for_between_price_rates1(self):
        """
        Ensure we can create call bill records by creating start/end
        call records. It must calculate correctly for 13 mins between
        price rates, starting at the standard rate.
        """
        url = reverse('v1:call-records-list')
        call_id = 71
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T21:57:13Z',
            'call_id': call_id,
            'source': self.sample_subscriber.phone,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'type': 'end',
            'timestamp': '2017-12-12T22:10:56Z',
            'call_id': call_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = BillRecord.objects.filter(call_record_id=call_id).values()[0]
        result['call_price'] = float(result['call_price'])
        expected = {
            'call_price': 0.54,
            'call_record_id': call_id,
            'id': 1,
            'subscriber_id': 1}
        self.assertEqual(result, expected)

    def test_create_bill_records_for_between_price_rates2(self):
        """
        Ensure we can create call bill records by creating start/end
        call records. It must calculate correctly for 13 mins between
        price rates, starting at the reduced rate.
        """
        url = reverse('v1:call-records-list')
        call_id = 71
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T04:57:13Z',
            'call_id': call_id,
            'source': self.sample_subscriber.phone,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'type': 'end',
            'timestamp': '2017-12-12T06:10:56Z',
            'call_id': call_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = BillRecord.objects.filter(call_record_id=call_id).values()[0]
        result['call_price'] = float(result['call_price'])
        expected = {
            'call_price': 1.26,
            'call_record_id': call_id,
            'id': 1,
            'subscriber_id': 1}
        self.assertEqual(result, expected)

    def test_create_bill_records_for_call_that_changes_days(self):
        """
        Ensure we can create call bill records by creating start/end
        call records. It must calculate correctly for a call that
        starts one day and finishes in the next day
        """
        url = reverse('v1:call-records-list')
        call_id = 71
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T21:57:13Z',
            'call_id': call_id,
            'source': self.sample_subscriber.phone,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'type': 'end',
            'timestamp': '2017-12-13T22:10:56Z',
            'call_id': call_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = BillRecord.objects.filter(call_record_id=call_id).values()[0]
        result['call_price'] = float(result['call_price'])
        expected = {
            'call_price': 86.94,
            'call_record_id': call_id,
            'id': 1,
            'subscriber_id': 1}
        self.assertEqual(result, expected)

    def test_fail_for_list_bill_records_for_not_found_subscriber(self):
        """
        Ensure the route returns 404 when the phone number isn't registered.
        """
        phone = 48999999999
        url = reverse(
            'v1:bill-records-list',
            kwargs={'subscriber_phone': phone})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_msg = 'Subscriber with phone number {} not found.'.format(phone)
        self.assertEqual(response.data['detail'], error_msg)

    def test_list_bill_records_for_empty_bills_without_reference(self):
        """
        Ensure the route works when there are no bills and no reference
        period.
        """
        with freeze_time("2012-02-14"):
            phone = self.sample_subscriber.phone
            url = reverse(
                'v1:bill-records-list',
                kwargs={'subscriber_phone': phone})
            response = self.client.get(url)
            result = json.loads(response.content.decode('utf-8'))
            expected = {
                'subscriber_name': self.sample_subscriber.name,
                'reference_period': '01-2012',
                'call_records': []}
            self.assertEqual(result, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_for_list_bill_records_with_invalid_reference(self):
        """
        Test must fails if the reference is not in a valid format.
        """
        with freeze_time("2012-02-14"):
            phone = self.sample_subscriber.phone
            url = reverse(
                'v1:bill-records-list',
                kwargs={'subscriber_phone': phone})
            url += "?reference=2017"
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_msg = "Invalid reference format: time data '2017'"
            error_msg += " does not match format '%m-%Y'"
            self.assertEqual(response.data, [error_msg])

    def test_list_bill_records_for_empty_bills_with_reference(self):
        """
        Ensure the route works when there are a reference
        period, but no bills.
        """
        with freeze_time("2012-02-14"):
            phone = self.sample_subscriber.phone
            url = reverse(
                'v1:bill-records-list',
                kwargs={'subscriber_phone': phone})
            url += "?reference=03-2017"
            response = self.client.get(url)
            result = json.loads(response.content.decode('utf-8'))
            expected = {
                'subscriber_name': self.sample_subscriber.name,
                'reference_period': '03-2017',
                'call_records': []}
            self.assertEqual(result, expected)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bill_records_when_reference_is_empty(self):
        """
        Ensure the route lists bill records only for the reference period.
        """
        url = reverse('v1:call-records-list')
        call_id = 71
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T21:57:13Z',
            'call_id': call_id,
            'source': self.sample_subscriber.phone,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'type': 'end',
            'timestamp': '2017-12-12T22:10:56Z',
            'call_id': call_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        phone = self.sample_subscriber.phone
        url = reverse(
            'v1:bill-records-list',
            kwargs={'subscriber_phone': phone})
        url += "?reference=11-2017"
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        expected = {
            'subscriber_name': self.sample_subscriber.name,
            'reference_period': '11-2017',
            'call_records': []}
        self.assertEqual(result, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bill_records(self):
        """
        Ensure the route lists bill records.
        """
        url = reverse('v1:call-records-list')
        call_id = 71
        data = {
            'type': 'start',
            'timestamp': '2017-12-12T21:57:13Z',
            'call_id': call_id,
            'source': self.sample_subscriber.phone,
            'destination': 4893468278
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'type': 'end',
            'timestamp': '2017-12-12T22:10:56Z',
            'call_id': call_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        phone = self.sample_subscriber.phone
        url = reverse(
            'v1:bill-records-list',
            kwargs={'subscriber_phone': phone})
        url += "?reference=12-2017"
        response = self.client.get(url)
        result = json.loads(response.content.decode('utf-8'))
        expected = {
            'subscriber_name': self.sample_subscriber.name,
            'reference_period': '12-2017',
            'call_records': [{
                'destination': 4893468278,
                'call_start_date': '2017-12-12',
                'call_start_time': '21:57:13',
                'call_duration': 13,
                'call_price': 0.54
            }]}
        self.assertEqual(result, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
