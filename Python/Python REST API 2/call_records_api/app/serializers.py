from .models import (Subscriber, PriceRate, CallStartRecord,
                     CallEndRecord, BillRecord)
from rest_framework import serializers


class BillRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillRecord
        fields = ('id', 'call_price')


class SubscriberSerializer(serializers.ModelSerializer):
    bill_records = BillRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Subscriber
        fields = ('id', 'name', 'phone', 'bill_records')


class PriceRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRate
        fields = ('id', 'rate_type', 'start_time', 'end_time',
                  'standing_charge', 'charge_per_min')


class CallStartRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStartRecord
        fields = (
            'id', 'timestamp', 'call_id', 'origin_phone',
            'destination_phone')


class CallEndRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEndRecord
        fields = (
            'id', 'timestamp', 'call_id', 'reference_month',
            'reference_year')
