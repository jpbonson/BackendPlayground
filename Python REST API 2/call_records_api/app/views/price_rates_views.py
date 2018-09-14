from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from ..models import PriceRate
from ..serializers import PriceRateSerializer


# GET  priceRates/: return a list of PriceRates
# POST priceRates/: create a PriceRate
class PriceRateList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = PriceRate.objects.all()
    serializer_class = PriceRateSerializer
    lookup_url_kwarg = 'priceRate_id'


# GET    priceRates/<priceRate_id>/: return a PriceRate
# PUT    priceRates/<priceRate_id>/: update a PriceRate
# PATCH  priceRates/<priceRate_id>/: patch a PriceRate
# DELETE priceRates/<priceRate_id>/: delete a PriceRate
class PriceRateDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = PriceRate.objects.all()
    serializer_class = PriceRateSerializer
    lookup_url_kwarg = 'priceRate_id'
