from django.db import models

# Create your models here.
class Address(models.Model):

    pins = (('755026','755026'),)
    panchayats = (
        ('Kumbhiragadia','Kumbhiragadia'),
        ('Manatira','Manatira'),
        ('Khapirapada','Khapirapada'),
    )
    states = (
        ('Odisha','Odisha'),
    )
    dists = (
        ('Jajpur','Jajpur'),
    )
    full_name = models.CharField(max_length=100,null=True,blank=True)
    mobile_number = models.CharField(max_length=20,null=True,blank=True)
    at = models.CharField(max_length=50,null=False,blank=False)
    landmark = models.CharField(max_length=50,null=False,blank=False)
    panchayat = models.CharField(max_length=50,null=False,blank=False,choices=panchayats)
    dist = models.CharField(max_length=50,null=False,blank=False,choices=dists)
    pin = models.CharField(max_length=20,null=False,blank=False,choices=pins)
    state = models.CharField(max_length=10,null=False,blank=False,choices=states)
    alternate_number = models.CharField(max_length=15,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        add = self.panchayat + self.pin
        return add

