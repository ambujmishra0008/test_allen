from django.db import models

# Create your models here.


class Deal(models.Model):
    item = models.IntegerField()
    price = models.IntegerField()
    deal_end_time = models.DateTimeField()
    active = models.BooleanField(default=True)


class UserDeal(models.Model):
    user_id = models.IntegerField()
    deal_id = models.IntegerField()
