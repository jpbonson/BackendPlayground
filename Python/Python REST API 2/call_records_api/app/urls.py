from django.conf.urls import url
from .views import (subscriber_views, price_rates_views,
                    call_record_views, bill_record_views)

urlpatterns = [
    url(
        r'^subscribers/$',
        subscriber_views.SubscriberList.as_view(),
        name='subscriber-list'
    ),
    url(
        r'^subscribers/(?P<subscriber_id>[0-9]+)/$',
        subscriber_views.SubscriberDetail.as_view(),
        name='subscriber-detail'
    ),
    url(
        r'^priceRates/$',
        price_rates_views.PriceRateList.as_view(),
        name='price-rate-list'
    ),
    url(
        r'^priceRates/(?P<priceRate_id>[0-9]+)/$',
        price_rates_views.PriceRateDetail.as_view(),
        name='price-rate-detail'
    ),
    url(
        r'^callRecords/$',
        call_record_views.call_records_list,
        name='call-records-list'
    ),
    url(
        r'^billRecords/(?P<subscriber_phone>[0-9]+)/$',
        bill_record_views.bill_records_list,
        name='bill-records-list'
    ),
]
