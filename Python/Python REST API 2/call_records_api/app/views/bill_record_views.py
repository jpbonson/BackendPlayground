import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from ..models import (BillRecord, Subscriber,
                      CallStartRecord, CallEndRecord)


# GET  billRecords/<subscriber_phone>/: return a BillRecord
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def bill_records_list(request, subscriber_phone, format=None):
    subscriber = get_subscriber(subscriber_phone)
    reference = get_reference_period(request.query_params)
    base_msg = generate_base_message(subscriber, reference)

    records = BillRecord.objects.filter(subscriber_id=subscriber['id'])
    if not records:
        return Response(base_msg)

    base_msg['call_records'] = process_records(records, reference)
    return Response(base_msg)


def get_subscriber(subscriber_phone):
    subscribers = Subscriber.objects.filter(phone=subscriber_phone).values()
    if not subscribers:
        error_msg = "Subscriber with phone number {} not found."
        error_msg = error_msg.format(subscriber_phone)
        raise NotFound(error_msg)
    return subscribers[0]


def get_reference_period(query_params):
    if 'reference' in query_params:
        reference = query_params['reference']
        try:
            return datetime.datetime.strptime(reference, '%m-%Y')
        except ValueError as e:
            error_msg = 'Invalid reference format: {}'.format(str(e))
            raise ValidationError(error_msg)
    else:
        return datetime.date.today() - relativedelta(months=1)


def generate_base_message(subscriber, reference):
    reference_month = reference.month
    reference_year = reference.year
    return {
        'subscriber_name': subscriber['name'],
        'reference_period': '{:02}-{}'.format(reference_month, reference_year),
        'call_records': []}


def process_records(records, reference):
    call_records = []
    for record in records:
        end_call = get_end_call(record.call_record_id, reference)
        if not end_call:
            continue

        start_call = CallStartRecord.objects.filter(
            call_id=record.call_record_id)[0]

        timestamp_diff = end_call.timestamp - start_call.timestamp
        call_duration = int(timestamp_diff.total_seconds() / 60)
        call_record = {
            'destination': start_call.destination_phone,
            'call_start_date': start_call.timestamp.date(),
            'call_start_time': start_call.timestamp.time(),
            'call_duration': call_duration,
            'call_price': record.call_price}
        call_records.append(call_record)
    return call_records


def get_end_call(call_record_id, reference):
    end_calls = CallEndRecord.objects.filter(
        call_id=call_record_id,
        reference_month=reference.month,
        reference_year=reference.year)
    if not end_calls:
        return None
    return end_calls[0]
