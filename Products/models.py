from django.db import models

# Create your models here.
class Product(models.Model):
    quality =(
        ('Good','Good'),
        ('Better','Better'),
        ('Best','Best'),
    )
    category = (
        ('Grocery','Grocery'),
        ('Snacks','Snacks'),
        ('Cooking oil','Cooking oil'),
        ('Tooth paste','Tooth paste'),
        ('Soap','Soap'),
        ('Beauty_products','Beauty_products'),
        ('Drinks','Drinks'),
        ('Masala','Masala'),
        ('Hair oil','Hair oil'),
        ('Yeepi noodles','Yeepi noodles'),
        ('Finail','Finail'),
        ('Biscuts','Biscuts'),
        ('Tea','Tea'),
        ('Others','Others'),
    )
    boolean = (
        ('True','True'),
        ('False','False'),
    )


    product_name = models.CharField(max_length=30,null=False,blank=False)
    brand = models.CharField(max_length=15,null=True,blank=True)
    quantity = models.CharField(max_length=20,null=False,blank=False)
    retail_price = models.CharField(max_length=30,null=False,blank=False)
    margin_price = models.CharField(max_length=30,null=False,blank=False)
    discount_price = models.CharField(max_length=10,null=True,blank=True)
    mrp = models.CharField(max_length=10,null=False,blank=False)
    discount_percentage = models.CharField(max_length=15,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='product_images',null=False,blank=False)
    quality = models.CharField(max_length=15,null=True,blank=True,choices=quality)
    category = models.CharField(max_length=20,null=False,blank=False,choices=category)
    special_offer = models.CharField(max_length=20,null=True,blank=True,choices=boolean)
    best_offer = models.CharField(max_length=20,null=True,blank=True,choices=boolean)
    upload_time = models.DateTimeField(auto_now_add=True)
    out_of_stock = models.BooleanField(max_length=20,null=True,blank=True,choices=boolean)

    def __str__(self):
        return self.name
