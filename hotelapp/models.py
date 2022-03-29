from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='rooms', default='pix.jpg')
    
    def __str__(self):
        return self.title 

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Rooms(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='rooms', default='pix.jpg')
    description = models.TextField()
    booked = models.BooleanField()
    available = models.BooleanField()
    minn = models.IntegerField(default=1)
    maxn = models.IntegerField(default=100)
    paid_order = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    description = models.TextField( blank=True, null=True)
    paid_order = models.BooleanField(default=False)
    nights = models.IntegerField(blank=True, null=True)
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    order_no = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    pay_code = models.CharField(max_length=50)
    paid_order = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    order_no = models.CharField(max_length=50)

    def __str__(self):
        return self.username
        
