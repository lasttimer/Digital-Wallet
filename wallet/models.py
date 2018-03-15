from django.db import models

# Create your models here.


class balance(models.Model):
    username = models.CharField(max_length=10)
    balance = models.FloatField(default=0)
    fd = models.FloatField(default=0)

    def __unicode__(self):
        return self.balance
