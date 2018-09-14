from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from ..models import Subscriber
from ..serializers import SubscriberSerializer


# GET  subscribers/: return a list of Subscribers
# POST subscribers/: create a Subscriber
class SubscriberList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    lookup_url_kwarg = 'subscriber_id'


# GET    subscribers/<subscriber_id>/: return a Subscriber
# PUT    subscribers/<subscriber_id>/: update a Subscriber
# PATCH  subscribers/<subscriber_id>/: patch a Subscriber
# DELETE subscribers/<subscriber_id>/: delete a Subscriber
class SubscriberDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    lookup_url_kwarg = 'subscriber_id'
