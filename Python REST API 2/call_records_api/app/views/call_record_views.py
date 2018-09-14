import datetime
import pytz
from rest_framework import status
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Subscriber, CallStartRecord, CallEndRecord, PriceRate
from ..serializers import (CallStartRecordSerializer,
                           CallEndRecordSerializer, BillRecordSerializer)


# GET  callRecords/: return a list of CallRecords
# POST callRecords/: create a CallRecord
@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def call_records_list(request, format=None):
    if request.method == 'POST':
        if request.data['type'] == 'start':
            return create_call_record_start(request.data)
        elif request.data['type'] == 'end':
            return create_call_record_end(request.data)
        else:
            raise ValidationError("Call record type must be 'start' or 'end'")
    else:
        return list_call_records()


def create_call_record_start(data):
    transformed_data = {
        'timestamp': data['timestamp'],
        'call_id': data['call_id'],
        'origin_phone': data['source'],
        'destination_phone': data['destination']}
    serializer = CallStartRecordSerializer(data=transformed_data)
    if serializer.is_valid():
        serializer.save()
        return finalize_response(serializer, data['type'])
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def finalize_response(serializer, data_type):
    result = serializer.data
    result['type'] = data_type
    return Response(result, status=status.HTTP_201_CREATED)


def create_call_record_end(data):
    date = data['timestamp'].split('T')[0]
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d')

    transformed_data = {
        'timestamp': data['timestamp'],
        'call_id': data['call_id'],
        'reference_month': date_object.month,
        'reference_year': date_object.year}
    serializer = CallEndRecordSerializer(data=transformed_data)
    if serializer.is_valid():
        serializer.save()
        attempt_bill_record_creation(serializer.validated_data)
        return finalize_response(serializer, data['type'])
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def attempt_bill_record_creation(end_call_record):
    start_calls = CallStartRecord.objects.filter(
        call_id=int(end_call_record['call_id'])).values()
    if start_calls:
        start_call = start_calls[0]
        origin_phone = start_call['origin_phone']
        subscribers = Subscriber.objects.filter(
            phone=origin_phone).values()
        if subscribers:
            create_bill_record(start_call, end_call_record, subscribers[0])


def create_bill_record(start_call_record, end_call_record, subscriber):
    subscriber_id = subscriber['id']
    bill_record_data = {
        'call_price': calculate_call_price(
            start_call_record['timestamp'],
            end_call_record['timestamp'])}
    serializer = BillRecordSerializer(data=bill_record_data)
    if serializer.is_valid():
        serializer.save(
            subscriber_id=subscriber_id,
            call_record_id=start_call_record['call_id'])


def calculate_call_price(start_timestamp, end_timestamp):
    std_price_rates = PriceRate.objects.filter(rate_type='std')[0]
    rdc_price_rates = PriceRate.objects.filter(rate_type='rdc')[0]
    if not std_price_rates or not rdc_price_rates:
        raise Exception("Must have a standard and a reduced price rate")

    total_price, rate_type = initial_price_rate_info(
        start_timestamp, std_price_rates, rdc_price_rates)

    rate_info = {
        'std': {
            'rate': std_price_rates.charge_per_min,
            'final_time': std_price_rates.end_time
        },
        'rdc': {
            'rate': rdc_price_rates.charge_per_min,
            'final_time': rdc_price_rates.end_time
        }
    }

    current = start_timestamp
    while (current < end_timestamp):
        final_datetime = calculate_final_datetime(
            current,
            rate_info[rate_type]['final_time'],
            end_timestamp)

        total_price += calculate_price_for_interval(
            final_datetime, current, rate_info[rate_type]['rate'])

        current = final_datetime
        if rate_type == 'std':
            rate_type = 'rdc'
        else:
            rate_type = 'std'
    return total_price


def initial_price_rate_info(start_timestamp, std_price_rates, rdc_price_rates):
    if check_time_between_intervals(std_price_rates, start_timestamp.time()):
        return std_price_rates.standing_charge, 'std'
    elif check_time_between_intervals(rdc_price_rates, start_timestamp.time()):
        return rdc_price_rates.standing_charge, 'rdc'
    else:
        raise Exception("Check the registered price rates")


def check_time_between_intervals(price_rates, timestamp):
    start = price_rates.start_time
    end = price_rates.end_time
    if start <= end:
        return start <= timestamp < end
    else:
        before_midnight = start <= timestamp <= datetime.time(23, 59, 59)
        after_midnight = datetime.time(0, 0, 0) <= timestamp < end
        return before_midnight or after_midnight


def calculate_final_datetime(current_datetime, final_time, end_datetime):
    final_datetime = datetime.datetime.combine(
        current_datetime.date(),
        final_time)
    final_datetime = pytz.utc.localize(final_datetime)

    if(final_datetime.time() < current_datetime.time()):
        final_datetime += datetime.timedelta(days=1)

    if(final_datetime > end_datetime):
        final_datetime = end_datetime
    return final_datetime


def calculate_price_for_interval(end_datetime, start_datetime, price_rate):
    total_minutes = int((end_datetime - start_datetime).total_seconds() / 60)
    return total_minutes * price_rate


def list_call_records():
    start_records = CallStartRecord.objects.all()
    start_data = list(
        CallStartRecordSerializer(start_records, many=True).data)
    end_records = CallEndRecord.objects.all()
    end_data = list(CallEndRecordSerializer(end_records, many=True).data)
    return Response(start_data + end_data)
