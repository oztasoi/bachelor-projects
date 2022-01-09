from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

CARGO_COMPANY_CHOICES = (
    ('aras', 'Aras Kargo'),
    ('mng', 'MNG Kargo'),
    ('yurtici', 'Yurtici Kargo'),
    ('ptt', 'PTT Kargo'),
    ('ups', 'UPS'),
    ('other', 'Other')
)


class Vendor(models.Model):

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(primary_key=True, blank=False)
    lat = models.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    lon = models.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=3000, blank=False)
    amount_left = models.PositiveIntegerField()
    price = models.FloatField(
        validators=[
            MinValueValidator(0)
        ]
    )
    brand = models.CharField(max_length=200, blank=False)
    is_free_shipment = models.BooleanField()
    release_date = models.DateTimeField(default=timezone.now)
    cargo_company = models.CharField(max_length=10,
                                     choices=CARGO_COMPANY_CHOICES,
                                     default='other')

    def release_product(self):
        self.release_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title