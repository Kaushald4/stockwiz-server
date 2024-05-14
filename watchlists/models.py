from django.db import models
from accounts.models import User

# Create your models here.
class WatchList(models.Model):
    title = models.CharField(max_length=100)

    symbol = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


# Since alphavantage API has rate limit of 25 request per day
# saving few stock symbol examples for search API 
class Symbol(models.Model):
    symbol = models.CharField()
    name = models.CharField()
    type = models.CharField()
    region = models.CharField()
