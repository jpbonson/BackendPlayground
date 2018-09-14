from django.db import models
from .validators import phone
from django.core.validators import MaxValueValidator, MinValueValidator


class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField(
        db_index=True, unique=True, validators=[phone.validate_size])

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class PriceRate(models.Model):
    RATE_CHOICES = {
        ('std', 'standard'),
        ('rdc', 'reduced'),
    }
    rate_type = models.CharField(max_length=3, choices=RATE_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    standing_charge = models.DecimalField(max_digits=5, decimal_places=2)
    charge_per_min = models.DecimalField(max_digits=5, decimal_places=2)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class CallStartRecord(models.Model):
    timestamp = models.DateTimeField()
    call_id = models.IntegerField(db_index=True, unique=True)
    origin_phone = models.BigIntegerField(validators=[phone.validate_size])
    destination_phone = models.BigIntegerField(
        validators=[phone.validate_size])

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class CallEndRecord(models.Model):
    timestamp = models.DateTimeField()
    call_id = models.IntegerField(db_index=True, unique=True)
    reference_month = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(12)
    ])
    reference_year = models.IntegerField(validators=[
        MinValueValidator(1900),
        MaxValueValidator(2100)
    ])

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class BillRecord(models.Model):
    subscriber = models.ForeignKey(
        Subscriber, related_name='bill_subscribers', on_delete=models.CASCADE)
    call_record = models.ForeignKey(
        CallStartRecord,
        related_name='bill_call_records',
        on_delete=models.SET_NULL,
        null=True,
        to_field="call_id",
        db_column="call_id")
    call_price = models.DecimalField(max_digits=99, decimal_places=2)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
